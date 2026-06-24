#!/usr/bin/env python3
"""Seed a sanitized Graphiti MCP memory episode.

This script intentionally uses only stdlib so it can run in minimal environments.
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.request
from pathlib import Path


def post_json(url: str, payload: dict, session_id: str | None = None) -> tuple[dict, str | None]:
    data = json.dumps(payload).encode("utf-8")
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
    }
    if session_id:
        headers["Mcp-Session-Id"] = session_id
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=30) as resp:
        body = resp.read().decode("utf-8", errors="replace")
        new_session = resp.headers.get("Mcp-Session-Id") or session_id
    # Some MCP servers respond as SSE. Keep parsing conservative.
    if body.startswith("event:") or "\ndata:" in body:
        for line in body.splitlines():
            if line.startswith("data:"):
                body = line.removeprefix("data:").strip()
                break
    return json.loads(body), new_session


def initialize(url: str) -> str | None:
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "graph-memory-case-study", "version": "0.1.0"},
        },
    }
    _, session_id = post_json(url, payload)
    return session_id


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default="http://localhost:8000/mcp/")
    parser.add_argument("--group-id", required=True)
    parser.add_argument("--name", required=True)
    parser.add_argument("--body-file", required=True)
    args = parser.parse_args()

    raw = Path(args.body_file).read_text(encoding="utf-8")
    try:
        parsed = json.loads(raw)
        body = parsed.get("episode", raw)
    except json.JSONDecodeError:
        body = raw

    session_id = initialize(args.url)
    payload = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/call",
        "params": {
            "name": "add_memory",
            "arguments": {
                "name": args.name,
                "episode_body": body,
                "group_id": args.group_id,
            },
        },
    }
    response, _ = post_json(args.url, payload, session_id=session_id)
    print(json.dumps(response, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())

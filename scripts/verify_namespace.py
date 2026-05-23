#!/usr/bin/env python3
"""Verify that a Graphiti namespace is usable through MCP tools.

Checks episodes, nodes, and memory facts through the runtime path rather than direct DB access.
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.request


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
            "clientInfo": {"name": "graph-memory-namespace-verifier", "version": "0.1.0"},
        },
    }
    _, session_id = post_json(url, payload)
    return session_id


def call_tool(url: str, session_id: str | None, tool: str, arguments: dict, request_id: int) -> dict:
    payload = {
        "jsonrpc": "2.0",
        "id": request_id,
        "method": "tools/call",
        "params": {"name": tool, "arguments": arguments},
    }
    response, _ = post_json(url, payload, session_id=session_id)
    return response


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default="http://localhost:8000/mcp")
    parser.add_argument("--group-id", required=True)
    parser.add_argument("--query", required=True)
    args = parser.parse_args()

    session_id = initialize(args.url)
    checks = [
        ("get_episodes", {"group_ids": [args.group_id], "max_episodes": 5}),
        ("search_nodes", {"query": args.query, "group_ids": [args.group_id], "max_nodes": 10}),
        ("search_memory_facts", {"query": args.query, "group_ids": [args.group_id], "max_facts": 10}),
    ]

    ok = True
    for idx, (tool, arguments) in enumerate(checks, start=2):
        print(f"\n== {tool} ==")
        try:
            response = call_tool(args.url, session_id, tool, arguments, idx)
            print(json.dumps(response, indent=2))
            if "error" in response:
                ok = False
        except Exception as exc:  # pragma: no cover - diagnostic script
            ok = False
            print(f"ERROR: {exc}")

    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())

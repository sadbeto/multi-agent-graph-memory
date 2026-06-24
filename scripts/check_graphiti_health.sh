#!/usr/bin/env bash
set -euo pipefail

URL="${1:-http://localhost:8000/mcp/}"

printf 'Checking Graphiti MCP endpoint: %s\n' "$URL"
status=$(curl -sS -o /tmp/graphiti_mcp_health.txt -w '%{http_code}' "$URL" || true)

if [[ "$status" == "200" || "$status" == "202" || "$status" == "400" || "$status" == "405" ]]; then
  printf 'Endpoint responded with HTTP %s. Server is reachable.\n' "$status"
  exit 0
fi

printf 'Unexpected HTTP status: %s\n' "$status"
printf 'Response body:\n'
sed -n '1,40p' /tmp/graphiti_mcp_health.txt || true
exit 1

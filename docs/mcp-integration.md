# MCP Integration

## Pattern

The agent runtime connects to Graphiti through MCP. Graphiti exposes tools such as:

- `add_memory`
- `get_episodes`
- `search_nodes`
- `search_memory_facts`
- `clear_graph`

Tool names can drift between Graphiti versions and wrappers. Always test the live MCP server instead of assuming the docs match your runtime.

## Example config

See `examples/config.example.yaml`.

## Streamable HTTP endpoint

A common local endpoint is:

```text
http://localhost:8000/mcp
```

The scripts in this repo use JSON-RPC over HTTP and initialize an MCP session before calling tools.

## Verification path

After seeding an episode, verify through the same path agents use:

1. `get_episodes(group_ids=[namespace])`
2. `search_nodes(query=..., group_ids=[namespace])`
3. `search_memory_facts(query=..., group_ids=[namespace])`

Do not rely only on database internals.

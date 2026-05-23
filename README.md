# Persistent Graph Memory for Multi-Agent AI Systems

A public-safe architecture case study for giving specialized AI agents persistent, isolated, queryable memory using Graphiti, FalkorDB, MCP, and namespace-based routing.

This repository documents the design pattern behind a personal AI "Guild": multiple specialized agents that each own a domain, remember prior context, and avoid contaminating each other's memory.

> Status: documentation-first case study with sanitized examples and utility scripts. It intentionally does not include private prompts, real chat IDs, secrets, production logs, or personal memory data.

## Why this matters

Most agent demos are stateless. They answer the current prompt, maybe use a scratchpad, and forget the rest.

A useful long-running agent system needs:

- Persistent memory across sessions
- Domain-specific memory boundaries
- Verifiable ingestion and retrieval
- Guardrails against cross-agent identity drift
- Operational checks that prove memory is actually usable at runtime

This repo captures a working pattern for that.

## High-level architecture

```text
User / Chat Channels / CLI
        |
        v
Hermes Agent runtime
        |
        | MCP tools over Streamable HTTP
        v
Graphiti MCP Server
        |
        | graph + vector operations
        v
FalkorDB
        |
        +-- graph: hermes        # orchestrator memory
        +-- graph: security      # defensive security agent memory
        +-- graph: markets       # investment research agent memory
        +-- graph: dev           # development agent memory
        +-- graph: planner       # planning / follow-up agent memory
```

Each agent has a namespace. Agents search and write only inside their namespace. The orchestrator routes incoming content to the correct agent and memory space.

## Core design principles

1. Memory isolation beats one giant shared memory.
2. Retrieval must be verified through the same MCP path agents use.
3. Successful ingestion calls are not enough; async processing can fail later.
4. Agent identity must be reinforced when graph context mentions other agents.
5. Public demos should use fake agent names and fake memories, not production data.

## What is included

```text
.
├── README.md
├── docs/
│   ├── architecture.md
│   ├── namespace-design.md
│   ├── mcp-integration.md
│   ├── safety-model.md
│   ├── lessons-learned.md
│   ├── identity-drift.md
│   └── roadmap.md
├── examples/
│   ├── config.example.yaml
│   ├── docker-compose.example.yml
│   ├── agent-registry.example.yaml
│   ├── seed-episode.example.json
│   └── agent-prompt-block.example.md
├── scripts/
│   ├── check_graphiti_health.sh
│   ├── seed_agent_memory.py
│   └── verify_namespace.py
└── diagrams/
    └── guild-architecture.svg
```

## Demo agent model

The real implementation used private agent names and private operational data. This public repo uses generic stand-ins:

| Namespace | Agent | Domain |
|---|---|---|
| `orchestrator` | OrchestratorAgent | Routing, system overview, agent coordination |
| `security` | SecurityAgent | Defensive security, hardening, audit findings |
| `markets` | MarketsAgent | Market research and risk notes |
| `dev` | DevAgent | Code, APIs, dashboards, engineering decisions |
| `planner` | PlannerAgent | Goals, reminders, follow-ups, second-angle review |

## Quick start

This assumes you already have a Graphiti MCP server running locally.

```bash
# 1. Check server health
./scripts/check_graphiti_health.sh http://localhost:8000/mcp

# 2. Seed one fake agent memory
python3 scripts/seed_agent_memory.py \
  --url http://localhost:8000/mcp \
  --group-id security \
  --name security-seed-v1 \
  --body-file examples/seed-episode.example.json

# 3. Verify retrieval through MCP tools
python3 scripts/verify_namespace.py \
  --url http://localhost:8000/mcp \
  --group-id security \
  --query "SecurityAgent defensive security"
```

## Important Graphiti/FalkorDB lessons

### `group_id` and `group_ids` are not interchangeable

In many Graphiti MCP setups:

- write tools use `group_id` as a singular string
- read/search tools use `group_ids` as an array

Passing `group_ids` to a write call can silently fall back to the default namespace.

### Avoid hyphens in namespace names

Some FalkorDB/RediSearch paths can break on hyphenated graph names. Prefer simple namespace IDs like `security`, `markets`, and `planner`.

### A successful write may only mean queued

Graphiti can process episodes asynchronously. A successful MCP response may mean the episode was accepted, not that entities and facts were extracted. Always verify retrieval after writing.

### Runtime verification beats database inspection

Agents use MCP tools, not direct database queries. If direct FalkorDB shows nodes but MCP search returns empty, the agent still cannot use that memory.

## Safety and privacy

This repo is intentionally sanitized.

Do not commit:

- `.env` files
- API keys or tokens
- real chat IDs
- personal memory episodes
- raw logs
- SQLite/state databases
- production prompts with private details
- local absolute paths from a private system

See `docs/safety-model.md` for the full public-release model.

## Portfolio value

This project demonstrates:

- Multi-agent architecture
- MCP-based tool integration
- Persistent graph memory
- LLMOps-style verification discipline
- Agent identity and memory-isolation design
- Public-safe documentation of a private production system

## License

MIT. See `LICENSE`.

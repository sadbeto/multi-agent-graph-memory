# Persistent Graph Memory for Multi-Agent AI Systems

A public-safe case study for the Guild I actually run day to day: one orchestrator, a handful of specialist agents, and a graph memory layer that keeps each lane useful without mixing everything together.

In plain English: each specialist agent gets its own memory lane, its own rules, and its own way of finding past context without stepping on the other agents.

> Status: documentation-first case study with sanitized examples and utility scripts. It intentionally does not include private prompts, real chat IDs, secrets, production logs, or personal memory data.

## Why this matters

Most agent demos are stateless. They answer the current prompt, maybe use a scratchpad, and forget the rest.

That works for a toy demo. It breaks down once the system has to remember decisions, avoid repetition, and stay useful after a restart. The real Guild has to survive restarts, handoffs, and the usual chaos of daily life.

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
        +-- graph: mrbeto        # defensive security agent memory
        +-- graph: pao           # investment research agent memory
        +-- graph: mira          # planning / follow-up agent memory
        +-- graph: zuck          # development agent memory
```

Each agent has a namespace. Agents search and write only inside their namespace. The orchestrator routes incoming content to the correct agent and memory space.

## Core design principles

1. Memory isolation beats one giant shared memory.
2. Retrieval must be verified through the same MCP path agents use.
3. A successful write is not the same as a usable memory.
4. Agent identity has to be reinforced when graph context mentions other agents.
5. Public artifacts should mirror the real operating model, but with names, IDs, paths, and logs stripped out.
6. If the docs feel too robotic, they probably need a human pass.

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

## Live agent model, sanitized

This is the real lane structure I use, just without the private stuff.

| Namespace | Agent | Domain |
|---|---|---|
| `hermes`        | Hermes    | Orchestration, routing, continuity, memory hygiene |
| `mrbeto` | Mr.Beto | Defensive security, hardening, audit findings |
| `pao` | Pao | Market research, risk notes, catalysts |
| `mira` | Mira | Second-angle review, reminders, proactive context |
| `zuck` | Zuck | Development, dashboards, APIs, engineering decisions |

## Quick start

This assumes you already have a Graphiti MCP server running locally.

```bash
# 1. Check server health
./scripts/check_graphiti_health.sh http://localhost:8000/mcp

# 2. Seed one sanitized agent memory
python3 scripts/seed_agent_memory.py \
  --url http://localhost:8000/mcp \
  --group-id mrbeto \
  --name mrbeto-seed-v1 \
  --body-file examples/seed-episode.example.json

# 3. Verify retrieval through MCP tools
python3 scripts/verify_namespace.py \
  --url http://localhost:8000/mcp \
  --group-id mrbeto \
  --query "Mr.Beto defensive security"
```

## Important Graphiti/FalkorDB lessons

### `group_id` and `group_ids` are not interchangeable

In many Graphiti MCP setups:

- write tools use `group_id` as a singular string
- read/search tools use `group_ids` as an array

Passing `group_ids` to a write call can silently fall back to the default namespace.

### Avoid hyphens in namespace names

Some FalkorDB/RediSearch paths can break on hyphenated graph names. Prefer simple namespace IDs like `hermes`, `mrbeto`, `pao`, `mira`, and `zuck`.

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

## What this repo is really showing

This project demonstrates the live operating model, only sanitized:

- Multi-agent architecture that feels operational, not hypothetical
- MCP-based tool integration
- Persistent graph memory
- Verification discipline for memory that may process asynchronously
- Agent identity and memory-isolation design
- Public-safe documentation of a private production system

It is not trying to look fancy. It is trying to show what was actually built, what broke, and what had to be learned the hard way.

## License

MIT. See `LICENSE`.

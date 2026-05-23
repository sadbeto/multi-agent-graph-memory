# Architecture

## Goal

Build a multi-agent AI system where each specialist agent has persistent graph memory without contaminating the memory or identity of other agents.

## Components

### Hermes Agent runtime

The main agent runtime exposes tools, routes work, and connects to MCP servers. In this pattern, it acts as the orchestration layer and is responsible for selecting the correct agent and namespace.

### Specialist agents

Each specialist agent owns one domain. Examples:

- `SecurityAgent`: defensive security, scans, hardening, findings
- `MarketsAgent`: market research, portfolio context, catalysts
- `DevAgent`: code, APIs, dashboards, project docs
- `PlannerAgent`: goals, reminders, follow-ups, second-angle review

### Graphiti MCP server

Graphiti provides memory ingestion and retrieval through MCP tools. It turns episodes into graph entities, relationships, and searchable facts.

### FalkorDB

FalkorDB stores the graph and vector-search backing data. The important design choice is using separate graph namespaces per agent.

## Request flow

```text
1. User sends message, URL, document, or screenshot.
2. Orchestrator classifies the content domain.
3. Orchestrator selects the target agent and namespace.
4. Agent searches its namespace before answering or acting.
5. Agent performs the task.
6. Agent writes durable lessons or useful episodes back to its namespace.
7. Verification checks confirm the memory can be retrieved through MCP.
```

## Memory write flow

```text
Agent decision
   |
   v
add_memory(name, episode_body, group_id)
   |
   v
Graphiti async processing queue
   |
   v
LLM extraction + embedding
   |
   v
FalkorDB graph/vector storage
   |
   v
verify with get_episodes + search_nodes + search_memory_facts
```

## Read-before-action pattern

Agents should search memory before answering when:

- the user refers to past work
- the task touches a known project
- the agent is about to make a recommendation
- the task depends on prior decisions, configs, or constraints

## Why namespaces instead of one shared graph

One shared memory graph creates three problems:

1. Retrieval noise: irrelevant facts from other domains appear in context.
2. Safety leakage: an agent may see data it should not use.
3. Identity drift: an agent may adopt the orchestrator's role or another agent's role when retrieved facts mention the wider system.

Namespaces reduce all three.

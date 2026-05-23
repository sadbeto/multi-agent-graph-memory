# Namespace Design

## Rule

Each agent gets exactly one write namespace. Agents may read their own namespace and, if explicitly allowed, a small orchestrator summary namespace. They should not write to another agent's namespace.

## Public demo namespace map

| Namespace | Owner | Purpose |
|---|---|---|
| `orchestrator` | OrchestratorAgent | System map, routing rules, public-safe overview |
| `security` | SecurityAgent | Defensive security facts and hardening history |
| `markets` | MarketsAgent | Market research and risk-management notes |
| `dev` | DevAgent | Engineering decisions, APIs, dashboards, debugging lessons |
| `planner` | PlannerAgent | Goals, reminders, planning context, follow-ups |

## Naming rules

Use:

- lowercase ASCII
- no spaces
- no hyphens
- short names
- stable names that will not change with branding

Avoid:

- `security-agent`
- `mr-security`
- `dev.agent`
- names with personal data

Recommended:

- `security`
- `markets`
- `dev`
- `planner`
- `orchestrator`

## Write example

```json
{
  "name": "security-seed-v1",
  "episode_body": "SecurityAgent owns defensive security memory. It tracks hardening decisions, scan summaries, and safe remediation notes.",
  "group_id": "security"
}
```

## Read example

```json
{
  "query": "hardening decisions scan summaries",
  "group_ids": ["security"],
  "max_facts": 10
}
```

## The important asymmetry

Write calls commonly use:

```text
group_id: "security"
```

Search calls commonly use:

```text
group_ids: ["security"]
```

This is easy to get wrong and can silently write data to the default namespace.

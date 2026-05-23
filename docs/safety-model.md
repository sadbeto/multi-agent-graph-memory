# Safety Model

## Public case-study rule

This repo documents architecture, not private operations.

## Never commit

- API keys
- tokens
- `.env` files
- real chat IDs
- private channel names
- personal memory episodes
- raw logs
- state databases
- SQLite files
- private hostnames/IPs
- production prompts with personal details
- local absolute paths from a private system

## Use sanitized examples

Replace private agents with generic stand-ins:

- `OrchestratorAgent`
- `SecurityAgent`
- `MarketsAgent`
- `DevAgent`
- `PlannerAgent`

Replace production namespaces with generic namespaces:

- `orchestrator`
- `security`
- `markets`
- `dev`
- `planner`

## Recommended pre-publish scan

```bash
git grep -nE 'API[_-]?KEY|TOKEN|SECRET|PASSWORD|BEGIN .*PRIVATE KEY|chat_id|telegram|discord|sqlite|state.db|/home/[a-zA-Z0-9_-]+' || true
```

Review every hit manually.

## Publish gate

Create and commit locally first. Do not create a public GitHub remote or push until the owner explicitly approves publishing.

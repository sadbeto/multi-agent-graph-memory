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

Replace private details with public-safe stand-ins, but keep the real lane structure intact:

- `router`
- `security`
- `research`
- `planning`
- `build`

Replace production namespaces with the live namespaces, but never leak channel IDs or private runtime data:

- `router`
- `security`
- `research`
- `planning`
- `build`

## Recommended pre-publish scan

```bash
git grep -nE 'API[_-]?KEY|TOKEN|SECRET|PASSWORD|BEGIN .*PRIVATE KEY|chat_id|telegram|discord|sqlite|state.db|/home/[a-zA-Z0-9_-]+' || true
```

Review every hit manually.

## Publish gate

Create and commit locally first. Do not create a public GitHub remote or push until the owner explicitly approves publishing.

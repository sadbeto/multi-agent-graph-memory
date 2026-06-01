# Namespace Design

## Rule

Each agent gets exactly one write namespace. Agents may read their own namespace and, if explicitly allowed, a small orchestrator summary namespace. They should not write to another agent's namespace.

That sounds strict, but it is what keeps the whole thing sane.

## Live namespace map, sanitized

| Namespace | Owner | Purpose |
|---|---|---|
| `hermes` | Hermes | System map, routing rules, public-safe overview |
| `mrbeto` | Mr.Beto | Defensive security facts and hardening history |
| `pao` | Pao | Market research and risk-management notes |
| `mira` | Mira | Goals, reminders, planning context, follow-ups |
| `zuck` | Zuck | Engineering decisions, APIs, dashboards, debugging lessons |

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
- anything that leaks chat IDs, phone numbers, or private hostnames

Recommended:

- `mrbeto`
- `pao`
- `mira`
- `zuck`
- `hermes`

## Write example

```json
{
  "name": "mrbeto-seed-v1",
  "episode_body": "Mr.Beto owns defensive security memory. It tracks hardening decisions, scan summaries, and safe remediation notes.",
  "group_id": "mrbeto"
}
```

## Read example

```json
{
  "query": "hardening decisions scan summaries",
  "group_ids": ["mrbeto"],
  "max_facts": 10
}
```


## The important asymmetry

Write calls commonly use:

```text
group_id: "mrbeto"
```


Search calls commonly use:

```text
group_ids: ["mrbeto"]
```


This is easy to get wrong and can silently write data to the default namespace.

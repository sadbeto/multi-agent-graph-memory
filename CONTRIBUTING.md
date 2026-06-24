# Contributing

Thanks for your interest. This is a public-safe case study, not a production package — contributions are welcome but the bar is simple: keep it honest, keep it sanitized.

## What fits

- Corrections to docs or examples
- Improvements to the utility scripts
- Additional sanitized example configs
- Clarifications on the Graphiti/FalkorDB pitfalls section
- Typos and grammar

## What does not fit

- Real API keys, chat IDs, or private system data
- Unrelated features or scope creep beyond graph memory for multi-agent systems
- Heavyweight dependencies added to the scripts

## Process

1. Fork the repo.
2. Make your changes on a branch.
3. Open a pull request with a short description of what changed and why.
4. No formal issue required for small docs fixes — just open the PR.

## Style

- Plain English, direct sentences.
- Code examples must be runnable or clearly marked as pseudocode.
- No marketing language. This repo should read like a builder's notes, not a product page.

## Sanitization check before submitting

Run a quick grep before pushing:

```bash
grep -rn "sk-\|ghp_\|Bearer\|password\|secret\|localhost:.*:[0-9]\{4,\}" . \
  --include="*.md" --include="*.yaml" --include="*.yml" --include="*.json" \
  --include="*.py" --include="*.sh"
```

If any real credentials or private paths show up, clean them before submitting.

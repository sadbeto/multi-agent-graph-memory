# Lessons Learned

## 1. The default namespace is a safety risk

If a write call omits `group_id`, data lands in the default namespace. Set that default to a safe orchestrator namespace and still require explicit `group_id` in every write.

## 2. `group_id` vs `group_ids` causes silent bugs

Use `group_id` for writes and `group_ids` for reads/searches. Put the examples right next to the prompt so the agent has no excuse to guess.

## 3. Hyphenated namespaces can break FalkorDB search paths

Use simple names like `mrbeto`, not `security-agent`.

## 4. Async ingestion needs verification

A successful tool response can just mean the episode was queued. Always check retrieval after the extraction pipeline finishes.

## 5. Identity drift is real

If an agent retrieves context that says "Hermes is the orchestrator" or lists all agents, some models may start speaking as the orchestrator. Repeat identity boundaries in:

1. channel/system prompt
2. agent documentation
3. skill/procedure file

## 6. Runtime checks matter more than backend checks

Agents cannot use memory that only appears in direct database inspection. Verify through MCP, the same way the agent will use it.

## 7. Public repos should be case studies, not backups

A clean public case study is better for portfolio value and safer than dumping a private working directory.

## 8. If it reads like a robot wrote it, trim it

The docs should still sound like a human built the system, hit real problems, and learned real lessons.

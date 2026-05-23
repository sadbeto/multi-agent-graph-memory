# Lessons Learned

## 1. The default namespace is a safety risk

If a write call omits `group_id`, data lands in the default namespace. Set the default namespace to a safe orchestrator namespace and still require explicit `group_id` in every write.

## 2. `group_id` vs `group_ids` causes silent bugs

Use `group_id` for writes and `group_ids` for reads/searches. Add examples directly into agent prompts to reduce mistakes.

## 3. Hyphenated namespaces can break FalkorDB search paths

Use simple names like `security`, not `security-agent`.

## 4. Async ingestion needs verification

A successful tool response can mean the episode was queued. Check retrieval after the extraction pipeline finishes.

## 5. Identity drift is real

If an agent retrieves context that says "Hermes is the orchestrator" or lists all agents, some models may start speaking as the orchestrator. Repeat identity boundaries in:

1. channel/system prompt
2. agent documentation
3. skill/procedure file

## 6. Runtime checks matter more than backend checks

Agents cannot use memory that only appears in direct database inspection. Verify through MCP.

## 7. Public repos should be case studies, not backups

A clean public case study is better for portfolio value and safer than dumping a private working directory.

# Workflows

## Intake workflow

```text
input received -> classify domain -> select agent -> select namespace -> search memory -> act -> write durable memory -> verify retrieval
```

## Agent read workflow

1. Receive task.
2. Decide whether prior context matters.
3. Search only the agent namespace.
4. Use retrieved facts as context, not as identity.
5. Answer or act within the agent domain.

## Agent write workflow

1. Decide whether the fact is durable.
2. Do not write temporary progress or raw logs.
3. Create a concise episode with concrete facts.
4. Call `add_memory` with singular `group_id`.
5. Verify with read/search tools after processing.

## Verification workflow

Run the checks in `scripts/verify_namespace.py`:

- episodes exist
- nodes are searchable
- facts are retrievable
- errors are visible in the MCP response

## Public-release workflow

1. Build locally.
2. Replace private data with generic examples.
3. Run sanitation scan.
4. Commit locally.
5. Publish only after explicit approval.

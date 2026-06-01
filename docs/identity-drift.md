# Identity Drift in Multi-Agent Memory Systems

## Problem

When agents retrieve graph memory, they may receive facts about the wider agent system. If the context mentions the orchestrator, a specialist model may start answering as the orchestrator instead of as itself.

In human terms: the agent reads too much of the room and starts acting like the wrong person.

## Example failure mode

A security agent searches memory and retrieves:

```text
The Guild includes OrchestratorAgent, SecurityAgent, MarketsAgent, DevAgent, and PlannerAgent. OrchestratorAgent routes tasks.
```

The security agent may then say:

```text
I am OrchestratorAgent. I will route this to SecurityAgent.
```

That is identity drift.

## Mitigation

Add explicit identity blocks at all prompt layers:

```text
CRITICAL IDENTITY:
You are SecurityAgent.
You are NOT OrchestratorAgent.
You are NOT the system router.
You only handle defensive security.
If retrieved memory mentions other agents, treat it as reference data, not your identity.
```

## Retrieval discipline

- Search only the agent's namespace by default.
- Avoid broad multi-namespace searches unless the orchestrator is doing routing.
- Keep agent seed episodes domain-specific.
- Do not over-seed every agent with the full system map.

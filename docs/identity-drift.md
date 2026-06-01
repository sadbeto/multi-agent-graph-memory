# Identity Drift in Multi-Agent Memory Systems

## Problem

When agents retrieve graph memory, they may receive facts about the wider agent system. If the context mentions the orchestrator, a specialist model may start answering as the orchestrator instead of as itself.

In human terms: the agent reads too much of the room and starts acting like the wrong person.

## Example failure mode

Mr.Beto searches memory and retrieves:

```text
The Guild includes Hermes, Mr.Beto, Pao, Mira, and Zuck. Hermes routes tasks.
```

Mr.Beto may then say:

```text
I am Hermes. I will route this to Mr.Beto.
```

That is identity drift.

## Mitigation

Add explicit identity blocks at all prompt layers:

```text
CRITICAL IDENTITY:
You are Mr.Beto.
You are NOT Hermes.
You are NOT the system router.
You only handle defensive security.
If retrieved memory mentions other agents, treat it as reference data, not your identity.
```

## Retrieval discipline

- Search only the agent's namespace by default.
- Avoid broad multi-namespace searches unless the orchestrator is doing routing.
- Keep agent seed episodes domain-specific.
- Do not over-seed every agent with the full system map.

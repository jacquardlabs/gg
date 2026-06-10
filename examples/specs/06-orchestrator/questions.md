---
type: questions
spec: 06-orchestrator
date: 2026-06-09
status: answered
---
# Questions before work starts

Reply inline at each "answer:". Each question states what happens if I guess.

## Needs your decision (reserved for you)

1. **Postgres or DynamoDB for the event store?** The spec reserves storage
   choices. Postgres: simpler local dev, transactional replay; Dynamo: less
   ops at scale we don't have yet.
   Recommendation: Postgres, revisit past 10k events/min. → answer: Postgres.

## Open questions

2. **R3 says the orchestrator "responds fast" — what number?** No latency item
   exists in Verification, so R3 is currently a wish. If unanswered I will
   target p95 < 500ms on the dispatch path, and that becomes the gate.
   → answer: 500ms is fine, make it a gate.

3. **R5 (replay) — replay from the beginning of time, or from a checkpoint?**
   Affects store schema and retention. If unanswered I will implement
   checkpoint-based replay with 30-day retention.
   → answer: checkpoint-based, 30 days, good default.

## Contradictions

4. **R5 (consumers can replay missed events) conflicts with the Interfaces
   section** ("consumers receive events only via the bus; consumers never read
   the store"). Replay implies someone reads the store. Which wins?
   → answer: the interface rule wins — replay goes through the bus too. The
   orchestrator re-publishes from the store; consumers stay bus-only. Recorded
   as ADR-3.

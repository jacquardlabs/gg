---
type: escalation
spec: 06-orchestrator
id: 001
date: 2026-06-12
status: resolved
blocks: [plan-4, plan-5]
scope: [src/orchestrator/queue.py]
---
# Two failed attempts: consumer drops messages under load

**Situation.** The load test (V2's precondition) loses ~2% of messages at
5k events/min. Attempt 1: exponential backoff on the consumer — no change.
Attempt 2: smaller batch size — reduced loss to 1.5%, still failing.
Hypothesis: the bug is upstream in ack timing — the orchestrator acks before
the bus confirms delivery, which is outside this plan item's scope.

**Options.**
1. Fix ack timing in the dispatch path — touches the dispatch interface named
   in the spec, so it needs your sign-off either way.
2. Compensate in the consumer with dedup + re-fetch — stays in scope, but
   treats the symptom and adds a consumer-side cache to maintain.

**Recommendation.** Option 1, because option 2 leaves every future consumer
re-solving the same problem.

**Continuing meanwhile.** Plan items 6–8 (metrics endpoint, config, docs) —
unaffected by this thread.

**Resolution.** Approved option 1. Ack only after bus confirmation; loss of
throughput is acceptable at our scale. — B, 2026-06-12

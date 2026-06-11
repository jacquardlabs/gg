---
type: plan
spec: 06-orchestrator
date: 2026-06-09
status: in-progress
---
# Plan

## Verification mapping

| Plan item | Requirement | Verification |
|---|---|---|
| P1: Postgres schema + migration | R2, R5 | V2, V5 |
| P2: event store layer (persist + query) | R2, R4, R5 | V2, V4, V5 |
| P3: gRPC consumer registry | R1 | V1 |
| P4: dispatch loop (fan-out to registered consumers) | R1, R3 | V1, V3 |
| P5: crash-recovery replay on startup | R4 | V4 |
| P6: consumer-requested replay via bus | R5 | V5 |
| P7: `/metrics` endpoint | R6 | V6 |
| P8: integration tests (R1–R6) | R1–R6 | V1–V6 |

## Steps

1. (P1) Write Postgres schema: `events` table (event_id UUID PK, topic text, payload jsonb, checkpoint_id UUID, dispatched_at timestamptz nullable), plus Alembic migration.
2. (P2) Implement `EventStore`: `persist(event)`, `mark_dispatched(event_id)`, `unreplayed_since(checkpoint_id)`. Wraps Postgres; no dispatch logic here.
3. (P3) Implement `ConsumerRegistry`: register/unregister by consumer_id + delivery callback; thread-safe snapshot for fan-out.
4. (P4) Implement dispatch loop: persist first, then fan-out to registry snapshot, then mark dispatched. Measure dispatch latency for the V3 benchmark.
5. (P5) On startup, call `unreplayed_since(last_checkpoint)` and re-run dispatch for each result before opening the publish port.
6. (P6) Add `ReplayRequest` to gRPC `ConsumerService`: orchestrator calls `unreplayed_since(checkpoint)`, re-publishes each event to the requesting consumer only via the existing dispatch path.
7. (P7) Add `/metrics` HTTP handler (stdlib `http.server`): read atomic counters incremented by the dispatch loop; emit Prometheus text format.
8. (P8) Write integration tests for V1–V6 using a real Postgres instance (pytest + psycopg3, no mocks).

```manifest
# Files this plan may edit. One path per line, relative to the git root.
# The manifest_check hook enforces this list.
examples/specs/06-orchestrator/orchestrator/__init__.py
examples/specs/06-orchestrator/orchestrator/store.py
examples/specs/06-orchestrator/orchestrator/registry.py
examples/specs/06-orchestrator/orchestrator/dispatch.py
examples/specs/06-orchestrator/orchestrator/metrics.py
examples/specs/06-orchestrator/orchestrator/recovery.py
examples/specs/06-orchestrator/proto/bus.proto
examples/specs/06-orchestrator/migrations/001_events.sql
examples/specs/06-orchestrator/tests/test_integration.py
examples/specs/06-orchestrator/plan.md
```

<!--
Plan revision log:
- 2026-06-09: initial plan from questions.md answers (Q1=Postgres, Q2=500ms gate,
  Q3=checkpoint-based 30d, Q4=bus-mediated replay / ADR-3). No requirements changed.
-->

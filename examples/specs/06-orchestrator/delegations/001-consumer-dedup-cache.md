---
type: mini-spec
spec: 06-orchestrator
id: 001
date: 2026-06-12
---
**Goal:** Implement a consumer-side dedup cache so that a consumer
restarting mid-batch delivers each message exactly once, eliminating the
duplicate-delivery failure in V2.

**Verification:** `pytest tests/test_crash_recovery.py` passes with zero
duplicate deliveries across all crash-mid-batch scenarios. The cache must
survive a process restart (persisted, not in-memory).

**Non-goals:** Do not touch the dispatch path or ack timing in
`src/orchestrator/dispatch.py` — that's covered by escalation 001's
resolution and is out of scope here. Do not add a cache management UI or
expose cache state via any endpoint.

**Guidelines:** CLAUDE.md applies. The cache key is `(consumer_id,
message_id)` — derive it from existing message metadata, do not add new
fields to the message schema (that would touch the spec's interface list
and require a drift check).

**Reserved decisions:** Cache storage backend (in-process SQLite vs.
Redis vs. filesystem) — this affects the deployment model. Escalate with
a recommendation if the choice is non-obvious; do not pick without
sign-off.

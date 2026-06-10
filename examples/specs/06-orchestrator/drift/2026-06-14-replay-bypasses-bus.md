---
type: drift-note
spec: 06-orchestrator
date: 2026-06-14
classification: structural
trigger: interface-touch
escalation: 002
---
# Drift: replay path reads the event store directly

**Intended shape** (spec §Interfaces, ADR-3): consumers receive events only
via the bus; replay re-publishes from the store through the bus; nothing but
the orchestrator touches the store.

**Current shape:** the replay implementation (plan item 5) gives consumers a
read-only store client for checkpoint recovery — consumers now have a second
path to events that bypasses the bus.

**Classification: structural** — touches an interface named in the spec, and
contradicts ADR-3 (definitional on both counts; no judgment applied).

**Action:** thread halted; escalation 002.

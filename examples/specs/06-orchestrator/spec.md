---
type: spec
spec: 06-orchestrator
date: 2026-06-09
---
# Event bus orchestrator

**Goal:** Implement an event bus orchestrator that dispatches events to registered consumers, persists events for replay, and exposes a Prometheus-compatible metrics endpoint — so the team can run durable, observable event-driven workflows without a third-party broker.

## Requirements

| # | Requirement |
|---|---|
| R1 | Consumers register and unregister via a gRPC API; the bus dispatches each published event to all registered consumers |
| R2 | Events are persisted to a Postgres store before dispatch; a crash between persist and dispatch leaves the event in the store for recovery on restart |
| R3 | The dispatch path meets p95 < 500ms under normal load |
| R4 | On restart after a crash, the orchestrator replays un-dispatched events before accepting new publishes |
| R5 | Consumers can request replay of missed events; replay is delivered via the bus (the orchestrator re-publishes from the store; consumers never read the store directly) |
| R6 | A `/metrics` endpoint exposes Prometheus-compatible counters: events published, events dispatched per consumer, dispatch errors, consumer lag |

## Verification

| R# | Gate |
|---|---|
| R1 | Integration test: register two consumers, publish an event, assert both receive it; unregister one, publish again, assert only the remaining consumer receives it |
| R2 | Integration test: insert an event row directly, kill the process, restart, assert the event is dispatched on startup |
| R3 | Benchmark: publish 1000 events under two concurrent consumers; assert p95 dispatch latency < 500ms in the benchmark output |
| R4 | Covered by R2 test |
| R5 | Integration test: consumer registers, 10 events published, consumer unregisters; consumer re-registers and requests replay from checkpoint; assert all 10 events delivered via bus |
| R6 | Start the service, publish 5 events, hit `/metrics`; assert counters `events_published`, `events_dispatched`, `consumer_lag` are present and non-zero |

## Non-goals

- No web UI or human-facing dashboard (ruled out by triage; the metrics endpoint feeds Grafana directly)
- No multi-tenant isolation; single namespace for all consumers
- No at-most-once delivery guarantee; at-least-once is sufficient and simpler
- No cross-datacenter replication

## Reserved for human

- Schema migration strategy if the event store needs a column change after data exists
- Retention policy changes (currently 30-day checkpoint-based; any change is a data-loss decision)
- Adding a new external dependency beyond Postgres and the existing gRPC stack

## Interfaces

Public surfaces this spec owns:

- `ConsumerService` gRPC service (register, unregister, receive stream)
- `PublisherService` gRPC service (publish)
- `GET /metrics` HTTP endpoint (Prometheus text format)
- `events` Postgres table schema (event_id, topic, payload, checkpoint_id, dispatched_at)

ADR-3 records: replay is bus-mediated; consumers never read the store directly.

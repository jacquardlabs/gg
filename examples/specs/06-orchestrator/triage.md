---
type: triage
date: 2026-06-09
verdict: REFRAME
---
# "Build a web dashboard so ops can monitor event processing"

**Verdict: REFRAME**

The underlying need — ops visibility into the bus — is real and worth
solving. A web dashboard is the wrong lever: it requires a server,
authentication, and a deployment pipeline we don't have, and it would
need to stay current with every schema change. The metrics endpoint
already exists (`/debug/state`, added during the crash-recovery
investigation) and exposes exactly what ops needs. The gap is surfacing
it, not building a UI around it.

**Underlying need:** Ops needs to see event throughput, consumer lag, and
error rates without digging into logs.

**Better path:** Structured `/metrics` endpoint (Prometheus-compatible)
on the existing orchestrator process + Grafana dashboard config checked
into the repo. No new server; hooks into the monitoring stack the team
already runs. Two-day build vs. two weeks.

**Proceeds to spec:** yes

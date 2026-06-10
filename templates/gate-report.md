---
type: gate-report
spec: <NN>-<slug>
date: <YYYY-MM-DD>
claimed: <done | partial>     # the agent's claim, recorded BEFORE gates run
verdict: <pass | fail>        # what the gates found
---
# Gate run

**Claim (recorded before gates ran):** "<the agent's completion claim,
verbatim>"

<!--
Sequencing rule: capture the claim BEFORE executing any verification item.
The claimed/verdict pair, aggregated over time, is the perception-gap
dataset. A claim written after the gates ran measures nothing.
-->

## Verification items

| # | Item (from spec) | Check | Proof | Result |
|---|---|---|---|---|
| V1 | <verification item, verbatim from spec> | `<command>` | <path or "below"> | PASS / FAIL / BLOCKED |

<For any FAIL: the relevant output excerpt. For any BLOCKED: the open
escalation id.>

## Claimed vs verified

<One or two sentences: what was claimed, what the gates found, and where the
gap was — what was asserted but never run.>

## Traceability

| Change | Plan item | Requirement |
|---|---|---|
| <path> | <plan-item or — > | <RN or — > |

<List orphans (changes with no plan item) explicitly, each routed to plan
revision or revert. An empty orphan list is stated, not implied.>

## Route

<Per failure: back to which plan item, or to an escalation. Per orphan: plan
revision proposed or revert. On full pass: ready for PR; attach this report.>

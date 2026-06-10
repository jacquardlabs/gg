---
type: drift-note
spec: <NN>-<slug>
date: <YYYY-MM-DD>
classification: <none | minor | structural>
trigger: <milestone | interface-touch | refactor | adr-conflict | requested>
escalation: <NNN>             # REQUIRED when classification is structural or trigger is adr-conflict; omit otherwise
---
# Drift: <one line — what shape changed>

**Intended shape** (<spec section / ADR reference>): <the intended structure,
one sentence — components and the direction of dependencies, not code>.

**Current shape:** <what the structure actually is now, one sentence, with the
plan item that introduced it>.

**Classification: <X>** — <cite the rule. Definitional where possible: "touches
an interface named in the spec," "changes a public signature." Judgment-based
classifications say so explicitly.>

**Action:** <none / note only / thread halted; escalation NNN>.

<!--
- Diff-of-shape, not diff-of-code: intended vs current in two sentences.
  Steward reads these in aggregate; a code diff is noise at that altitude.
- `trigger` keeps classification honest in aggregate: if structural drift
  only ever arrives via "requested" and never via "interface-touch", the
  automatic tripwires are not firing — that itself is a steward signal.
-->

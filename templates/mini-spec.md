---
type: mini-spec
spec: <NN>-<slug>
id: <NNN>                     # sequential within this work item
date: <YYYY-MM-DD>
---
**Goal:** <What to produce — one sentence. A measurable output, not an
activity. "Implement X so that Y" is a goal; "work on X" is not.>

**Verification:** <How the output will be checked. At least one concrete
check: a test to run, a behavior to observe, a file to inspect. Without
this the delegation is a wish, not a contract.>

**Non-goals:** <What the agent must not do. Scope boundary. At least one.>

**Guidelines:** <Rules inherited from CLAUDE.md apply. List any overrides
or additional constraints specific to this delegation only.>

**Reserved decisions:** <Decisions the agent cannot make. Propagated from
the parent spec. If reached: escalate, do not absorb.>

<!--
- Minimum viable: Goal + Verification + Non-goals. Guidelines inherits
  from CLAUDE.md if not overridden. Reserved-decisions omit only if the
  parent spec has none.
- The PreToolUse hook checks for Goal:, Verification:, and Non-goals:
  labels. A delegation prompt missing any of these is rejected.
- Subagent output is verified at its boundary using the Verification
  section — never trusted on the agent's say-so.
- Five total lines is fine. Do not pad.
- Save a copy to delegations/<NNN>-<slug>.md in the work item dir.
-->

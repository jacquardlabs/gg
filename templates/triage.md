---
type: triage
date: <YYYY-MM-DD>
verdict: <BUILD | BUILD-SMALLER | REFRAME | DEFER | DONT-BUILD>
spec: <NN>-<slug>             # omit when verdict is DEFER or DONT-BUILD
---
# <one-line description of what was evaluated>

**Verdict: <BUILD | BUILD SMALLER | REFRAME | DEFER | DON'T BUILD>**

<Rationale — two to four sentences. Why this verdict. Plain English; no
gg vocabulary. This is the part the sender reads.>

<!-- Remove sections that don't apply to the verdict. -->

**What's in:** <the 80% version — what this delivers>
**What's deferred:** <what's explicitly out and why — not "never," just "not now">

<!-- BUILD SMALLER only: the two lines above. -->

**Underlying need:** <the actual problem this idea is trying to solve>
**Better path:** <the different change that addresses it more directly>

<!-- REFRAME only: the two lines above. -->

**Preconditions:** <what would need to change for this to become BUILD>

<!-- DEFER only: the line above. -->

**Proceeds to spec:** yes / no

<!--
Rules:
- Verdict recorded before analysis is written — commit to the label,
  then write the rationale. Avoids the rationale driving the verdict.
- The body is for the sender. A PM reading this needs no knowledge that
  gg exists. No jargon; no references to internal processes.
- REFRAME is not rejection. It says: the underlying need is real; this
  particular solution is not the right lever.
- If BUILD or BUILD-SMALLER: `spec:` frontmatter key links to the work
  item this becomes. If DEFER or DONT-BUILD: omit it.
-->

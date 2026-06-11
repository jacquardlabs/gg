---
description: Independent product-reviewer pass on the spec before decompose. Catches scope, persona mismatch, and simplest-version gaps the author is too close to see. Returns PROCEED TO PLAN / REVISE / RETHINK.
allowed-tools: Read, Glob, Grep, Task
---

# Spec Review

Independent review of the spec contract before decompose. The author red-teamed their own spec; this gate provides a perspective they can't give themselves — whether the design serves actual users and fits the product.

Run this gate after the human confirms the spec, before spawning decomposing-specs.

Read PRODUCT.md and DESIGN.md first. If PRODUCT.md is absent, proceed with best-effort review and flag the absence as a finding.

## Part 1 — Product review

Invoke `product-reviewer` as a subagent with instruction: "Review this spec as a pre-implementation design doc. Use the Gate 2 (design doc review) context in your prompt. Ground every judgment in PRODUCT.md personas and journeys."

Pass the spec's path: `specs/<NN>-<slug>/spec.md`.

## Part 2 — Persona walkthrough

Walk through the spec as the primary persona from PRODUCT.md would experience the feature it describes. Narrate step by step:

- How does the persona discover this feature exists?
- What is their first interaction with it?
- What are they thinking and feeling at each step?
- Where might they get confused, frustrated, or surprised?
- Does it feel like it belongs in this product, or does it feel bolted on?
- Is there a step where they would think "what?" or reach for a help doc?

Be honest. If any step feels forced or unnatural, say so.

## Part 3 — Verdict

Synthesize the product-reviewer findings and persona walkthrough into a clear recommendation:

- **PROCEED TO PLAN**: design is sound, no product concerns — hand off to decomposing-specs
- **REVISE**: specific issues must be addressed before implementation (list in priority order) — update the spec, re-confirm with the human, re-run spec-review
- **RETHINK**: fundamental product misalignment — route back to writing-specs triage phase with a clear statement of why

## Record the verdict

File: `specs/<NN>-<slug>/spec-review.md`

Frontmatter: `type: spec-review`, `date`, `verdict`

Body: the product-reviewer findings (classified as BLOCKS SHIP / SHOULD FIX / MINOR / OBSERVATION), the persona walkthrough narrative, and the verdict with its rationale.

The spec-review is a design-time gate. Its output is not a gate evidence report (those belong in `gates/`) — it's a record of the independent review that the human relied on before authorizing decompose.

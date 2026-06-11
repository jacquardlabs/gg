---
description: Post-implementation product acceptance gate — experience check, error states, journey regression, first-time-user test. Returns SHIP / FIX AND RE-CHECK / HOLD.
allowed-tools: Read, Glob, Grep, Bash, Task
---

# Acceptance

Post-implementation product acceptance gate. Verify that the implementation delivers the intended experience, not just that the code works. This is one of the two standard verification implementations in the gg gate library.

Read PRODUCT.md first. If absent, proceed with a best-effort review and flag the absence.

## Part 1 — Product review

Invoke `product-reviewer` as a subagent with the instruction: "Review the implementation on the current branch against the spec and PRODUCT.md. This is a post-implementation acceptance review (Gate 3 context in the product-reviewer prompt)."

## Part 2 — Implementation walkthrough

Walk through every user-facing change on this branch:

1. **Experience check.** For each user-facing change — what does the user see? Does it match what the spec intended? Call out gaps between intent and result.

2. **Error states.** Find every error path, empty state, and edge case in the changeset. For each: is the message helpful and human, or technical and confusing?

3. **Journey regression.** Check the critical user journeys in PRODUCT.md. With this feature present, walk through each. Flag anything that feels different, slower, or requires an extra step — even subtly.

4. **First-time user test.** Read the feature as someone with zero context. Is it self-explanatory? Or does it assume knowledge the user wouldn't have?

5. **One complaint.** What's the single thing a real user would complain about if shipped as-is? Be specific. There is always something.

## Verdict

Record the verdict in the gate report:

- **SHIP**: Implementation delivers the intended experience; no user-facing issues that block merge.
- **FIX AND RE-CHECK**: Specific user-facing issues to address (list each with severity). Fix, then re-run `/acceptance`. Do not edit mid-run — finish the run first.
- **HOLD**: Fundamental gap between design intent and implementation; rework required beyond quick fixes.

For FIX AND RE-CHECK items, be specific enough that each one can become a concrete fix task routed to a plan item.

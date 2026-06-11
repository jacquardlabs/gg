# gg

This repo is the home of the **gg + steward** portfolio: gg (the goals-and-guidelines Claude Code plugin, inner loop) and steward (the staff+ sensemaking practice/tool, outer loop).

**`DESIGN.md` is the source of truth** for all portfolio decisions — layering, naming, workflow, standing rules, open items. Read it before designing anything; record new decisions in it, not in conversation.

## Boundaries

- **cctx is an external dependency.** Treat it as a black box with a CLI contract (see DESIGN.md §2). Never design cctx features, internals, or changes in this project — if gg needs something from cctx, record it as an interface request against cctx's public CLI, don't reach in.
- gg must degrade gracefully when cctx is absent; cctx enriches, never load-bearing.
- Data flows up (cctx → gg → steward); opinions never flow down.

## Vocabulary

- Metaphor names things; it never operates them. Commands, skill names, trigger phrases, file names, and error messages use plain software vocabulary. The loom/Jacquard story is essay material only.
- Artifacts (questions reports, escalation notes, gate evidence reports, drift notes) must be legible to people who have never heard of gg — recipient-facing, plain English, no suite jargon.

## Behavioral rules

- Review the plan before starting work. Stop on blockers rather than improvising. Mark tasks done one at a time, not in batches.
- Never claim work is complete, tests pass, or a bug is fixed without running the verification command in this message first.
- No fixes without root cause investigation first. Hypothesize, then verify, then fix.
- No production code without a failing test first. Tests define the contract; code satisfies it.

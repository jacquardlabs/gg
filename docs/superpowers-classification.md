# Superpowers skill classification

*Produced 2026-06-10 per DESIGN.md §9 migration plan.*
*Dispositions: replaced-by-gg | demoted-to-guideline | retained | retained-with-overlap*

---

| Skill | Disposition | gg counterpart | Notes |
|---|---|---|---|
| `writing-plans` | **replaced-by-gg** | `decomposing-specs` | decomposing-specs owns "decompose spec into plan with verification mapping." writing-plans' plan format (`docs/superpowers/plans/`) is superseded by `specs/<NN>-<slug>/plan.md` + manifest block. File-structure thinking and bite-sized-step guidance demote to CLAUDE.md guidelines. Disable after decomposing-specs passes retention test. |
| `executing-plans` | **demoted-to-guideline** | `decomposing-specs` → plan.md execution | Execution discipline ("review before starting, stop on blockers, mark done not in-progress") is CLAUDE.md-level behavior, not a boundary skill. gg's plan.md + manifest hooks replace the plan format. Key rules to harvest into CLAUDE.md before disabling. |
| `verification-before-completion` | **demoted-to-guideline** | `running-gates` (macro) | Iron Law ("evidence before claims, always") is a single CLAUDE.md entry. Micro-level claim discipline — "run the command in this message before claiming it passes" — is a guideline. running-gates handles the structured macro-boundary event. Harvest the Red Flags list into CLAUDE.md; disable the skill. |
| `brainstorming` | **retained** | partial overlap with `writing-specs` | brainstorming handles pre-spec creative exploration (fuzzy idea → clear design); writing-specs handles the contract authoring (clear idea → spec). They're sequential, not competing. One friction point: brainstorming writes to `docs/superpowers/specs/`; gg specs live in `specs/<NN>-<slug>/`. Resolve at first use: brainstorming output should flow into gg's spec.md, not stay in the superpowers path. |
| `dispatching-parallel-agents` | **retained** | complementary to `delegating-with-specs` | governs orchestration mechanics (how to run multiple independent agents); delegating-with-specs governs delegation quality (what goes in each delegation). Orthogonal. Constraint to enforce: any dispatch via dispatching-parallel-agents must include a mini-spec per delegating-with-specs. |
| `finishing-a-development-branch` | **retained** | downstream of `running-gates` | handles git mechanics (merge, PR, worktree cleanup) — outside gg's scope. Sequencing rule to document: running-gates must pass before finishing-a-development-branch runs. Gate evidence report attaches to the PR this skill creates. |
| `receiving-code-review` | **retained** | none | Pure behavioral discipline for receiving reviewer feedback. No gg boundary counterpart. Retained indefinitely. |
| `requesting-code-review` | **retained** | complementary to `running-gates` | running-gates verifies spec conformance; requesting-code-review verifies code quality. Sequential and complementary: running-gates passes → request code review → address findings → finishing-a-development-branch. Neither replaces the other. |
| `subagent-driven-development` | **retained-with-overlap** | `delegating-with-specs` + `running-gates` | The spec-compliance reviewer step (spec-reviewer-prompt.md) overlaps with what running-gates does at a task boundary. Over time, delegating-with-specs + running-gates absorbs the spec compliance review. The "fresh subagent per task, zero context inheritance" orchestration principle is not in gg and stays. Revisit at gg 1.0. |
| `systematic-debugging` | **retained** | `escalating` (when debugging fails) | Debugging methodology is how-knowledge, not a boundary behavior. Too detailed for a CLAUDE.md guideline. escalating handles the case where debugging exhausts its attempts; systematic-debugging handles how to investigate before that point. Iron Law ("no fixes without root cause first") should also appear in CLAUDE.md as a summary entry. |
| `test-driven-development` | **retained** | none | Implementation methodology — how-knowledge, not a boundary behavior. Iron Law ("no production code without a failing test first") should appear in CLAUDE.md as a summary entry alongside the full skill. Too detailed for a guideline alone. |
| `using-git-worktrees` | **retained** | none | Workspace isolation is infrastructure, outside gg's scope. Sequencing: using-git-worktrees → decomposing-specs (isolation before planning). |
| `using-superpowers` | **retained** (meta) | none | Meta-framework skill. gg's TRIGGER sections provide auto-triggering that reduces the cognitive overhead of "always check for a skill first," but the meta-skill itself remains the harness. Update eventually to note gg's TRIGGER model. |
| `writing-skills` | **retained** | none | Skill authoring methodology — standalone meta-skill. Low-frequency by nature; must be retention-tested with injected scenarios (not usage counts). |

---

## Migration sequence

**Disable first (safest — clear replacements, low consequence if wrong):**
1. `executing-plans` → harvest CLAUDE.md rules, disable
2. `verification-before-completion` → harvest Iron Law + Red Flags to CLAUDE.md, disable

**Disable after retention test:**
3. `writing-plans` → disable two weeks after `decomposing-specs` enters rotation; cctx data decides; if recurrence of planning-quality regressions, revert

**Never disable based on usage counts:**
- `systematic-debugging` — low-frequency on healthy sessions, high-consequence when needed (fire alarm)
- `writing-skills` — invoked rarely by design; test with injected scenarios

**CLAUDE.md harvests before any disable:**
- From `executing-plans`: "Review the plan before starting work. Stop on blockers rather than improvising. Mark tasks done one at a time, not in batches."
- From `verification-before-completion`: "Never claim work is complete, tests pass, or a bug is fixed without running the verification command in this message."
- From `systematic-debugging`: "No fixes without root cause investigation first."
- From `test-driven-development`: "No production code without a failing test first."

---

## Disposition counts

| Disposition | Count | Skills |
|---|---|---|
| replaced-by-gg | 1 | writing-plans |
| demoted-to-guideline | 2 | executing-plans, verification-before-completion |
| retained | 10 | brainstorming, dispatching-parallel-agents, finishing-a-development-branch, receiving-code-review, requesting-code-review, systematic-debugging, test-driven-development, using-git-worktrees, using-superpowers, writing-skills |
| retained-with-overlap | 1 | subagent-driven-development |

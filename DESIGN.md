# gg + steward — Portfolio Design

*2026-06-09 · Consolidated from the founding design session. This document is the durable record of decisions; the conversation that produced it is not the source of truth — this file is.*

---

## 1. Thesis

Code review used to do two jobs in one ritual: **verification** (is this change correct and acceptable?) and **sensemaking** (does the team still understand the system?). Agent-speed development breaks the ritual — volume arrives faster than anyone can read — so both jobs go unserved. This portfolio ships the unbundled replacements:

- **gg** re-houses *verification* in the inner loop: contracts in, agent works the middle, gates and evidence at the boundary.
- **steward** re-houses *sensemaking* in the outer loop: drift against intent, the human's own read first, trends over snapshots.

One epistemic claim runs through both: **at agent speed, self-assessment fails.** The agent's "it's done" and the developer's "I've got this" are equally unreliable, and both need an external signal at a boundary. gg is that structure for the agent; steward is that structure for the human. This claim is the original contribution — the seam to own in all public writing.

## 2. The portfolio

| Layer | Object | Timescale | Question it answers |
|---|---|---|---|
| **gg** (plugin) | the deliverable | hours–days | did the work fulfill its contract? |
| **steward** (practice → tool) | the humans' mental model | weeks–months | do we still understand the system we own? |

**External dependency: cctx.** cctx is deliberately outside the portfolio — a session-debugging product with its own users and lifecycle, and the referee for the migration data (the referee cannot wear the team jersey). Its entire relationship to this portfolio is this contract, and every other cctx mention in this document defers to it:

- gg consumes cctx's CLI output through thin wrappers: `watch` signals, `autopsy`/`harvest` output, `export`. Consumption only; cctx never knows gg exists.
- **gg degrades gracefully when cctx is absent.** gg's own hooks provide the baseline tripwires; cctx enriches but is never load-bearing. A gg feature that hard-requires cctx is rejected.
- If gg needs something cctx doesn't provide, that's an interface request recorded against cctx's public CLI — never a design decision made here.

**Layer rule: data flows up, opinions never flow down.** cctx → gg → steward. Any feature that violates the direction (cctx gaining a "gg mode," gg requiring steward concepts) is rejected on the rule alone.

## 3. Naming (decided)

- **gg** — the plugin. From "goals & guidelines," the methodology itself; the expansion teaches the concept. Two keystrokes for the thing typed at every handoff. Free tagline: *it's not done until gg says gg.* Never ship a bare `gg` shell binary (PyPI `gg`, gg-scm, gg2 exist); the name lives as plugin namespace and slash command.
- **steward** — the outer-loop tool, formerly "Eddy." Names the staff/principal/architect posture; joins existing discourse ("stewardship over ownership," Foundation for Public Code's "codebase stewardship") with no product squatting on the word (nearest neighbor: Scala Steward, a dependency bot). Runners-up, recorded for posterity: reckon (dead reckoning — keep as a possible framework-essay frame), bearings, perch.
- **warp is dead** — warp.dev is "The Agentic Development Environment," same niche, 700K+ users. Disqualifying collision.
- **jaqal archives** with a pointer: "jaqal evolved into gg." Single-digit external users; migration note suffices. Its gates are absorbed (see §5); its pipeline framing retires.
- **Jacquard Labs** remains the org-level narrative brand. The loom story (automation moved the craft to the boundaries; punch cards became computing) is essay material, never operational vocabulary.

**Vocabulary guideline:** *Metaphor names things; it never operates them.* Every command, skill name, trigger phrase, file name, and error message uses plain software vocabulary. A metaphor term may never be the only name for a thing. Test: a user who skipped the README's framing can still use everything.

## 4. gg — the inner loop

### The inversion

superpowers encodes process; gg encodes boundaries. Membership test for any candidate skill: **does it govern the protocol at a handoff (what/when/boundaries), or does it script how the domain work is done?** Interface protocols may be procedural — that's what a contract is. How-knowledge becomes a one-line guideline in CLAUDE.md or is trusted to the agent and caught by gates; it never becomes a suite skill.

### The thesis: contracts at every handoff

PM→dev, dev→agent, agent→subagent, dev→reviewer. A PM ticket is a (usually malformed) spec; agents didn't create the handoff problem, they multiplied handoff frequency past what informal habits absorb. The model is fractal in both directions.

### Three knowledge layers

- **Specs** — per-project goals; ephemeral contracts; owned by the human
- **Guidelines** — durable rules in CLAUDE.md; evolve by harvest
- **Skills** — portable boundary behaviors (this plugin)

Misfiled knowledge is the failure mode; `tending-guidelines` enforces the taxonomy.

### The eight boundary skills

1. **writing-specs** — author and pressure-test the contract; every requirement maps to a verification item ("a requirement without a gate is a wish"); mandatory non-goals and reserved-for-human sections; ends with a red-team pass naming the spec's three weakest points. Absorbs jaqal's should-we-build gate as intake triage, with verdicts BUILD / BUILD SMALLER / **REFRAME** (new: a different change solves the underlying need) / DEFER / DON'T BUILD.
2. **decomposing-specs** — the agent's mandatory first move on receiving a spec; no code before the questions round-trip (open questions, reserved-for-human decisions spotted, ambiguities); then a plan where every item maps to a verification item. **The spec is the human's contract and is not revisable by the agent; the plan is the agent's artifact and is freely revisable** — but every revision re-checks the verification mapping and regenerates the file manifest (§6).
3. **escalating** — stopping conditions; stop means stop *on that thread*, unblocked work continues. Escalation format: situation, options with tradeoffs, recommendation, what continues meanwhile. Notes carry open/resolved status. Session-level rule: when all threads block, end gracefully ("blocked on N escalations") — never idle-grind or rationalize around the blockage.
4. **running-gates** — execute the spec's Verification section literally, item by item, proof attached per item. Records **claimed-vs-verified delta** (the agent's completion claim vs. gate findings — perception-gap data for steward). Includes a **traceability section**: every change maps to a plan item maps to a requirement; orphan changes listed. Agent self-assessment is never a completion signal. The gate evidence report is most trustworthy when CI-attested (generated by the Action during the agentic job, not by the agent afterward) — an author-generated report is gameable; a CI-generated one is not. Redaction rule: findings and metrics travel in the report; transcript content does not.
5. **tending-guidelines** — the CLAUDE.md lifecycle. A repeating failure means a missing guideline, not a bad agent. Guidelines are short, testable, behavioral. Every lesson routes to its correct layer with the routing stated. Owns hook/tripwire tuning (§6) — false positives are harvest input, same as false negatives. Guideline diffs stay in git, dated.
6. **instrumenting-sessions** — hybrid: session-start is a SessionStart hook (deterministic — cctx watch on, purpose tags, MCP/skills manifest verification against lockfile); session-end self-autopsy is a skill (judgment — what shipped, cost, deviations, harvest candidates, open threads). Manifest drift at session-start is a blocking signal: a poisoned or unexpectedly updated tool description is an attack surface (CVE-2025-54136, rug-pull class), not a config curiosity.
7. **checking-drift** — compare built structure against the spec's interfaces and ADRs at milestones, before tagging, after large refactors. Classify none/minor/structural; structural halts the thread and escalates; ADR contradiction always escalates. "Structural" is *definitional* wherever possible (any public-signature change, anything on the spec's interface list) to resist self-serving classification. Drift notes stay in git — steward's input and future training data.
8. **delegating-with-specs** — every delegation gets a mini-spec (goal, guidelines, verification, non-goals; five lines is fine). Subagent output is verified at its boundary, never trusted. Reserved decisions propagate and can never be absorbed by a subagent. Enforced, not honor-system (§6).

### Gate library

jaqal's gates become the verification implementations `running-gates` executes: audit, acceptance, design-review, plus test/eval invocations. During dogfood, `running-gates` wraps the existing jaqal commands unmodified; native folding happens at merge time.

### Team story: single-player software, multiplayer artifacts

No servers, no accounts, no shared state at 1.0. The team story rides on artifacts in git and existing channels: the questions report is the ticket-refinement comment; the escalation note goes to the lead; the gate evidence report attaches to the PR; guidelines evolve in a shared CLAUDE.md through normal PR review. Two hard requirements follow:

1. **Artifacts must be legible to non-users.** A PM reading a triage verdict or a reviewer reading an evidence report needs zero knowledge that gg exists. Recipient-facing, plain English, no suite jargon.
2. **Trigger language must cover team vocabulary** — "PM sent me this," "groom this ticket," "is this worth doing" — not just solo-dev phrasing.

If a feature idea needs a server, it is post-1.0 by definition.

## 5. The workflow

```
                       THE INNER LOOP (gg) — per piece of work

  ticket/idea ──► 1 TRIAGE ──► 2 SPEC ──► 3 DECOMPOSE ──► 4 BUILD ──► 5 GATES ──► merged
                     │            │           │              │           │
                     ▼            ▼           ▼              ▼           ▼
                  verdict      spec +     questions rpt   escalation   evidence
                               weaknesses   + plan        + drift notes  report
                     │            │           │              │           │
                     └────────────┴───────────┴──────┬───────┴───────────┘
                                                     │ 6 HARVEST (weekly + on pain)
                                                     ▼
                                              guideline changelog
                                                     │
            ═════════════════════════════════════════╪═════ the seam: artifacts in git
                                                     ▼
                       THE OUTER LOOP (steward) — per system, on cadence

        7 OWN READ ──► 8 COMPARE ──► 9 DRIFT & TRENDS ──► 10 INTENT REFRESH
        (human first)  (then tool)   (direction, not        (ADRs/charter updated;
                                      snapshots)             feeds the next spec)
```

| Step | Trigger | Action | Artifact |
|---|---|---|---|
| 1 Triage | handoff arrives: ticket, idea, "should we build this" | evaluate against product context: buildable? smaller 80% version? different change for the same need? | verdict (BUILD / SMALLER / REFRAME / DEFER / DON'T), legible to the sender |
| 2 Spec | BUILD-ish verdict; "spec this out" | author the contract with the human; red-team it | spec file + three-weakest-points list (human-owned) |
| 3 Decompose | agent receives a spec | questions round-trip, then plan with verification mapping + file manifest | questions report → plan (agent-owned) |
| 4 Build | none — the agent owns the middle | boundary monitors armed (escalate, drift, delegate); see §6 | escalation notes, drift notes |
| 5 Gates | "done?", "ship it", pre-PR | execute Verification literally; proof per item; claimed-vs-verified delta; traceability section | gate evidence report, attached to PR |
| 6 Harvest | pain, surprise, weekly retro, "why does this keep happening" | route each lesson to spec / guideline / skill; prune stale rules; tune tripwires | dated guideline diff in git |
| 7–8 Own read, compare | weekly light, monthly deep; after change bursts; "I've lost the thread" | human writes their unaided read **first**, then steward presents changes by architectural consequence from gg's exhaust | personal perception-gap delta |
| 9 Drift & trends | same session | drift vs. ADRs/charter as direction over time: drift rate, claimed-vs-verified gap, repeat harvests, escalation clustering | trend report |
| 10 Intent refresh | when trends demand it | amend ADRs/charter; revised intent feeds the next spec's context | updated intent documents |

Steps 7–8 work as a pure practice (a markdown template) long before steward is software — which is the required order: the Eddy/steward brief is problem-first, and any tool is downstream proof-of-concept.

**UX decision (decided 2026-06-10):** Auto-triggering skills + `/gg` as explicit fallback. Skills self-select via TRIGGER sections (the superpowers pattern) — the AI pattern-matches from context without the user invoking skills by name. `/gg` is the escape hatch for "I don't know what stage I'm at." TRIGGER sections must cover team vocabulary explicitly ("PM sent me this," "groom this ticket," "is this worth doing," "done?", "ship it") — not just solo-dev phrasing.

## 6. Step 4 hardening (pressure-test results)

**The finding:** as first specced, step 4's monitors fired on internal states — "scope temptation," "feels contrary to an ADR," "same fix attempted twice." That is agent self-assessment as a *stopping* signal, in a system whose axiom is that agent self-assessment is unreliable. The thesis predicts its own step 4 fails, and fails self-servingly.

**The fix principle: trigger on observable acts, not internal states.** You can't hook a temptation, but the temptation becomes a tool call within seconds, and tool calls are hookable.

| Condition (internal state) | Observable proxy | Mechanism |
|---|---|---|
| scope temptation | edit outside the plan's **file manifest**; new dependency; unplanned new file | PreToolUse hook vs. manifest |
| same fix attempted twice | same test/command failing after 2 edit-run cycles; same error class recurring | PostToolUse failure counter keyed by command signature |
| reserved-for-human decision | pre-enumerated: decompose extracts the spec's reserved list into named tripwires in the plan | plan checkpoint; list-match, not semantic recognition |
| spec-named interface touched | edit to a path/symbol on the spec's interface list | PreToolUse hook vs. spec manifest |
| budget threshold | token/cost counter | deterministic |
| guideline conflict; *unanticipated* reserved decisions; missed ambiguity | **no good proxy** — accepted residual | containment via gates (below) |

**The manifest rule:** out-of-manifest edits aren't forbidden — they're illegal *until the plan is revised first*. The hook says "revise the plan, then edit." Plan revision is observable and loggable, re-checks the verification mapping, and forces the tier question at the right moment: a revision serving an existing requirement is within-spec replanning (free, logged); a revision that changes the contract is an escalation. Scope creep stops being a temptation to resist and becomes a door that only opens through the plan.

**Layered defense, ordered by reliability:**

1. Deterministic hooks on the observable proxies above.
2. Plan-embedded checkpoints (drift checks at milestones; reserved-decision tripwires).
3. Sparse, **evidence-demanding** cadence prompts — "list the problems you've attempted more than once this session," never yes/no checklists (retrieval resists pencil-whipping; affirmation doesn't).
4. cctx watch → the human: retry-loop and scope-creep classifiers alert the user on an independent path. Honest limit: requires a human present; fails exactly when escalation matters most (long autonomous runs). Layer rule preserved — gg's hooks consume cctx signals; cctx stays ignorant of gg.
5. **Gates as containment** — the traceability section surfaces orphan changes, so missed escalations degrade from *silent damage* to *caught late*. Caught-late costs rework, which cctx measures, which harvest converts into a sharper tripwire. The system metabolizes its own trigger failures.

**Delegation is enforceable, not honor-system** (verified against Claude Code hooks docs, 2026-06-09): PreToolUse/PostToolUse hooks fire inside subagents (tagged with `agent_id`/`agent_type`); `SubagentStart`/`SubagentStop` events exist; `SubagentStop` can block completion. Therefore: a PreToolUse hook on the Agent tool rejects spawns whose prompt lacks mini-spec structure; the same scope/failure tripwires monitor delegated work; `SubagentStop` can refuse a return without verification-shaped output.

**Open holes, eyes open:**

- *Post-escalation thread parking* — emitting the note and continuing anyway makes the note an alibi. Fix: notes carry open/resolved status; a hook flags edits touching an open escalation's scope; gates refuse work overlapping unresolved escalations.
- *Drift classification gaming* — minor-vs-structural remains partly self-assessed. Mitigation: definitional "structural" where possible; steward's weekly read catches misclassification late; harvest sharpens the definitions.
- *Alert fatigue* — too-tight manifests and trigger-happy counters kill nag systems. Tripwire thresholds live with guidelines and are tuned by harvest.

**Net design change:** step 4 was specced as the agent monitoring itself; it survives pressure-testing only as the *harness* monitoring the agent, with agent self-monitoring demoted to best-effort sugar. The system's own thesis, applied to itself.

## 7. steward — scope notes

- Audience: staff/principal/architect persona and the leaders they report to. The problem is inherently team-scale (code review's sensemaking function); solo dogfood data is the pilot study, not the proof.
- Four required capabilities (inherited from the Eddy brief): live read of what changed; drift measured against stated intent; the human's judgment captured *before* the AI's framing; trends, not snapshots. Concrete trend metrics (GitClear-style, derivable from git history): duplication delta, 30/90-day revert rate, refactor ratio, diff-size-per-fix-size. These are the quantitative spine of step 9 — without named metrics, "trends" stays a wish.
- **Differentiation is judgment and drift, not knowledge capture.** The memory corner is crowded (getlore.tech, get-lore.com, GitLab "LORE" — found 2026-06-09); the existing-tool landscape evaluation in the brief should note this.
- Writing-first: framework document gated on the reading program; evidence caveats from the brief stand (METR perception gap yes, "19% slower" no; GitClear vs. DORA — state both).
- gg artifacts are designed with steward as second reader: drift-note format stable and dated; gate reports carry claimed-vs-verified deltas; guideline changelog is organizational-memory-formation data.

## 8. Standing rules (portfolio-wide)

1. Data flows up; opinions never flow down.
2. Metaphor names things; it never operates them.
3. Artifacts are legible to people who never installed the plugin.
4. A requirement without a gate is a wish.
5. Agent self-assessment is never a completion signal — and (per §6) never a *stopping* signal either; observable acts, not internal states.
6. The spec is the human's contract; the plan is the agent's artifact.
7. Reserved decisions propagate; they are never absorbed downstream.
8. If it needs a server, it's post-1.0.

## 9. Migration & evidence plan

- **superpowers:** nothing deleted on faith. Each gg skill enters rotation after passing skill-creator's eval loop; its counterpart is disabled two weeks; cctx data decides. Caveat recorded: low-frequency/high-consequence skills (escalating) will look dead in usage counts — a fire alarm that never rang isn't useless; retention-test them with injected drills (deliberately ambiguous specs), not usage counts. Before migration starts, produce the one-page table classifying every superpowers skill: replaced-by-gg / demoted-to-guideline / retired-outright / no-counterpart.
- **jaqal:** freeze now (no features, no announcement); `running-gates` wraps its gate commands during dogfood; fold natively at merge; archive with pointer at gg's publish.
- **Evidence:** summer 2026 solo dogfood validates dev→agent; deployment at Bryan's work validates PM→dev (wedge: should-we-build triage on incoming tickets — most self-contained skill, zero team buy-in needed, artifacts get read by real non-users). Publication decisions (~fall) are earned by this data, not scheduled.

## 10. Open items (in order)

1. ~~**Artifact formats**~~ — *complete 2026-06-10*: all six templates in `templates/` (`triage.md`, `questions.md`, `escalation.md`, `mini-spec.md`, `gate-report.md`, `drift-note.md`); worked examples in `examples/specs/06-orchestrator/`. Key rules: triage verdict recorded before rationale is written; mini-spec requires Goal/Verification/Non-goals (hook-enforced); gate claim recorded before gates run; escalation `scope`/`blocks` keys power enforcement hooks; drift `trigger` key audits tripwire fidelity.
2. ~~**`/gg` front door vs. eight triggers**~~ — decided 2026-06-10: Option C (see §4 UX decision).
3. ~~**Gate library wiring**~~ — decided 2026-06-10: (a) `running-gates` executes the spec's Verification section literally — no implicit routing; if an item says "run `/audit`", spawn `/audit` as a subagent with a mini-spec; at native folding those implementations absorb into gg. (b) CI-attestation: `attestation: agent | ci` field in the gate-report frontmatter; `ci` means the Action re-ran the commands independently and produced the report. (c) Redaction: `claimed:` is a verbatim assertion only; Proof column is minimum useful excerpt; nothing from conversation history appears anywhere in the report.
4. ~~**Hook implementation pass**~~ — *complete 2026-06-10*: manifest_check.py (PreToolUse), manifest_updater.py (PostToolUse/Write), failure_counter.py (PostToolUse/Bash), session_start.py (SessionStart); 18 tests passing; docs/install.md. MCP/skills lockfile remains open (gg#3 part 2, separate spike).
5. ~~**superpowers classification table**~~ — complete 2026-06-10: docs/superpowers-classification.md. 1 replaced (writing-plans), 2 demoted-to-guideline (executing-plans, verification-before-completion), 10 retained, 1 retained-with-overlap (subagent-driven-development). Four CLAUDE.md harvests identified before any disables.
6. ~~**steward practice template**~~ — complete 2026-06-10: templates/steward-read.md (light and deep cadences, Parts 1–3, gap-score frontmatter key); worked example at examples/steward/2026-06-15-light.md. Reads live in steward/reads/YYYY-MM-DD-<depth>.md.
7. ~~**Eight boundary skills**~~ — complete 2026-06-10: all eight skills in `skills/`; `/gg` orientation command in `.claude/commands/gg.md`; `tests/test_skill_structure.py`; CLAUDE.md behavioral rules harvested from demoted superpowers skills.

## Next open items

8. **MCP/skills lockfile** (gg#3 part 2): spike to resolve repo-vs-cctx-feature, injection-pattern detection floor, rug-pull blocking UX, and scope (MCP only vs. skills+commands). First milestone: `gg lock` writes hashed manifest; `gg verify` diffs and exits non-zero on drift. Session-start hook does a soft version already; the spike decides whether to harden in-repo or spin separately.
9. **superpowers migration execution**: four CLAUDE.md harvests done (2026-06-10); next is disabling `executing-plans` and `verification-before-completion` after a two-week observation window. `writing-plans` disabled only after `decomposing-specs` passes solo dogfood retention test. Low-frequency skills (`systematic-debugging`, `writing-skills`) retention-tested with injected drills.
10. **Solo dogfood sprint**: use gg end-to-end on a real work item; instrument sessions with cctx; run `tending-guidelines` on findings after ≥3 sessions. Validates the PM→dev wedge with real non-users reading artifacts.

## 11. Reserved for human

Publish/no-publish and timing for gg (fall, evidence-dependent); steward framework publication (after reading program); attaching Bryan's name to steward's README; retiring any superpowers skill; the membership-test verdict on any proposed ninth skill; jaqal archive announcement wording.

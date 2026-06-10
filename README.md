# gg

**Goals-and-guidelines development** — boundary contracts for working with AI agents, instead of process scripts.

gg is a Claude Code plugin (in design) built on one observation: code review used to do two jobs in one ritual — *verification* (is this change correct?) and *sensemaking* (do we still understand the system?). Agent-speed development broke the ritual, and both jobs went unserved. This repo holds the replacements:

- **gg** — the inner loop. Contracts at every handoff: PM→dev, dev→agent, agent→subagent, dev→reviewer. The agent owns the middle; the boundaries are governed and verified.
- **steward** — the outer loop. The staff/principal-engineer practice of keeping your grip on a system that changes faster than you can read: drift against intent, your own read before the AI's, trends over snapshots.

One claim runs through both: **at agent speed, self-assessment fails.** The agent's "it's done" and the developer's "I've still got this" are equally unreliable. Both need an external signal at a boundary. It's not done until gg says gg.

## The shape of it

gg doesn't script *how* to work — no TDD skill, no debugging skill, no plan-execution choreography. The agent owns the middle. gg defines the contracts at the edges:

```
ticket/idea ─► TRIAGE ─► SPEC ─► DECOMPOSE ─► BUILD ─► GATES ─► merged
                 │          │         │           │         │
              verdict    spec +   questions   escalation  evidence
                         red-team  + plan     + drift      report
                 └──────────┴─────────┴─────┬─────┴──────────┘
                                            ▼
                              HARVEST → guidelines (CLAUDE.md)
                                            │
                                            ▼  artifacts in git
                       steward: own read → compare → trends → intent
```

Three rules carry most of the weight:

1. **A requirement without a gate is a wish.** Every spec requirement maps to a verification item; work is done when the gates say so, never when the agent says so.
2. **The spec is the human's contract; the plan is the agent's artifact.** The agent revises its plan freely but can never touch the contract — and scope only expands through explicit plan revision, never silently.
3. **Stopping is governed by observable acts, not good intentions.** Out-of-scope edits, repeated failures, and touched interfaces trip deterministic hooks; the agent's self-restraint is sugar, not the mechanism.

## What's in this repo

| Path | What it is |
|---|---|
| [`DESIGN.md`](DESIGN.md) | The full portfolio design — thesis, workflow, the eight boundary skills, enforcement mechanics, migration plan. **Start here for review.** |
| [`templates/`](templates/) | The four boundary artifacts: questions report, escalation note, gate evidence report, drift note. Conventions in the [README](templates/README.md). |
| [`examples/specs/06-orchestrator/`](examples/specs/06-orchestrator/) | The four artifacts as one continuous worked example. Read in date order: an answered question becomes an architecture rule, a drift check catches its violation, the resulting escalation blocks a gate item, and the gate report catches an overconfident completion claim. |
| [`CLAUDE.md`](CLAUDE.md) | Project boundaries and vocabulary rules. |

## How to use it today

gg is in the design phase — there is no plugin to install yet. But the artifact layer works with zero software, and using it manually is the point of the dogfood period:

1. **Author a spec** for a piece of work: goal, requirements, **verification** (one gate per requirement), **non-goals**, and **reserved-for-human** decisions. Put it in `specs/<NN>-<slug>/spec.md` in your project.
2. **Before any code**, have the agent produce `questions.md` from the template — open questions, reserved decisions it spotted, contradictions. Answer inline. Every question carries a default-if-unanswered, so silence is a logged decision, not a blocker.
3. **During the build**, stopping conditions produce `escalations/NNN-<slug>.md` (open/resolved lifecycle; unblocked work continues) and shape-checks produce `drift/<date>-<slug>.md` (intended shape vs. current shape, two sentences).
4. **Before claiming done**, run the verification section literally and fill `gates/<date>.md` — recording the agent's completion claim *before* the gates run. The claimed-vs-verified gap, accumulated over time, is the dataset that tells you how much to trust "it's done."
5. **Weekly**, harvest: anything that went wrong twice becomes a one-line guideline in CLAUDE.md; anything stale gets pruned.

The frontmatter on every artifact is deliberately machine-readable — dates, classifications, claims vs. verdicts. That's the trend data the outer loop (steward) reads later. Write the artifacts for the person receiving them; the YAML is for the machines.

## Status

Design phase, dogfooding next. The eight skills, enforcement hooks, and gate wiring are specified in DESIGN.md but not yet built. The migration plan retires [superpowers](https://github.com/obra/superpowers) process skills one at a time as evidence supports it, and folds [jaqal](https://github.com/jacquardlabs/jaqal)'s gates in as the verification library. Publication is a fall 2026 decision earned by usage data, not a launch date.

*gg = goals & guidelines. From [Jacquard Labs](https://github.com/jacquardlabs).*

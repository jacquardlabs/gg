# gg

**Goals, guidelines, and gates** — the three things every piece of agentic work needs to answer.

- **Goals** — *what are we building?* A spec with every requirement paired to a verification item. A requirement without a gate is a wish.
- **Guidelines** — *how do we stay on track?* Durable rules in CLAUDE.md, evolved by harvest, enforced by deterministic hooks at every boundary.
- **Gates** — *how do we know it's correct?* The spec's verification section executed literally, the agent's claim recorded before the run, proof attached per item. The agent's "it's done" is not a completion signal.

---

gg is a Claude Code plugin built on one observation: code review used to do two jobs in one ritual — *verification* (is this change correct?) and *sensemaking* (do we still understand the system?). Agent-speed development broke the ritual, and both jobs went unserved. This repo holds the replacements:

- **gg** — the inner loop. Contracts at every handoff: PM→dev, dev→agent, agent→subagent, dev→reviewer. The agent owns the middle; the three Gs govern the boundaries.
- **steward** — the outer loop. The staff/principal-engineer practice of keeping your grip on a system that changes faster than you can read: drift against intent, your own read before the AI's, trends over snapshots.

**At agent speed, self-assessment fails.** The agent's "it's done" and the developer's "I've still got this" are equally unreliable. Both need an external signal at a boundary. It's not done until gg says gg.

## The workflow

```
ticket/idea ─► TRIAGE ─► SPEC ─► DECOMPOSE ─► BUILD ─► GATES ─► merged
                 │          │         │           │         │
              verdict    spec +   questions   escalation  evidence
           [  goals  ]  red-team  + plan     + drift      report
                         └─────────┴──────────┘           [gates]
                [guidelines: CLAUDE.md + hooks watch the middle]
                               ▼
                     HARVEST → CLAUDE.md update
                               │
                               ▼  artifacts in git
            steward: own read → compare → trends → intent refresh
```

Three rules carry most of the weight:

1. **A requirement without a gate is a wish.** Every spec requirement maps to a verification item; work is done when the gates say so, never when the agent says so.
2. **The spec is the human's contract; the plan is the agent's artifact.** The agent revises its plan freely but can never revise the contract — scope only expands through explicit plan revision, never silently.
3. **Stopping is governed by observable acts, not good intentions.** Out-of-scope edits, repeated failures, and touched interfaces trip deterministic hooks; the agent's self-restraint is sugar, not the mechanism.

## What's in this repo

| Path | What it is |
|---|---|
| [`DESIGN.md`](DESIGN.md) | The full portfolio design — thesis, workflow, the eight boundary skills, enforcement mechanics, migration plan. Start here. |
| [`skills/`](skills/) | Eight Claude Code skills, one per boundary: triage, spec, decompose, escalate, gates, harvest, drift, delegate. Plus the [`/gg`](.claude/commands/gg.md) orientation command. |
| [`hooks/`](hooks/) | Four deterministic hooks: manifest check (PreToolUse), manifest updater (PostToolUse/Write), failure counter (PostToolUse/Bash), session start (SessionStart). |
| [`templates/`](templates/) | All seven boundary artifacts as blank templates. Conventions in the [README](templates/README.md). |
| [`examples/`](examples/) | One continuous worked example (`06-orchestrator`). A question becomes an architecture rule; a drift check catches its violation; the gate report records the gap between claim and reality. |
| [`docs/install.md`](docs/install.md) | Install: wire the hooks into `.claude/settings.json`, copy skills to `~/.claude/skills/gg/`. |

## Installing

See [`docs/install.md`](docs/install.md). Two steps: hook settings and skill copy.

The `/gg` slash command gives orientation at any point — it reads your `specs/` directory, determines what stage the work is at, and routes to the right skill.

## How it works in practice

1. **Triage** — ticket arrives; evaluate against product context. Verdict before rationale: BUILD / BUILD-SMALLER / REFRAME / DEFER / DON'T-BUILD.
2. **Spec** — author the contract: goal, requirements, one gate per requirement, non-goals, reserved-for-human decisions. Red-team it (three weakest points) before handing off. The spec is frozen once confirmed.
3. **Decompose** — before any code: questions round-trip (reserved decisions first, ambiguities with explicit defaults), then a plan where every step maps to a requirement. Writing the plan arms the manifest-check hook.
4. **Build** — the agent owns the middle. Hooks watch for out-of-scope edits, repeated failures, and touched interfaces. Stopping conditions escalate; unblocked plan items continue.
5. **Gates** — claim recorded first. Execute the spec's verification section literally, proof per item. Traceability section maps every changed file back to a plan item and requirement. Orphan changes are listed, never implied.
6. **Harvest** — route each pain point to its layer: spec, guideline, or hook threshold. One testable sentence per rule. Prune what never fires.

## Status

Hooks and skills are implemented. The install doc is at [`docs/install.md`](docs/install.md). In dogfood — publication is a fall 2026 decision, earned by usage data.

*From [Jacquard Labs](https://github.com/jacquardlabs).*

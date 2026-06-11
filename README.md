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
| [`agents/`](agents/) | Seven gate agents dispatched by running-gates: security-auditor, code-auditor, doc-auditor, architect-reviewer (coordinator), frontend-reviewer, ux-reviewer, product-reviewer. |
| [`commands/`](commands/) | Four gate commands: [`/gg:gg-init`](commands/gg-init.md) (scaffold PRODUCT.md and specs/), [`/gg:spec-review`](commands/spec-review.md) (independent spec review before decompose), [`/gg:audit`](commands/audit.md) (full parallel audit pass), [`/gg:acceptance`](commands/acceptance.md) (post-implementation product review). |
| [`hooks/`](hooks/) | Four deterministic hooks: manifest check (PreToolUse), manifest updater (PostToolUse/Write), failure counter (PostToolUse/Bash), session start (SessionStart). |
| [`templates/`](templates/) | Artifact templates for every boundary: triage, spec, mini-spec, questions, plan, gate report, escalation, drift note, steward read. Plus [`product.md`](templates/product.md) — the PRODUCT.md scaffold. |
| [`examples/`](examples/) | One continuous worked example (`06-orchestrator`). A question becomes an architecture rule; a drift check catches its violation; the gate report records the gap between claim and reality. |
| [`docs/install.md`](docs/install.md) | Install: one command (`cp -r /path/to/gg ~/.claude/skills/gg`). Skills, commands, and hooks all wired automatically. |

## Installing

See [`docs/install.md`](docs/install.md). Two paths: marketplace install (`/plugin marketplace add jacquardlabs/gg` + `/plugin install gg@gg`) gives `gg:*` namespacing; local copy (`cp -r /path/to/gg ~/.claude/skills/gg`) loads flat names. Both wire hooks automatically.

The `/gg` slash command gives orientation at any point — it reads your `specs/` directory, determines what stage the work is at, and routes to the right skill. Run `/gg:gg-init` (or `/gg-init` with local install) in a new project to scaffold PRODUCT.md and the `specs/` directory.

## How it works in practice

0. **Init** — new project? Run `/gg:gg-init` to scaffold PRODUCT.md and `specs/`. Fill in PRODUCT.md before the first spec-review or acceptance gate — product-reviewer reads it to ground every judgment.
1. **Triage** — ticket arrives; evaluate against product context. Verdict before rationale: BUILD / BUILD-SMALLER / REFRAME / DEFER / DON'T-BUILD.
2. **Spec** — first, pick the path: if the change has a single requirement, no interface changes, and no external users affected, use the mini-spec (goal + requirement + verification + non-goals, five lines, proceed directly to build). Otherwise: author the full contract, red-team it (three weakest points), confirm with the human. For full-ceremony specs, run `/gg:spec-review` before handing off — an independent product-reviewer pass that catches what the author is too close to see.
3. **Decompose** — before any code: questions round-trip (reserved decisions first, ambiguities with explicit defaults), then a plan where every step maps to a requirement. Writing the plan arms the manifest-check hook.
4. **Build** — the agent owns the middle. Hooks watch for out-of-scope edits, repeated failures, and touched interfaces. Stopping conditions escalate; unblocked plan items continue.
5. **Gates** — claim recorded first. Execute the spec's verification section literally, proof per item. Two named standard implementations: `/gg:audit` (seven parallel auditors — security, code, docs, architecture, UX, frontend; frontend/UX skipped when no UI changes) and `/gg:acceptance` (post-implementation product review). Traceability section maps every changed file back to a plan item and requirement. Orphan changes are listed, never implied.
6. **Harvest** — route each pain point to its layer: spec, guideline, or hook threshold. One testable sentence per rule. Prune what never fires.

## Status

Hooks, skills, gate library, and plugin manifest are implemented. Install via `cp -r /path/to/gg ~/.claude/skills/gg` — see [`docs/install.md`](docs/install.md). In dogfood — publication is a fall 2026 decision, earned by usage data.

*From [Jacquard Labs](https://github.com/jacquardlabs).*

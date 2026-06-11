---
name: writing-specs
description: "Use when a ticket, idea, or feature request arrives and needs evaluation or a spec authored. Covers intake triage (should we build this?) and spec authoring (what exactly are we building?). Triggered by PM handoffs, ticket grooming, 'is this worth doing', and 'write a spec for X'."
---

# Writing Specs

Two-phase: first triage (should this be built at all, and at what scope?), then spec (what exactly must it do, verified how?). The triage verdict is written before the rationale — commit to the label, then explain it.

<HARD-GATE>
Do NOT write any code, create any plan, or spawn any agent until a triage verdict exists and (if BUILD-ish) a spec with verification items has been authored and the human has confirmed it.
</HARD-GATE>

## TRIGGER

Invoke this skill when the user's message contains any of:

- a PM or lead sent a ticket, idea, or feature request
- "should we build this", "is this worth doing", "is this a good idea"
- "groom this ticket", "PM sent me this", "ticket from product"
- "spec this out", "write a spec for", "design this"
- "scope this", "what would it take to build", "rough out a spec"
- the work item is new and has no `triage.md` yet

Do NOT trigger for work that already has a triage verdict and an approved spec — that's `decomposing-specs` territory.

---

## Phase 1 — Triage

Goal: produce a clear verdict a non-technical sender can read, in the format defined by `templates/triage.md`.

### Step 1: Read product context

Before evaluating, read:
- `DESIGN.md` (or the nearest product intent document)
- Any existing triage decisions in `specs/*/triage.md`
- The README if product context is thin

You are evaluating against **what the product is trying to be**, not against whether the idea is technically interesting.

### Step 2: State the verdict first

Pick the verdict before writing a word of rationale. The options:

| Verdict | Meaning |
|---|---|
| **BUILD** | Build it as described. Proceeds to spec. |
| **BUILD-SMALLER** | The 80% version is worth building now; the rest is explicitly deferred. Proceeds to spec of the smaller version. |
| **REFRAME** | The underlying need is real; this particular solution is not the right lever. Name the better path. Does not proceed to spec without a new framing. |
| **DEFER** | Worth building; wrong time. Name the preconditions. |
| **DON'T-BUILD** | Not worth building. Plain statement of why. |

**Rule: commit to the verdict label, then write the rationale.** Writing rationale before committing to a verdict lets the analysis drive the conclusion. A verdict written after its rationale is suspect.

### Step 3: Write the triage artifact

File: `specs/<NN>-<slug>/triage.md` (create the directory; assign the next sequential `NN`).

Follow `templates/triage.md` exactly:
- Frontmatter: `type`, `date`, `verdict`, `spec` (omit for DEFER/DON'T-BUILD)
- Body opens with the verdict in bold
- Rationale is two to four sentences — plain English, no gg vocabulary
- Conditional sections per verdict (see template comments)
- Closes with "Proceeds to spec: yes / no"

The body is for the sender. A PM reading this needs zero knowledge of gg.

### Step 4: Present and confirm

Show the triage artifact to the human and wait for confirmation before proceeding to Phase 2. If the human redirects the verdict, update the artifact and confirm again.

For DEFER and DON'T-BUILD: skill ends here.

---

## Phase 2 — Spec

Only reached after a BUILD or BUILD-SMALLER verdict is confirmed.

Goal: produce a spec the human owns, every requirement paired with a gate, that an agent can execute without ambiguity. The spec is the human's contract — it is not revisable by the agent.

### Path determination (do this first)

**Full-ceremony path** applies when any of the following are true:
- The spec has more than one requirement
- Any interface changes (public functions, API endpoints, data schemas, file paths)
- External users are affected

**Mini-spec path** applies when none of the above are true — a single-requirement change with no interface impact and no external users affected. The mini-spec omits the questions round-trip, the red-team pass, and the full plan; gates are a spot check.

**The path choice is always recorded.** State it in the spec frontmatter (`path: full` or `path: mini`) and in one line at the top of the body. Silent downgrade is not permitted — it defeats the traceability section.

---

### Mini-spec path (below-threshold changes)

If the mini-spec path applies, skip to this section. Skip Steps 1–4 below.

Write `specs/<NN>-<slug>/spec.md` with five lines:

```
Goal: <one sentence — what the work produces and for whom>
Requirement: <one requirement>
Verification: <exact gate that proves the requirement met>
Non-goals: <what this explicitly does not do>
Path: mini-spec
```

Present to the human; wait for confirmation. No questions round-trip. No red-team pass. No spec-review gate.

Proceed directly to build. Plan is a single-item list in the agent's working notes, not a `plan.md` file. Gates are a spot check: run only the one Verification gate, record the result, attach as the gate evidence.

---

### Step 1: Collect requirements

Ask for any requirements not already clear from the ticket. One round of questions is fine; this is not a design session. If the requirements are already clear, skip to Step 2.

Focus on:
- What outcome the user needs (not what solution to build)
- What the hard constraints are (performance, compatibility, scope)
- What "done" looks like to them

### Step 2: Draft the spec

File: `specs/<NN>-<slug>/spec.md`.

Required sections:

**Goal** — one sentence. What the work produces and for whom. A measurable outcome, not an activity.

**Requirements** — numbered list. Each requirement is specific enough to be tested. Vague requirements ("it should be fast") become untestable gates — push back and sharpen them here.

**Verification** — one gate per requirement, listed in the same order. Each gate names the exact test, command, observation, or artifact that proves the requirement met. Format:

```
| R# | Requirement | Gate |
|----|-------------|------|
| R1 | <requirement text> | <exact verification> |
```

A requirement without a gate is a wish. Do not leave this column blank.

**Non-goals** — what this work explicitly does not do. At least two items. Non-goals prevent scope creep from looking like good judgment.

**Reserved for human** — decisions the agent cannot make during build. These propagate to every sub-delegation. Examples: architecture choices, API contracts with external teams, decisions that affect the product beyond this work item.

**Interfaces** — public surfaces this work touches or creates (function signatures, API endpoints, data schemas, file paths). Listed here so drift checks have a named list to diff against.

### Step 3: Red-team pass

After drafting, read the spec once with an adversarial eye. Name the **three weakest points** in a `## Weaknesses` section at the end:

1. The requirement most likely to be misunderstood by an agent
2. The gate most likely to pass on a wrong implementation
3. The non-goal most likely to be violated under time pressure

Do not soften these. The point is to surface the risks so the human can tighten the spec before handing it off, not to reassure them that the spec is fine.

### Step 4: Human review gate

Present the spec to the human. Wait for explicit confirmation before this skill ends.

If the human requests changes: make them, re-run the red-team pass, and re-present. Repeat until the human confirms.

Once confirmed: the spec is frozen from the agent's perspective.

**Spec-review gate (recommended before decompose).** For full-ceremony specs (multiple requirements, any interface changes, or external users affected), run `/spec-review` now. It runs product-reviewer independently against the spec — the author's red-team and the independent review are different passes. Verdict REVISE loops back here to update and re-confirm; verdict RETHINK routes back to triage; verdict PROCEED TO PLAN clears the spec for decompose. Skip spec-review on the mini-spec path (below-threshold changes) when no PRODUCT.md exists or when the human explicitly waives it.

---

## Output artifacts

| Artifact | Path | Who owns it |
|---|---|---|
| Triage verdict | `specs/<NN>-<slug>/triage.md` | human (sender reads it) |
| Spec | `specs/<NN>-<slug>/spec.md` | human (agent executes against it) |

Both artifacts go in git. The triage verdict is the PM's answer; the spec is the agent's contract.

---

## Rules

- Verdict before rationale. Always.
- Every requirement has a gate. No exceptions.
- Non-goals: at least two. If you can't name two, the scope is probably underspecified.
- Reserved decisions propagate — they are never absorbed by the agent or a sub-delegation.
- The red-team pass is not optional and is not a summary of the spec. It names specific failure modes.
- Plain English throughout. The recipient of the triage artifact has never heard of gg.
- Path choice is always recorded. Mini-spec path for below-threshold changes; full ceremony for everything else. No silent downgrade.

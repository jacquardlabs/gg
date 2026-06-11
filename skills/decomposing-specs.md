---
name: decomposing-specs
description: "The agent's mandatory first move on receiving a spec. Surfaces reserved decisions, ambiguities, and contradictions before any code; then produces a plan where every step maps to a spec requirement, plus a file manifest that the manifest_check hook enforces. Triggered by receiving a spec, 'start on this', 'work from this spec', 'implement this'."
---

# Decomposing Specs

Two phases, strict order: questions first, plan second. No code is written until the questions round-trip completes and the plan exists.

<HARD-GATE>
Do NOT write any code, edit any files, or run any build commands before:
1. A questions report exists and all reserved decisions are resolved (or explicitly acknowledged as proceeding with default)
2. A plan exists with a complete verification mapping and a manifest block
</HARD-GATE>

## TRIGGER

Invoke this skill when:

- you have received a spec and are about to start work
- the user says "start on this", "work on this", "implement this", "build it"
- the user hands off a spec file and says go
- there is a `spec.md` in the work item directory but no `plan.md`

Do NOT trigger if a plan with a manifest already exists and the questions are answered — that's the build phase. Do NOT trigger if you are mid-build and need to revise the plan — revise the plan directly and re-check the verification mapping.

---

## Phase 1 — Questions

Goal: produce a `questions.md` the human can answer by number, then wait for answers before writing a single line of code.

### Step 0: Check for spec-review

Read `specs/<NN>-<slug>/spec-review.md` if it exists. A PROCEED TO PLAN verdict means the spec cleared independent review — proceed. If it's absent, note it: "spec-review not run — skipping is valid for below-threshold changes; flag if this is a full-ceremony spec." Do not block.

### Step 1: Read the spec completely

Read `specs/<NN>-<slug>/spec.md` from top to bottom before forming any questions. Also read:
- `DESIGN.md` or the nearest product intent document (context for reserved decisions)
- Any prior questions reports in this work item (don't re-ask answered questions)

### Step 2: Extract and classify every uncertainty

Walk through the spec and pull out:

**Reserved decisions** — items the spec's "Reserved for human" section lists explicitly, or decisions that meet any of these criteria:
- Affects public interfaces or API contracts
- Has implications beyond this work item
- Involves a tradeoff the human should own (cost, architecture choice, external dependency)
- You could implement it either way and both are reasonable

Reserved decisions go first in the questions report. They are the only true blockers — the human must answer them before work can begin on the parts they affect.

**Open ambiguities** — requirements that could be interpreted two ways, gates that don't specify how to measure, terms used without definition. For each, state what your default would be if the human doesn't answer. Silence becomes a logged decision, not a blocker.

**Contradictions** — places where two requirements conflict, or a requirement contradicts a non-goal. State both sides and ask which wins. If you have a clear recommendation, say so.

Do not ask questions you can answer by reading the spec or the codebase. Do not ask permission for implementation details the spec already decides. Ask only when genuine ambiguity exists.

### Step 3: Write the questions report

File: `specs/<NN>-<slug>/questions.md`.

Follow `templates/questions.md` exactly:
- Frontmatter: `type: questions`, `spec`, `date`, `status: awaiting-answers`
- Numbered throughout so answers can be given by number
- Reserved decisions first
- Each open question states its default explicitly ("If unanswered I will X, and that becomes the gate")
- Contradictions last

### Step 4: Present and wait

Show the questions report. Do not proceed until the human responds.

When answers arrive:
- Fill in the `→ answer:` lines in the file
- Flip `status` to `answered`
- Note any answers that change the spec's intent — if an answer changes what's being built, flag it to the human before proceeding. The spec is the human's contract and is not revisable by the agent. An answer that contradicts the spec requires the human to update the spec first.

If the human says to proceed with defaults: fill defaults in as answers, set status to `answered`, note which questions went to default.

---

## Phase 2 — Plan

Only reached after `questions.md` has `status: answered` and all reserved decisions are resolved.

Goal: produce a `plan.md` where every step maps to a spec requirement, and a file manifest that the manifest_check hook will enforce.

### Step 1: Draft the plan steps

Map the spec's requirements to concrete build steps. Rules:
- Every plan item maps to at least one spec requirement (R-number)
- Every spec requirement maps to at least one plan item
- A plan item with no requirement is out-of-scope — either it serves an existing requirement and you mislabeled it, or it's scope creep. Label it and confirm with the human before proceeding.

Order steps by dependency: earlier steps should not depend on later ones. Group steps that share a file boundary.

### Step 2: Build the verification mapping

Produce the table from `templates/plan.md`:

```
| Plan item | Requirement | Verification |
|---|---|---|
| P1: <name> | R1 | V1 |
```

The Verification column references the exact gate from the spec's Verification table. A plan item that touches no gate is a signal — either the requirement it serves has no gate (go back to the spec and flag it) or the plan item is out-of-scope.

### Step 3: Build the file manifest

List every file the plan will edit, create, or delete. Be specific — per-file, not per-directory. Include:
- Files you will edit
- Files you will create (even if they don't exist yet)
- Files you will delete or move

The manifest enforces the plan's scope. The `manifest_check` hook blocks edits to files not on this list until the plan is revised. This is the mechanism by which out-of-scope edits become visible rather than silent.

**Accuracy matters more than completeness at this stage.** It is better to add a file during a plan revision (observable, logged) than to list speculative files that never get touched (the manifest loses meaning). List what you actually expect to edit.

### Step 4: Write the plan file

File: `specs/<NN>-<slug>/plan.md`.

Follow `templates/plan.md` exactly, including the fenced manifest block:

~~~
```manifest
path/to/file.py
path/to/other.py
```
~~~

Writing this file triggers `manifest_updater.py`, which parses the manifest block and writes `.gg/state/manifest.txt`. From this point forward, edits to files outside the manifest are blocked until the plan is revised.

### Step 5: Present and confirm

Show the plan to the human. Wait for confirmation before writing any code.

The human may:
- Approve: proceed to the build phase
- Request changes: make them, re-check the verification mapping, rewrite the manifest, re-present
- Flag scope issues: any item the human questions should be mapped back to a requirement before proceeding

---

## Plan revision rules

The plan is the agent's artifact and is freely revisable. But every revision must:

1. **Re-check the verification mapping** — does the changed step still map to the same requirement? Does the revision orphan any requirement?
2. **Regenerate the manifest** — if new files are needed, add them to the manifest before editing them. Writing a revised `plan.md` automatically updates the hook's manifest.
3. **Classify the revision** — there are two kinds:
   - *Within-spec replanning*: adds or changes steps to serve an existing requirement more effectively. Free. Log it with a one-line note in the plan file.
   - *Contract change*: the revision changes what's being built (drops a requirement, changes an interface, adds new scope). This is an escalation — surface it to the human; do not absorb it into the plan silently.

A revision that changes the spec's intent is the human's decision, not the agent's. Surface it.

---

## Output artifacts

| Artifact | Path | Who owns it |
|---|---|---|
| Questions report | `specs/<NN>-<slug>/questions.md` | human fills answers; agent writes the questions |
| Plan | `specs/<NN>-<slug>/plan.md` | agent — freely revisable, never frozen |

The spec file (`spec.md`) is read-only from the agent's perspective. It is the human's contract and does not change during the build unless the human explicitly revises it.

---

## Rules

- No code before the questions round-trip. Zero exceptions.
- No code before the plan exists with a verification mapping and a manifest.
- Reserved decisions go first in questions — they are the only true blockers.
- Every plan item maps to a requirement. Orphan items are scope signals.
- The manifest is specific: files, not directories. Accuracy over speculative completeness.
- Plan revisions that change the contract → escalate. Plan revisions that change the approach → free.
- The spec is the human's contract and cannot be revised by the agent.

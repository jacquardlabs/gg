---
name: checking-drift
description: "Use at milestones, before tagging a release, after a large refactor, when a spec-named interface is touched, or when something feels structurally off. Compares built structure against the spec's interfaces and ADRs; classifies drift as none/minor/structural; structural drift halts the thread and escalates."
---

# Checking Drift

Drift is not a bug — it is a plan revision that didn't go through the plan. The purpose of this skill is to make drift visible at the moment it's cheapest to address, rather than discovering it at the gate or at the next code review.

## TRIGGER

Invoke this skill when:

- a milestone in the plan is reached (plan item marked complete)
- before tagging a release, merging to main, or calling a spec done
- an edit would touch a path or symbol on the spec's Interfaces list
- a large refactor, file move, or rename is completed
- something feels structurally different from what the spec describes
- `checking-drift` appears in the plan's verification mapping for a step

Do NOT trigger for every edit. This is a milestone and boundary check, not a per-commit review.

---

## What drift means

Drift is a difference between the **intended shape** (the spec's Interfaces section and any referenced ADRs) and the **current shape** (what the codebase actually implements). Shape is expressed in terms of components and the direction of dependencies — not line counts or code style.

**Drift is not always bad.** A plan revision that changed the approach while keeping the spec's interfaces intact is not drift. A refinement that stays within the spec's non-goals is not drift. Drift is a deviation from the contract, not a deviation from the original approach.

---

## Classification

Classify every diff between intended and current shape. Three categories:

**None.** The current shape matches the spec's interfaces and ADRs. State this explicitly: "No drift from spec §Interfaces and ADR-X."

**Minor.** The diff is real but does not change the spec's named interfaces or violate any ADR. Examples: internal refactor that keeps the public API intact, a private component renamed, an implementation detail changed without touching any interface on the spec's list.

Minor drift does not halt the thread. Write the note and continue.

**Structural.** The diff touches a public interface, violates an ADR, or changes a contract — the spec's named components, their dependencies, or the direction of those dependencies.

Structural drift **halts this thread** immediately and generates an escalation. It does not proceed; it does not continue in parallel.

**The classification test (apply in order):**

1. Does this change a path or symbol on the spec's Interfaces list? → **Structural** (definitional)
2. Does this contradict an ADR referenced in the spec? → **Structural** (definitional; ADR contradictions always escalate, no judgment applied)
3. Does this change a public-facing signature, endpoint, schema, or contract? → **Structural** (definitional)
4. Everything else → **Minor or None**

Steps 1–3 are definitional: if any applies, the classification is structural without further judgment. The definitional criteria exist to resist self-serving classification ("it's just a minor change") — if the spec named it, it is structural.

---

## Running a drift check

**Step 1: Read the spec's Interfaces section completely.**

The Interfaces section is the canonical list of what the spec owns. Every named path, function, endpoint, schema, and component is a potential structural drift point.

**Step 2: Read any referenced ADRs.**

ADRs record decisions the team has committed to. An implementation that contradicts an ADR contradicts a decision, not just a document.

**Step 3: Compare current state to the intended shape.**

For each Interface item:
- Does the current implementation match the spec's description?
- Has the direction of dependencies changed (e.g., X used to call Y; now Y calls X)?
- Are there new dependencies the spec didn't account for?

This is a structural comparison, not a code review. You are asking: does the shape of this component match its intended role?

**Step 4: Write the drift note (even for none).**

File: `specs/<NN>-<slug>/drift/<YYYY-MM-DD>-<slug>.md`.

Follow `templates/drift-note.md` exactly:
- `classification`: none / minor / structural
- `trigger`: milestone / interface-touch / refactor / adr-conflict / requested
- `escalation`: REQUIRED when structural or adr-conflict; omit otherwise

The body is two sentences:
- **Intended shape:** the intended structure from the spec — components and dependency directions, not code
- **Current shape:** what actually exists, one sentence, with the plan item that introduced it

Classification is stated with the rule that applies. Definitional rules are cited as such ("touches an interface named in the spec"). Judgment-based classifications say so explicitly.

**Action** line: none / note only / thread halted; escalation NNN.

---

## On structural drift

When structural drift is found:

1. Write the drift note immediately, before anything else on this thread
2. Halt this thread — do not continue implementing
3. Generate an escalation (`escalating` skill): situation = the drift found, options = (a) revise the spec to match the implementation, (b) revert to the intended shape
4. Continue on unblocked plan items per the escalation rules

The human decides whether to revise the spec or revert the implementation. The agent does not absorb this decision.

**Do not reclassify structural drift as minor to avoid an escalation.** The drift note's `trigger` key exists precisely to catch this: if structural drift only ever arrives via `requested` (human explicitly asked for a drift check) and never via `interface-touch` (automatic tripwire), the automatic tripwires are not firing — that's a steward signal, and it means the classification is being gamed.

---

## Output artifact

| Artifact | Path | Notes |
|---|---|---|
| Drift note | `specs/<NN>-<slug>/drift/<YYYY-MM-DD>-<slug>.md` | Written even for `none`; steward reads the aggregate |

Drift notes stay in git. They are steward's primary input for measuring architectural coherence over time, and they are future training data for the definitions. An unwritten drift note is a coverage gap in both.

---

## Rules

- Classify using the definitional criteria first. Judgment is a last resort, not a default.
- Structural drift halts the thread. No exceptions.
- ADR contradictions are always structural. No judgment applied.
- Write the note even when the answer is "none." A clean bill of structural health is as valuable as a finding.
- The `trigger` key is an audit trail for the tripwires themselves. Use it accurately.
- The human decides whether to revise the spec or revert. The agent never absorbs that decision.

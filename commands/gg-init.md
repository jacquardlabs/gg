---
description: Initialize gg in this project — scaffold PRODUCT.md and specs/, add a gg workflow section to CLAUDE.md. Safe to re-run; checks before creating each artifact.
allowed-tools: Read, Write, Bash
---

Initialize gg in this project. Work through the three scaffolding steps below in order. Each step checks before acting — this command is safe to re-run.

## Step 1: PRODUCT.md

Check whether `PRODUCT.md` exists at the project root.

**If it exists:** read it and note "PRODUCT.md already exists — skipping."

**If it doesn't exist:** create `PRODUCT.md` with the following content:

```markdown
# Product: [Product Name]

## One-liner

[One sentence: what this product does and who it's for.]

## Users

<!-- Name 2–4 personas. Each line: bold name — who they are and what they need.
     product-reviewer grounds every judgment in these personas. -->

**[Persona]** — [who they are; what problem this product solves for them]

## Product principles

<!-- 3–5 "when in doubt, do X" rules that govern design decisions.
     Concrete beats abstract: "speed over completeness — a fast rough answer
     beats a slow complete one" is a principle; "be fast" is not.
     product-reviewer checks every design and implementation against these. -->

1. [Principle — what and why]

## Critical user journeys

<!-- 3–5 journeys a user must be able to complete without friction.
     Format: **Journey name**: what the user wants to do → key steps → success state.
     These are the regression tests for every new feature:
     product-reviewer walks each one mentally after implementation. -->

**[Journey]**: [goal] → [steps] → [success: what does done look like to the user]

## What we are not building

<!-- At least 2 explicit scope boundaries.
     Non-goals prevent scope creep from looking like good judgment.
     State what we're deliberately NOT doing, and briefly why. -->

- [Non-goal — and why it's out of scope]
- [Non-goal — and why it's out of scope]
```

Note "Created PRODUCT.md — fill in the template before running spec-review or acceptance gates."

## Step 2: specs/ directory

Check whether the `specs/` directory exists.

**If it exists:** note "specs/ already exists — skipping."

**If it doesn't exist:** run `mkdir -p specs && touch specs/.gitkeep`, then note "Created specs/."

## Step 3: CLAUDE.md

Search for an existing gg workflow section. Check both `CLAUDE.md` (project root) and `.claude/CLAUDE.md` for a heading containing "gg" (case-insensitive: `## Using gg`, `## gg workflow`, `# gg`, etc.).

**If a gg section already exists:** note "CLAUDE.md already has a gg section — skipping."

**If no gg section exists:** append the following to `.claude/CLAUDE.md` (create the file if it doesn't exist):

```markdown

## Using gg

This project uses gg for inner-loop verification. Workflow:

1. **Triage** — evaluate incoming work: "should we build this?" Skill: `gg:writing-specs`.
2. **Spec** — author the contract; every requirement paired with a verification gate.
3. **Decompose** — questions round-trip, then a plan with file manifest. Skill: `gg:decomposing-specs`.
4. **Build** — hooks enforce the manifest; stopping conditions escalate.
5. **Gates** — `/gg:audit` (7 parallel auditors), `/gg:acceptance` (product review). Skill: `gg:running-gates`.
6. **Harvest** — route pain points to specs, guidelines, or hook thresholds. Skill: `gg:tending-guidelines`.

Run `/gg` at any point to orient.
```

Note "Added gg workflow section to .claude/CLAUDE.md."

## Final report

Output a 3-line summary:

```
PRODUCT.md:  [created | already exists]
specs/:       [created | already exists]
CLAUDE.md:   [gg section added | already present]
```

If PRODUCT.md was just created: remind the user to fill in the template — particularly Users, Product principles, and Critical user journeys — before running `/gg:spec-review` or `/gg:acceptance` gates, since product-reviewer reads these to ground its judgments.

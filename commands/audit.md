---
description: Full audit pass — security, code, docs, architecture, UX, frontend (7 parallel auditors). Returns PASS / FIX AND RE-AUDIT / NEEDS DISCUSSION.
allowed-tools: Read, Glob, Grep, Bash, Task
---

# Audit

Run the full gate-agent audit pass against the current changeset. This is one of the two standard verification implementations in the gg gate library.

Read CLAUDE.md, PRODUCT.md (if present), and DESIGN.md before proceeding.

## Invoke architect-reviewer

Spawn `architect-reviewer` as a subagent. It will:

1. Identify which of the seven gate agents apply (frontend-reviewer and ux-reviewer are skipped when no UI changes are present).
2. Spawn all relevant agents in parallel.
3. Return a compiled report with cross-referenced findings.

Agents available: security-auditor, code-auditor, doc-auditor, architect-reviewer (as coordinator), frontend-reviewer, ux-reviewer, product-reviewer.

## After architect-reviewer returns

Record the compiled report as the gate evidence for this audit item. The overall verdict from architect-reviewer (PASS / FIX AND RE-AUDIT / NEEDS DISCUSSION) is the gate verdict.

**PASS**: No Critical or High findings. Proceed to the next gate item.

**FIX AND RE-AUDIT**: One or more Critical or High findings. Do NOT edit code to fix them mid-run. Record the findings, finish the full gate run, then route each finding to its plan item. Re-run `/audit` after fixes.

**NEEDS DISCUSSION**: Findings that require human judgment. Record them; do not block the gate run. Surface in the route section.

## What this gate does NOT do

- Fix code. Finding → plan item → fix after the run.
- Replace the spec's verification items. If the spec says "run `pytest tests/`", run `pytest tests/`. `/audit` is one named item among others.

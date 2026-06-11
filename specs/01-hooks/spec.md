---
type: spec
slug: 01-hooks
date: 2026-06-10
status: open
owner: human
---
# Hook implementation — §6 tripwires

Ship the three core PreToolUse/PostToolUse/SessionStart hooks that enforce
gg's §6 observable-act tripwires during dogfood sessions. The hooks ship
as scripts in the gg repo; users wire them via `.claude/settings.json`.

## Requirements

**R1.** A PreToolUse hook fires on Edit / Write / MultiEdit and blocks the
tool call if the target file is not in the active plan's file manifest,
emitting: "Not in plan manifest. Revise the plan first, then edit."

**R2.** The manifest check allows the edit immediately if a plan revision
(a write to `plan.md`) has occurred since the manifest was last read —
so the revision door opens before the edit, not after.

**R3.** A PostToolUse hook fires on Bash and increments a per-command
failure counter. When the same command signature fails N consecutive
times (default: 2), it emits a warning with the failure count and the
command; it does not block.

**R4.** A SessionStart hook starts `cctx watch` if cctx is installed, and
records a purpose tag (from the `GG_PURPOSE` environment variable if set,
otherwise a one-line prompt). Degrades gracefully when cctx is absent.

**R5.** All three hooks read state from and write state to a `.gg/state/`
directory in the project root. State files are plain JSON; not committed.

**R6.** Installing the hooks requires a single documented step: add a
known JSON block to `.claude/settings.json`. No other setup.

## Verification

V1. Given a plan.md with a file manifest, an Edit targeting a file not in
    the manifest exits non-zero and prints the "revise first" message.
    `pytest tests/test_manifest_check.py`

V2. Given a plan revision (write to plan.md) followed immediately by an
    Edit to a new file, the Edit is allowed.
    `pytest tests/test_manifest_check.py::test_revision_unlocks_edit`

V3. Given the same Bash command failing twice consecutively, the
    PostToolUse hook emits the warning with count=2 and exits 0.
    `pytest tests/test_failure_counter.py`

V4. SessionStart hook: when cctx is absent, exits 0 with no error.
    `pytest tests/test_session_start.py::test_degrades_without_cctx`

V5. SessionStart hook: when GG_PURPOSE is set, records the value without
    prompting. `pytest tests/test_session_start.py::test_purpose_from_env`

V6. `docs/install.md` describes adding the hook config block to
    `.claude/settings.json`. Manual check: follow the instructions on a
    clean project, verify hooks fire.

## Interfaces

- **Input to manifest_check**: Claude Code PreToolUse hook JSON via stdin
  (contains `tool_name`, `tool_input` with `path`).
- **Input to failure_counter**: Claude Code PostToolUse hook JSON via
  stdin (contains `tool_name`, `tool_input`, `tool_response`).
- **State files**: `.gg/state/manifest.json` (current plan manifest),
  `.gg/state/failure_counts.json` (counter map).
- **Plan manifest location**: parsed from `plan.md` in the active spec
  dir (format: TBD — see open question Q1).

## Non-goals

- MCP/skills lockfile (separate spike, gg#3 part 2).
- Budget threshold counter (deferred until cctx token data is available).
- Reserved-decision tripwires (require decomposing-specs output; deferred
  until that skill exists).
- Windows support.

## Reserved for human

- Plan manifest format in plan.md (Q1 — blocks implementation).
- Failure counter threshold N (Q2).
- Whether session_start blocks on missing GG_PURPOSE or silently skips (Q3).

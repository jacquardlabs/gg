# Installing gg hooks

One step: add the following block to your project's `.claude/settings.json`.
Replace `/path/to/gg` with the absolute path to where you cloned this repo.

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write|MultiEdit",
        "hooks": [
          {
            "type": "command",
            "command": "python3 /path/to/gg/hooks/manifest_check.py"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "python3 /path/to/gg/hooks/manifest_updater.py"
          }
        ]
      },
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python3 /path/to/gg/hooks/failure_counter.py"
          }
        ]
      }
    ],
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 /path/to/gg/hooks/session_start.py"
          }
        ]
      }
    ]
  }
}
```

## Verifying installation

Start a new Claude Code session in your project. You should see:

```
gg: what's the goal of this session? (one line) >
```

If `GG_PURPOSE` is set in your environment, the prompt is skipped and
the value is recorded automatically.

## Setting an active manifest

Before starting work on a spec, write a `plan.md` with a `manifest` block
(see `templates/plan.md`). The hooks activate as soon as `plan.md` is
written — no other setup needed.

To skip manifest enforcement for a session (e.g. exploratory work with no
active spec), omit or leave `plan.md` without a manifest block. The check
hook allows all edits when no manifest is present.

## Optional: GG_PURPOSE

Set this in your shell profile to skip the purpose prompt:

```sh
export GG_PURPOSE="your default session intent"
```

Or set it per-session before launching Claude Code:

```sh
GG_PURPOSE="implement auth refactor" claude
```

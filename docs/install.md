# Installing gg

## Plugin install (recommended)

Copy the full gg repo to your global Claude Code skills directory:

```sh
cp -r /path/to/gg ~/.claude/skills/gg
```

That one command installs everything:

- **Skills** — available as `gg:writing-specs`, `gg:running-gates`, etc. in any Claude Code session
- **Gate commands** — `/gg:audit`, `/gg:acceptance`, `/gg:spec-review`, `/gg:gg-init`
- **Hooks** — auto-wired via `hooks/hooks.json`; `${CLAUDE_PLUGIN_ROOT}` resolves to the install path, so no absolute-path editing required

To update after pulling a new gg version:

```sh
cp -r /path/to/gg ~/.claude/skills/gg
```

---

## Verifying installation

Start a new Claude Code session in your project. You should see:

```
gg: what's the goal of this session? (one line) >
```

If `GG_PURPOSE` is set in your environment, the prompt is skipped and the value is recorded automatically.

Run `/gg` at any point to orient — it reads your `specs/` directory, determines what stage the work is at, and routes to the right skill.

---

## Setting an active manifest

Before starting work on a spec, write a `plan.md` with a `manifest` block (see `templates/plan.md`). The hooks activate as soon as `plan.md` is written — no other setup needed.

To skip manifest enforcement for a session (e.g. exploratory work with no active spec), omit or leave `plan.md` without a manifest block. The check hook allows all edits when no manifest is present.

---

## Optional: GG_PURPOSE

Set this in your shell profile to skip the purpose prompt:

```sh
export GG_PURPOSE="your default session intent"
```

Or set it per-session before launching Claude Code:

```sh
GG_PURPOSE="implement auth refactor" claude
```

---

## Manual install (skills only, without plugin hooks)

If you prefer to install only the skills without the hook wiring:

```sh
cp -r /path/to/gg/skills/. ~/.claude/skills/gg/
```

Then wire the hooks manually. Add this block to your project's `.claude/settings.json`,
replacing `/path/to/gg` with the absolute path to where you cloned the repo:

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

With the skills-only install, gate commands (`/gg:audit` etc.) are not available — you will need to invoke the gate agents directly or adapt the verification section of your specs.

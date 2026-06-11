# Installing gg

Two install paths. The difference is naming: marketplace install namespaces everything as `gg:*`; local copy loads names flat.

## From GitHub (marketplace install — recommended)

```
/plugin marketplace add jacquardlabs/gg
/plugin install gg@gg
```

Skills load as `gg:writing-specs`, `gg:running-gates`, etc. Gate commands are `/gg:audit`, `/gg:acceptance`, `/gg:spec-review`, `/gg:gg-init`. Hooks auto-wired. This matches all command references in the skills.

## Local install (skills-dir copy)

```sh
cp -r /path/to/gg ~/.claude/skills/gg
```

Skills and commands load with flat names — `writing-specs`, `/audit`, `/gg-init`, `/spec-review`. Hooks auto-wire. Use this path when you need a local clone (active development, no internet access, or iterating on skills themselves).

**With the local install**, anywhere the skills say `/gg:audit` or `gg:running-gates`, drop the `gg:` prefix: `/audit`, `running-gates`, etc.

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

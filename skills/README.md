# gg skills

Eight boundary skills for Claude Code. Each skill governs the protocol at a
handoff point — what to do, when to do it, and what to produce.

Install to `~/.claude/skills/gg/` (see `../docs/install.md`).

| Skill | Trigger | Produces |
|---|---|---|
| `writing-specs` | ticket or idea arrives; "should we build this" | triage verdict + spec |
| `decomposing-specs` | agent receives a spec | questions report + plan |
| `escalating` | stopping condition fires | escalation note |
| `running-gates` | "done?", pre-PR | gate evidence report |
| `tending-guidelines` | repeating failure; "why does this keep happening" | dated guideline diff |
| `instrumenting-sessions` | session start/end | session record + harvest candidates |
| `checking-drift` | milestone, large refactor, ADR touch | drift note |
| `delegating-with-specs` | spawning a subagent | mini-spec; verified on return |

Skills 3–8 are not yet written. `writing-specs` and `decomposing-specs` are done.

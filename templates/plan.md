---
type: plan
spec: <NN>-<slug>
date: <YYYY-MM-DD>
status: <in-progress | complete>
---
# Plan

## Verification mapping

| Plan item | Requirement | Verification |
|---|---|---|
| P1: <name> | <RN> | <VN or — > |

<!--
Every plan item maps to at least one spec requirement.
Every spec requirement maps to at least one plan item.
A plan item with no requirement is a scope signal — route to spec revision
or escalation before proceeding.
-->

## Steps

1. (P1) <what to build — one line>
2. (P2) ...

```manifest
# Files this plan may edit. One path per line, relative to the git root.
# The manifest_check hook enforces this list.
# Add a file here BEFORE editing it. Doing so is a plan revision — update
# the verification mapping if the change affects any requirement.
path/to/file.py
```

<!--
The manifest block is parsed by hooks/manifest_updater.py each time
plan.md is written. Edits to files outside this list are blocked by
hooks/manifest_check.py until the manifest is updated.

A manifest revision that changes requirements → escalate.
A manifest revision that adds files to serve an existing requirement → free.
-->

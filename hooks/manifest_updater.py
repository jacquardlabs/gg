#!/usr/bin/env python3
"""
PostToolUse hook (Write) — re-parse the manifest block from plan.md
after a plan revision and update .gg/state/manifest.txt.

Runs silently on success. Prints a warning if plan.md was written but
contains no manifest block (the agent may have forgotten to include one).
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import find_git_root, normalize_path, read_hook_input, state_dir

PLAN_PATTERN = re.compile(r"[/\\]plan\.md$")
MANIFEST_BLOCK = re.compile(r"```manifest\n(.*?)```", re.DOTALL)


def parse_manifest_block(content: str) -> list[str]:
    match = MANIFEST_BLOCK.search(content)
    if not match:
        return []
    return [
        line.strip()
        for line in match.group(1).splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]


def main() -> None:
    data = read_hook_input()
    tool_input = data.get("tool_input", {})
    file_path = tool_input.get("file_path") or tool_input.get("path", "")

    if not file_path or not PLAN_PATTERN.search(file_path):
        sys.exit(0)

    git_root = find_git_root(Path.cwd())
    if not git_root:
        sys.exit(0)

    plan_path = Path(file_path)
    if not plan_path.is_absolute():
        plan_path = git_root / plan_path

    if not plan_path.exists():
        sys.exit(0)

    entries = parse_manifest_block(plan_path.read_text())

    manifest_file = state_dir(git_root) / "manifest.txt"
    if entries:
        manifest_file.write_text("\n".join(entries) + "\n")
    else:
        print(
            "gg: plan.md written but no ```manifest block found. "
            "Add one to enable the manifest check hook.",
            file=sys.stderr,
        )

    sys.exit(0)


if __name__ == "__main__":
    main()

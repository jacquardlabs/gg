#!/usr/bin/env python3
"""
PreToolUse hook — block edits to files not in the active plan manifest.

Reads the manifest from .gg/state/manifest.txt (one path per line,
relative to git root). Writes to plan.md are always allowed and set a
revision flag so the updater can re-parse the manifest afterward.

Exit 0 = allow. Exit 1 = block (message printed to stderr).
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import find_git_root, normalize_path, read_hook_input, state_dir

PLAN_PATTERN = re.compile(r"[/\\]plan\.md$")


def load_manifest(git_root: Path) -> set[str]:
    manifest_file = state_dir(git_root) / "manifest.txt"
    if not manifest_file.exists():
        return set()
    return {
        line.strip()
        for line in manifest_file.read_text().splitlines()
        if line.strip() and not line.strip().startswith("#")
    }


def main() -> None:
    data = read_hook_input()
    tool_input = data.get("tool_input", {})
    file_path = tool_input.get("file_path") or tool_input.get("path", "")
    if not file_path:
        sys.exit(0)

    git_root = find_git_root(Path.cwd())
    if not git_root:
        sys.exit(0)

    # Plan revisions are always allowed — they open the door for new files.
    if PLAN_PATTERN.search(file_path):
        sys.exit(0)

    manifest = load_manifest(git_root)
    if not manifest:
        sys.exit(0)  # no active manifest → allow all

    rel = normalize_path(file_path, git_root)

    if rel in manifest:
        sys.exit(0)

    print(f"gg: {rel} is not in the plan manifest.", file=sys.stderr)
    print("Revise plan.md to add this file, then edit.", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    main()

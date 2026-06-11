#!/usr/bin/env python3
"""
PostToolUse hook (Bash) — track consecutive failures per command signature.

Warns (exit 0, message to stderr) when the same command fails THRESHOLD
times in a row. Resets the counter on success. State persists in
.gg/state/failure_counts.json for the duration of the session.
"""
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import find_git_root, read_hook_input, state_dir

THRESHOLD = 2


def command_key(command: str) -> str:
    # Normalize whitespace before hashing so minor variations don't split counts.
    normalized = " ".join(command.split())
    return hashlib.sha1(normalized.encode()).hexdigest()[:12]


def load_counts(counts_file: Path) -> dict:
    if counts_file.exists():
        try:
            return json.loads(counts_file.read_text())
        except json.JSONDecodeError:
            pass
    return {}


def save_counts(counts_file: Path, counts: dict) -> None:
    counts_file.write_text(json.dumps(counts, indent=2))


def main() -> None:
    data = read_hook_input()
    tool_input = data.get("tool_input", {})
    tool_response = data.get("tool_response", {})

    command = tool_input.get("command", "")
    if not command:
        sys.exit(0)

    # Detect failure: non-zero exit code or error in response.
    exit_code = tool_response.get("exit_code")
    is_failure = exit_code not in (None, 0)

    git_root = find_git_root(Path.cwd())
    if not git_root:
        sys.exit(0)

    counts_file = state_dir(git_root) / "failure_counts.json"
    counts = load_counts(counts_file)
    key = command_key(command)

    if is_failure:
        counts[key] = counts.get(key, 0) + 1
        save_counts(counts_file, counts)

        if counts[key] >= THRESHOLD:
            short_cmd = command[:80] + ("…" if len(command) > 80 else "")
            print(
                f"gg: same command has failed {counts[key]} times in a row: {short_cmd!r}",
                file=sys.stderr,
            )
            print(
                "Consider escalating rather than retrying. "
                "See the escalating skill.",
                file=sys.stderr,
            )
    else:
        # Reset on success.
        if key in counts:
            del counts[key]
            save_counts(counts_file, counts)

    sys.exit(0)


if __name__ == "__main__":
    main()

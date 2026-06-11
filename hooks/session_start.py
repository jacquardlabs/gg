#!/usr/bin/env python3
"""
SessionStart hook — instrument a new session.

1. Starts `cctx watch` if cctx is available (degrades gracefully if not).
2. Records a purpose tag: reads GG_PURPOSE env var, or prompts the user
   if running interactively. Writes to .gg/state/session.json.
"""
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import find_git_root, read_hook_input, state_dir


def start_cctx_watch(transcript_path: str) -> None:
    if not shutil.which("cctx"):
        return
    try:
        subprocess.Popen(
            ["cctx", "watch", "--transcript", transcript_path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
        )
    except OSError:
        pass


def get_purpose() -> str:
    purpose = os.environ.get("GG_PURPOSE", "").strip()
    if purpose:
        return purpose

    # Interactive prompt — only when stdin is a tty.
    if sys.stdin.isatty():
        sys.stderr.write("gg: what's the goal of this session? (one line) > ")
        sys.stderr.flush()
        try:
            return sys.stdin.readline().strip()
        except (EOFError, KeyboardInterrupt):
            pass

    return ""


def main() -> None:
    data = read_hook_input()
    transcript_path = data.get("transcript_path", "")
    session_id = data.get("session_id", "")

    git_root = find_git_root(Path.cwd())
    if not git_root:
        sys.exit(0)

    start_cctx_watch(transcript_path)

    purpose = get_purpose()

    session_file = state_dir(git_root) / "session.json"
    session_file.write_text(
        json.dumps(
            {
                "session_id": session_id,
                "transcript_path": transcript_path,
                "purpose": purpose,
            },
            indent=2,
        )
    )

    if purpose:
        print(f"gg: session purpose recorded — {purpose!r}", file=sys.stderr)
    else:
        print("gg: no purpose set (set GG_PURPOSE or answer the prompt next time).", file=sys.stderr)

    sys.exit(0)


if __name__ == "__main__":
    main()

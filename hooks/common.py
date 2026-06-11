"""Shared utilities for gg hooks."""
from __future__ import annotations

import json
import sys
from pathlib import Path


def find_git_root(start: Path) -> Path | None:
    p = start.resolve()
    while p != p.parent:
        if (p / ".git").exists():
            return p
        p = p.parent
    return None


def state_dir(git_root: Path) -> Path:
    d = git_root / ".gg" / "state"
    d.mkdir(parents=True, exist_ok=True)
    return d


def read_hook_input() -> dict:
    return json.load(sys.stdin)


def normalize_path(path: str, git_root: Path) -> str:
    """Return path relative to git root, or the original string if outside."""
    try:
        return str(Path(path).resolve().relative_to(git_root))
    except ValueError:
        return path

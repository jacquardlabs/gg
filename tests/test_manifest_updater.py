"""Tests for manifest_updater.py."""
import json
import subprocess
import sys
from pathlib import Path

import pytest

HOOK = Path(__file__).parent.parent / "hooks" / "manifest_updater.py"


def run_hook(file_path: str, cwd: Path) -> subprocess.CompletedProcess:
    payload = json.dumps(
        {
            "tool_name": "Write",
            "tool_input": {"file_path": file_path},
            "hook_event_name": "PostToolUse",
        }
    )
    return subprocess.run(
        [sys.executable, str(HOOK)],
        input=payload,
        capture_output=True,
        text=True,
        cwd=cwd,
    )


@pytest.fixture()
def git_repo(tmp_path):
    (tmp_path / ".git").mkdir()
    (tmp_path / ".gg" / "state").mkdir(parents=True)
    return tmp_path


def test_non_plan_file_ignored(git_repo):
    result = run_hook(str(git_repo / "src" / "foo.py"), git_repo)
    assert result.returncode == 0
    assert not (git_repo / ".gg" / "state" / "manifest.txt").exists()


def test_parses_manifest_block(git_repo):
    plan = git_repo / "specs" / "01" / "plan.md"
    plan.parent.mkdir(parents=True)
    plan.write_text("# Plan\n\n```manifest\nsrc/foo.py\ntests/test_foo.py\n```\n")

    result = run_hook(str(plan), git_repo)
    assert result.returncode == 0

    manifest = (git_repo / ".gg" / "state" / "manifest.txt").read_text().splitlines()
    assert "src/foo.py" in manifest
    assert "tests/test_foo.py" in manifest


def test_warns_on_missing_manifest_block(git_repo):
    plan = git_repo / "specs" / "01" / "plan.md"
    plan.parent.mkdir(parents=True)
    plan.write_text("# Plan\n\nNo manifest block here.\n")

    result = run_hook(str(plan), git_repo)
    assert result.returncode == 0
    assert "no ```manifest block" in result.stderr


def test_ignores_comment_lines_in_manifest(git_repo):
    plan = git_repo / "specs" / "01" / "plan.md"
    plan.parent.mkdir(parents=True)
    plan.write_text(
        "# Plan\n\n```manifest\n# this is a comment\nsrc/foo.py\n```\n"
    )

    run_hook(str(plan), git_repo)
    manifest = (git_repo / ".gg" / "state" / "manifest.txt").read_text().splitlines()
    assert "src/foo.py" in manifest
    assert "# this is a comment" not in manifest

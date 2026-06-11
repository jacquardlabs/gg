"""Tests for manifest_check.py."""
import json
import subprocess
import sys
from pathlib import Path

import pytest

HOOK = Path(__file__).parent.parent / "hooks" / "manifest_check.py"


def run_hook(tool_input: dict, cwd: Path) -> subprocess.CompletedProcess:
    payload = json.dumps(
        {"tool_name": "Edit", "tool_input": tool_input, "hook_event_name": "PreToolUse"}
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
    state = tmp_path / ".gg" / "state"
    state.mkdir(parents=True)
    return tmp_path


def write_manifest(git_repo: Path, paths: list[str]) -> None:
    (git_repo / ".gg" / "state" / "manifest.txt").write_text(
        "\n".join(paths) + "\n"
    )


def test_no_manifest_allows_all(git_repo):
    result = run_hook({"file_path": str(git_repo / "src" / "foo.py")}, git_repo)
    assert result.returncode == 0


def test_file_in_manifest_allowed(git_repo):
    write_manifest(git_repo, ["src/foo.py"])
    result = run_hook({"file_path": str(git_repo / "src" / "foo.py")}, git_repo)
    assert result.returncode == 0


def test_file_not_in_manifest_blocked(git_repo):
    write_manifest(git_repo, ["src/foo.py"])
    result = run_hook({"file_path": str(git_repo / "src" / "bar.py")}, git_repo)
    assert result.returncode == 1
    assert "not in the plan manifest" in result.stderr


def test_plan_md_write_always_allowed(git_repo):
    write_manifest(git_repo, ["src/foo.py"])
    plan = git_repo / "specs" / "01-hooks" / "plan.md"
    result = run_hook({"file_path": str(plan)}, git_repo)
    assert result.returncode == 0


def test_revision_unlocks_edit(git_repo, tmp_path):
    """After plan.md is written (updater runs), new file is in manifest."""
    # Simulate updater having updated the manifest with a new file.
    write_manifest(git_repo, ["src/foo.py", "src/new.py"])
    result = run_hook({"file_path": str(git_repo / "src" / "new.py")}, git_repo)
    assert result.returncode == 0


def test_no_path_in_input_allowed(git_repo):
    write_manifest(git_repo, ["src/foo.py"])
    result = run_hook({}, git_repo)
    assert result.returncode == 0

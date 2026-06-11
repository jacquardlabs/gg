"""Tests for failure_counter.py."""
import json
import subprocess
import sys
from pathlib import Path

import pytest

HOOK = Path(__file__).parent.parent / "hooks" / "failure_counter.py"


def run_hook(command: str, exit_code: int, cwd: Path) -> subprocess.CompletedProcess:
    payload = json.dumps(
        {
            "tool_name": "Bash",
            "tool_input": {"command": command},
            "tool_response": {"exit_code": exit_code},
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


def test_success_no_warning(git_repo):
    result = run_hook("pytest tests/", 0, git_repo)
    assert result.returncode == 0
    assert result.stderr == ""


def test_single_failure_no_warning(git_repo):
    result = run_hook("pytest tests/", 1, git_repo)
    assert result.returncode == 0
    assert "failed" not in result.stderr


def test_two_failures_warns(git_repo):
    run_hook("pytest tests/", 1, git_repo)
    result = run_hook("pytest tests/", 1, git_repo)
    assert result.returncode == 0
    assert "failed 2 times in a row" in result.stderr
    assert "escalating" in result.stderr


def test_success_resets_counter(git_repo):
    run_hook("pytest tests/", 1, git_repo)
    run_hook("pytest tests/", 0, git_repo)  # success — resets
    result = run_hook("pytest tests/", 1, git_repo)
    assert "failed 2 times" not in result.stderr


def test_different_commands_counted_separately(git_repo):
    run_hook("pytest tests/", 1, git_repo)
    run_hook("make build", 1, git_repo)
    # Each has only 1 failure — neither should warn
    result_pytest = run_hook("pytest tests/", 0, git_repo)  # reset pytest
    assert "failed 2 times" not in result_pytest.stderr

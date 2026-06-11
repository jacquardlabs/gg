"""Tests for session_start.py."""
import json
import subprocess
import sys
from pathlib import Path

import pytest

HOOK = Path(__file__).parent.parent / "hooks" / "session_start.py"


def run_hook(env: dict | None = None, cwd: Path | None = None) -> subprocess.CompletedProcess:
    payload = json.dumps(
        {
            "session_id": "test-session-123",
            "transcript_path": "/tmp/test.jsonl",
            "hook_event_name": "SessionStart",
        }
    )
    return subprocess.run(
        [sys.executable, str(HOOK)],
        input=payload,
        capture_output=True,
        text=True,
        env=env,
        cwd=cwd,
    )


@pytest.fixture()
def git_repo(tmp_path):
    (tmp_path / ".git").mkdir()
    (tmp_path / ".gg" / "state").mkdir(parents=True)
    return tmp_path


def test_degrades_without_cctx(git_repo, monkeypatch):
    """Hook exits 0 even when cctx is not installed."""
    import os
    env = {k: v for k, v in os.environ.items() if k != "GG_PURPOSE"}
    env["PATH"] = ""  # cctx not findable
    result = run_hook(env=env, cwd=git_repo)
    assert result.returncode == 0


def test_purpose_from_env(git_repo):
    import os
    env = dict(os.environ)
    env["GG_PURPOSE"] = "implement manifest check hook"
    result = run_hook(env=env, cwd=git_repo)
    assert result.returncode == 0
    assert "implement manifest check hook" in result.stderr

    session_file = git_repo / ".gg" / "state" / "session.json"
    assert session_file.exists()
    data = json.loads(session_file.read_text())
    assert data["purpose"] == "implement manifest check hook"
    assert data["session_id"] == "test-session-123"


def test_no_purpose_logs_miss(git_repo):
    import os
    env = {k: v for k, v in os.environ.items() if k != "GG_PURPOSE"}
    env["PATH"] = ""
    result = run_hook(env=env, cwd=git_repo)
    assert result.returncode == 0
    assert "no purpose set" in result.stderr

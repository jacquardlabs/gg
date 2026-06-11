"""Structural validation for all eight gg skills."""
from pathlib import Path

import pytest
import yaml

SKILLS_DIR = Path(__file__).parent.parent / "skills"

SKILL_NAMES = [
    "writing-specs",
    "decomposing-specs",
    "escalating",
    "running-gates",
    "tending-guidelines",
    "checking-drift",
    "delegating-with-specs",
    "instrumenting-sessions",
]

# These skills govern hard boundaries and must have a HARD-GATE block.
HARD_GATE_REQUIRED = {
    "writing-specs",
    "decomposing-specs",
    "running-gates",
    "delegating-with-specs",
}

# All skills have a TRIGGER section except instrumenting-sessions,
# whose session-start half is a hook (automatic) not a skill trigger.
TRIGGER_REQUIRED = set(SKILL_NAMES) - {"instrumenting-sessions"}


def parse_frontmatter(path: Path) -> tuple[dict, str]:
    """Return (frontmatter_dict, body) from a skill markdown file."""
    text = path.read_text()
    if not text.startswith("---"):
        return {}, text
    _, fm_raw, body = text.split("---", 2)
    return yaml.safe_load(fm_raw), body


@pytest.fixture(params=SKILL_NAMES)
def skill_path(request):
    return SKILLS_DIR / f"{request.param}.md"


@pytest.fixture(params=SKILL_NAMES)
def skill_data(request):
    path = SKILLS_DIR / f"{request.param}.md"
    fm, body = parse_frontmatter(path)
    return request.param, fm, body


def test_skill_file_exists(skill_path):
    assert skill_path.exists(), f"Missing skill file: {skill_path}"


def test_skill_has_name_frontmatter(skill_data):
    name, fm, _ = skill_data
    assert "name" in fm, f"{name}: missing 'name' frontmatter key"
    assert fm["name"] == name, f"{name}: frontmatter name '{fm['name']}' does not match filename"


def test_skill_has_description_frontmatter(skill_data):
    name, fm, _ = skill_data
    assert "description" in fm, f"{name}: missing 'description' frontmatter key"
    assert len(fm["description"]) > 20, f"{name}: description is too short to be useful"


def test_trigger_section_present(skill_data):
    name, _, body = skill_data
    if name not in TRIGGER_REQUIRED:
        pytest.skip(f"{name} does not require a TRIGGER section")
    assert "## TRIGGER" in body, f"{name}: missing '## TRIGGER' section"


def test_hard_gate_present(skill_data):
    name, _, body = skill_data
    if name not in HARD_GATE_REQUIRED:
        pytest.skip(f"{name} does not require a HARD-GATE")
    assert "<HARD-GATE>" in body, f"{name}: missing '<HARD-GATE>' block"


def test_skill_has_rules_section(skill_data):
    name, _, body = skill_data
    assert "## Rules" in body, f"{name}: missing '## Rules' section"


def test_instrumenting_sessions_trigger_explains_hybrid(skill_data):
    name, _, body = skill_data
    if name != "instrumenting-sessions":
        pytest.skip("only applies to instrumenting-sessions")
    assert "TRIGGER" in body, "instrumenting-sessions: session-end TRIGGER section missing"
    assert "hook" in body.lower(), "instrumenting-sessions: should explain the session-start hook"

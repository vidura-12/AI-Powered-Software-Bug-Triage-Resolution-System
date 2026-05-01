# tests/test_classifier_agent.py
import pytest
from agents.classifier_agent import run_classifier_agent
import os

# ── Helper: create a temporary bug file ──────────────────────────────────────
def make_bug_file(tmp_path, content: str) -> str:
    f = tmp_path / "bug.txt"
    f.write_text(content)
    return str(f)


# ── Test 1: Critical severity is detected ────────────────────────────────────
def test_critical_severity_detected(tmp_path):
    content = """
    Title: Database wipes all user records on logout
    Reported by: Kamal Silva
    Component: Database Module
    File: src/db/session.py
    Description: All user records are permanently deleted when any user logs out.
    Data loss is confirmed. Security breach possible.
    """
    state = {
        "bug_file_path": make_bug_file(tmp_path, content),
        "agent_logs": [], "root_cause": None,
        "suggested_fix": None, "final_report": None,
    }
    result = run_classifier_agent(state)
    assert result["severity"] == "critical", (
        f"Expected 'critical' but got '{result['severity']}'"
    )


# ── Test 2: Minor severity is detected ───────────────────────────────────────
def test_minor_severity_detected(tmp_path):
    content = """
    Title: Button color is slightly off on the dashboard
    Reported by: Nimal Perera
    Component: UI
    Description: The submit button appears grey instead of blue. No functional impact.
    """
    state = {
        "bug_file_path": make_bug_file(tmp_path, content),
        "agent_logs": [], "root_cause": None,
        "suggested_fix": None, "final_report": None,
    }
    result = run_classifier_agent(state)
    assert result["severity"] == "minor", (
        f"Expected 'minor' but got '{result['severity']}'"
    )


# ── Test 3: Metadata is extracted correctly ───────────────────────────────────
def test_metadata_extracted(tmp_path):
    content = """
    Title: Payment fails for amounts above 10000
    Reported by: Saman Kumara
    Component: Payment Gateway
    Description: Any transaction above Rs.10000 throws a timeout error.
    """
    state = {
        "bug_file_path": make_bug_file(tmp_path, content),
        "agent_logs": [], "root_cause": None,
        "suggested_fix": None, "final_report": None,
    }
    result = run_classifier_agent(state)
    assert result["bug_title"] != "unknown"
    assert result["affected_component"] != "unknown"
    assert result["reported_by"] != "unknown"


# ── Test 4: State is never lost ───────────────────────────────────────────────
def test_state_fields_all_present(tmp_path):
    content = "Title: Login broken\nComponent: Auth\nDescription: Cannot log in."
    state = {
        "bug_file_path": make_bug_file(tmp_path, content),
        "agent_logs": [], "root_cause": None,
        "suggested_fix": None, "final_report": None,
    }
    result = run_classifier_agent(state)
    for key in ["severity", "bug_title", "affected_component",
                "reported_by", "raw_bug_report", "agent_logs"]:
        assert key in result, f"Missing key: {key}"


# ── Test 5: Log entry is appended to agent_logs ───────────────────────────────
def test_log_entry_appended(tmp_path):
    content = "Title: Crash on search\nComponent: Search\nDescription: App crashes."
    state = {
        "bug_file_path": make_bug_file(tmp_path, content),
        "agent_logs": ["existing log from before"],
        "root_cause": None, "suggested_fix": None, "final_report": None,
    }
    result = run_classifier_agent(state)
    assert len(result["agent_logs"]) == 2, "Agent1 should append exactly one log entry"
    assert "Agent1" in result["agent_logs"][1]


# ── Test 6: File not found raises error cleanly ───────────────────────────────
def test_missing_file_raises_error():
    state = {
        "bug_file_path": "nonexistent_file.txt",
        "agent_logs": [], "root_cause": None,
        "suggested_fix": None, "final_report": None,
    }
    with pytest.raises(FileNotFoundError):
        run_classifier_agent(state)


# ── Test 7: Severity is always one of the 3 valid values ─────────────────────
def test_severity_is_valid_value(tmp_path):
    content = "Title: Random bug\nComponent: Misc\nDescription: Something broke."
    state = {
        "bug_file_path": make_bug_file(tmp_path, content),
        "agent_logs": [], "root_cause": None,
        "suggested_fix": None, "final_report": None,
    }
    result = run_classifier_agent(state)
    assert result["severity"] in ["critical", "major", "minor"], (
        f"Invalid severity value: '{result['severity']}'"
    )
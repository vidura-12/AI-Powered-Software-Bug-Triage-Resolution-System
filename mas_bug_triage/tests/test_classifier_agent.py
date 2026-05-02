# tests/test_classifier_agent.py
import sys
import os

# ── Mock MUST be registered before any agent import ──
import tools.mock_llm as mock_llm
sys.modules['langchain_ollama'] = mock_llm

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from agents.classifier_agent import run_classifier_agent

# ── Helper: create a temporary bug file ──────────────────────────────────────
def make_bug_file(tmp_path, content: str) -> str:
    f = tmp_path / "bug.txt"
    f.write_text(content)
    return str(f)


# ── Test 1: Critical severity is detected ────────────────────────────────────
def test_critical_severity_detected(tmp_path):
    print("\n[TEST 1] Checking CRITICAL severity detection...")
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
    print(f"  → Severity     : {result['severity']}")
    print(f"  → Title        : {result['bug_title']}")
    print(f"  → Component    : {result['affected_component']}")
    print(f"  → Reported by  : {result['reported_by']}")
    assert result["severity"] == "critical", (
        f"Expected 'critical' but got '{result['severity']}'"
    )
    print("  ✔ PASSED — severity correctly identified as CRITICAL")


# ── Test 2: Minor severity is detected ───────────────────────────────────────
def test_minor_severity_detected(tmp_path):
    print("\n[TEST 2] Checking MINOR severity detection...")
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
    print(f"  → Severity     : {result['severity']}")
    print(f"  → Title        : {result['bug_title']}")
    print(f"  → Component    : {result['affected_component']}")
    print(f"  → Reported by  : {result['reported_by']}")
    assert result["severity"] == "minor", (
        f"Expected 'minor' but got '{result['severity']}'"
    )
    print("  ✔ PASSED — severity correctly identified as MINOR")


# ── Test 3: Metadata is extracted correctly ───────────────────────────────────
def test_metadata_extracted(tmp_path):
    print("\n[TEST 3] Checking metadata extraction...")
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
    print(f"  → Title        : {result['bug_title']}")
    print(f"  → Component    : {result['affected_component']}")
    print(f"  → Reported by  : {result['reported_by']}")
    assert result["bug_title"] != "unknown"
    assert result["affected_component"] != "unknown"
    assert result["reported_by"] != "unknown"
    print("  ✔ PASSED — all metadata fields extracted successfully")


# ── Test 4: State is never lost ───────────────────────────────────────────────
def test_state_fields_all_present(tmp_path):
    print("\n[TEST 4] Checking state integrity — no fields dropped...")
    content = "Title: Login broken\nComponent: Auth\nDescription: Cannot log in."
    state = {
        "bug_file_path": make_bug_file(tmp_path, content),
        "agent_logs": [], "root_cause": None,
        "suggested_fix": None, "final_report": None,
    }
    result = run_classifier_agent(state)
    expected_keys = ["severity", "bug_title", "affected_component",
                     "reported_by", "raw_bug_report", "agent_logs"]
    for key in expected_keys:
        print(f"  → Checking key '{key}': {repr(result.get(key, 'MISSING'))}")
        assert key in result, f"Missing key: {key}"
    print("  ✔ PASSED — all state fields present after agent execution")


# ── Test 5: Log entry is appended to agent_logs ───────────────────────────────
def test_log_entry_appended(tmp_path):
    print("\n[TEST 5] Checking observability — log entry appended...")
    content = "Title: Crash on search\nComponent: Search\nDescription: App stops."
    state = {
        "bug_file_path": make_bug_file(tmp_path, content),
        "agent_logs": ["existing log from before"],
        "root_cause": None, "suggested_fix": None, "final_report": None,
    }
    result = run_classifier_agent(state)
    print(f"  → Log count    : {len(result['agent_logs'])} (expected 2)")
    print(f"  → Log entry 1  : {result['agent_logs'][0]}")
    print(f"  → Log entry 2  : {result['agent_logs'][1]}")
    assert len(result["agent_logs"]) == 2, "Agent1 should append exactly one log entry"
    assert "Agent1" in result["agent_logs"][1]
    print("  ✔ PASSED — Agent1 log entry correctly appended to trace")


# ── Test 6: File not found raises error cleanly ───────────────────────────────
def test_missing_file_raises_error():
    print("\n[TEST 6] Checking error handling — missing file...")
    state = {
        "bug_file_path": "nonexistent_file.txt",
        "agent_logs": [], "root_cause": None,
        "suggested_fix": None, "final_report": None,
    }
    print("  → Calling agent with path: 'nonexistent_file.txt'")
    with pytest.raises(FileNotFoundError):
        run_classifier_agent(state)
    print("  ✔ PASSED — FileNotFoundError raised correctly")


# ── Test 7: Severity is always one of the 3 valid values ─────────────────────
def test_severity_is_valid_value(tmp_path):
    print("\n[TEST 7] Checking severity output is always a valid enum value...")
    content = "Title: Random bug\nComponent: Misc\nDescription: Something went wrong."
    state = {
        "bug_file_path": make_bug_file(tmp_path, content),
        "agent_logs": [], "root_cause": None,
        "suggested_fix": None, "final_report": None,
    }
    result = run_classifier_agent(state)
    print(f"  → Severity returned : '{result['severity']}'")
    print(f"  → Valid values      : ['critical', 'major', 'minor']")
    assert result["severity"] in ["critical", "major", "minor"], (
        f"Invalid severity value: '{result['severity']}'"
    )
    print("  ✔ PASSED — severity is a valid enum value")
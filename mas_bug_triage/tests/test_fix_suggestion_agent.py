# tests/test_fix_suggestion_agent.py

import pytest
from agents.fix_suggestion_agent import run_fix_suggestion_agent


# ── Test 1: Fix is generated for valid root cause ────────────────────────────
def test_fix_generated_successfully():
    state = {
        "root_cause": "Null pointer exception when accessing user name",
        "code_snippet": "user.name.length()",
        "agent_logs": [],
        "suggested_fix": None,
        "final_report": None,
    }

    result = run_fix_suggestion_agent(state)

    assert result["suggested_fix"] is not None
    assert len(result["suggested_fix"]) > 0


# ── Test 2: State is preserved correctly ─────────────────────────────────────
def test_state_preserved():
    state = {
        "root_cause": "Division by zero error",
        "code_snippet": "value / 0",
        "agent_logs": [],
        "suggested_fix": None,
        "final_report": None,
    }

    result = run_fix_suggestion_agent(state)

    for key in ["suggested_fix", "agent_logs"]:
        assert key in result, f"Missing key: {key}"


# ── Test 3: Agent appends log entry ──────────────────────────────────────────
def test_log_entry_added():
    state = {
        "root_cause": "Index out of range",
        "code_snippet": "arr[10]",
        "agent_logs": ["previous log"],
        "suggested_fix": None,
        "final_report": None,
    }

    result = run_fix_suggestion_agent(state)

    assert len(result["agent_logs"]) == 2
    assert "Agent3" in result["agent_logs"][1]


# ── Test 4: Handles empty root cause gracefully ──────────────────────────────
def test_empty_root_cause():
    state = {
        "root_cause": "",
        "code_snippet": "",
        "agent_logs": [],
        "suggested_fix": None,
        "final_report": None,
    }

    result = run_fix_suggestion_agent(state)

    assert "suggested_fix" in result


# ── Test 5: Output is always string ──────────────────────────────────────────
def test_output_is_string():
    state = {
        "root_cause": "Memory leak issue",
        "code_snippet": "list.append(data)",
        "agent_logs": [],
        "suggested_fix": None,
        "final_report": None,
    }

    result = run_fix_suggestion_agent(state)

    assert isinstance(result["suggested_fix"], str)


# ── Test 6: No crash on missing fields ───────────────────────────────────────
def test_missing_fields_safe():
    state = {
        "agent_logs": []
    }

    result = run_fix_suggestion_agent(state)

    assert "suggested_fix" in result
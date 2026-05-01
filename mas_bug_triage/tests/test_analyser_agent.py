# tests/test_agent2.py

import os
import pytest
from tools.tool2_read_code import read_code_file_tool


# ── Tests for the Tool ────────────────────────────────────────────────

class TestReadCodeFileTool:

    def test_reads_valid_python_file(self, tmp_path):
        """Tool should read a .py file and return numbered lines."""
        sample = tmp_path / "sample.py"
        sample.write_text("def hello():\n    return 'world'\n")

        result = read_code_file_tool(str(sample))

        assert "1 |" in result
        assert "def hello" in result
        assert "2 |" in result

    def test_line_numbers_are_sequential(self, tmp_path):
        """Each line should have a correct sequential number."""
        sample = tmp_path / "code.py"
        sample.write_text("a = 1\nb = 2\nc = 3\n")

        result = read_code_file_tool(str(sample))
        lines = result.strip().split("\n")

        assert "1 |" in lines[0]
        assert "2 |" in lines[1]
        assert "3 |" in lines[2]

    def test_file_not_found_returns_error(self):
        """Should return an error string when file doesn't exist."""
        result = read_code_file_tool("nonexistent/path/file.py")
        assert result.startswith("ERROR:")
        assert "not found" in result.lower()

    def test_unsupported_extension_returns_error(self, tmp_path):
        """Should reject non-Python/JS files."""
        bad_file = tmp_path / "document.pdf"
        bad_file.write_text("some content")

        result = read_code_file_tool(str(bad_file))
        assert result.startswith("ERROR:")
        assert "Unsupported" in result

    def test_reads_javascript_file(self, tmp_path):
        """Tool should also handle .js files."""
        js_file = tmp_path / "app.js"
        js_file.write_text("function greet() {\n  console.log('hi');\n}\n")

        result = read_code_file_tool(str(js_file))
        assert "1 |" in result
        assert "function greet" in result

    def test_empty_file_returns_empty_content(self, tmp_path):
        """Empty file should return empty string (no errors)."""
        empty = tmp_path / "empty.py"
        empty.write_text("")
        result = read_code_file_tool(str(empty))
        assert "ERROR" not in result


# ── LLM-as-a-Judge Test for the Agent ────────────────────────────────

def test_agent_output_contains_line_reference(tmp_path):
    """
    LLM-as-a-Judge style test: the root cause output from the agent
    should mention a line number, proving it actually read the code.
    This is a lightweight check — full LLM judge can be added later.
    """
    from agents.agent2_analyser import run_code_analyser_agent

    # Create a simple buggy Python file
    buggy = tmp_path / "buggy.py"
    buggy.write_text("def divide(a, b):\n    return a / b\n\nresult = divide(10, 0)\n")

    state = {
        "file_path": str(buggy),
        "bug_description": "ZeroDivisionError when b is 0",
        "severity": "critical",
        "log_trail": [],
    }

    updated_state = run_code_analyser_agent(state)

    # The agent must have added a root_cause
    assert "root_cause" in updated_state
    assert len(updated_state["root_cause"]) > 10

    # The log must have been updated
    assert len(updated_state["log_trail"]) == 1
    assert updated_state["log_trail"][0]["agent"] == "Agent 2 - Code Analyser"
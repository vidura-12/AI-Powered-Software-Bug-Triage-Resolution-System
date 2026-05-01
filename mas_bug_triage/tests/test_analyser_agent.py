# tests/test_analyser_agent.py

import pytest
import os
import sys

# Make sure imports work from project root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tools.read_code_file_tool import read_code_file


# ══════════════════════════════════════════════════════════════════════
#  TOOL TESTS — read_code_file_tool
# ══════════════════════════════════════════════════════════════════════

class TestReadCodeFileTool:

    def test_reads_valid_python_file(self, tmp_path):
        """Tool must read a .py file and return content with line numbers."""
        sample = tmp_path / "sample.py"
        sample.write_text("def hello():\n    return 'world'\n")

        result = read_code_file(str(sample))

        assert "1 |" in result
        assert "def hello" in result
        assert "2 |" in result

    def test_line_numbers_are_sequential(self, tmp_path):
        """Every line must have a correct sequential number."""
        sample = tmp_path / "code.py"
        sample.write_text("a = 1\nb = 2\nc = 3\n")

        result = read_code_file(str(sample))
        lines = result.strip().split("\n")

        assert "1 |" in lines[0]
        assert "2 |" in lines[1]
        assert "3 |" in lines[2]

    def test_file_not_found_raises_error(self):
        """Must raise FileNotFoundError when file doesn't exist."""
        with pytest.raises(FileNotFoundError) as exc_info:
            read_code_file("nonexistent/path/file.py")
        assert "not found" in str(exc_info.value).lower()

    def test_unsupported_extension_raises_error(self, tmp_path):
        """Must raise ValueError for non-code file types."""
        bad_file = tmp_path / "document.pdf"
        bad_file.write_text("some content")

        with pytest.raises(ValueError) as exc_info:
            read_code_file(str(bad_file))
        assert "Unsupported" in str(exc_info.value)

    def test_reads_javascript_file(self, tmp_path):
        """Tool must also handle .js files correctly."""
        js_file = tmp_path / "app.js"
        js_file.write_text("function greet() {\n  console.log('hi');\n}\n")

        result = read_code_file(str(js_file))

        assert "1 |" in result
        assert "function greet" in result

    def test_empty_file_returns_empty_string(self, tmp_path):
        """Empty file must return empty string with no errors."""
        empty = tmp_path / "empty.py"
        empty.write_text("")

        result = read_code_file(str(empty))
        assert result == ""

    def test_multiline_file_has_correct_count(self, tmp_path):
        """Number of numbered lines must match number of actual lines."""
        code = "line1\nline2\nline3\nline4\nline5\n"
        sample = tmp_path / "multi.py"
        sample.write_text(code)

        result = read_code_file(str(sample))
        numbered_lines = [l for l in result.split("\n") if "|" in l]

        assert len(numbered_lines) == 5

    def test_content_is_preserved(self, tmp_path):
        """Original code content must appear after the line number."""
        sample = tmp_path / "app.py"
        sample.write_text("x = 42\n")

        result = read_code_file(str(sample))

        assert "x = 42" in result


# ══════════════════════════════════════════════════════════════════════
#  AGENT STATE TESTS — run_analyser_agent (no LLM needed)
# ══════════════════════════════════════════════════════════════════════

class TestAnalyserAgentState:

    def test_agent_fails_gracefully_on_missing_file(self):
        """Agent must handle missing file and return error in root_cause."""
        from agents.analyser_agent import run_analyser_agent

        state = {
            "bug_file_path": "nonexistent/totally_fake.py",
            "bug_title": "Test bug",
            "severity": "minor",
            "affected_component": "unknown",
            "raw_bug_report": "Something broke",
            "agent_logs": [],
        }

        result = run_analyser_agent(state)

        # Must not crash — must return error message in root_cause
        assert "root_cause" in result
        assert "ERROR" in result["root_cause"]

    def test_agent_appends_to_log_trail(self, tmp_path):
        """Agent must always append exactly one entry to agent_logs."""
        # We only test the tool + state flow without LLM here
        # by checking that a bad file path still logs correctly
        from agents.analyser_agent import run_analyser_agent

        state = {
            "bug_file_path": "bad_path.py",
            "bug_title": "Test",
            "severity": "major",
            "affected_component": "API",
            "raw_bug_report": "API fails",
            "agent_logs": ["existing log from agent 1"],
        }

        result = run_analyser_agent(state)

        # Log must grow by exactly 1
        assert len(result["agent_logs"]) == 2
        assert "Agent2" in result["agent_logs"][1]

    def test_agent_preserves_existing_state_keys(self, tmp_path):
        """Agent must not delete any keys that Agent 1 put in state."""
        from agents.analyser_agent import run_analyser_agent

        state = {
            "bug_file_path": "bad_path.py",
            "bug_title": "Login crash",
            "severity": "critical",
            "affected_component": "Auth",
            "reported_by": "Ashan Fernando",
            "raw_bug_report": "App crashes on login",
            "agent_logs": [],
        }

        result = run_analyser_agent(state)

        # All Agent 1 keys must still be present
        assert result["bug_title"] == "Login crash"
        assert result["severity"] == "critical"
        assert result["reported_by"] == "Ashan Fernando"
from agents.reporter_agent import run_reporter_agent
import os

def test_report_generation():
    state = {
        "bug_report": "App crashes on login",
        "severity": "CRITICAL",
        "analysis": "Null pointer exception",
        "fix_suggestion": "Add null check",
        "file_path": "login.py"
    }

    result = run_reporter_agent(state)

    assert "report_path" in result
    assert os.path.exists(result["report_path"])

    with open(result["report_path"], "r", encoding="utf-8") as f:
        content = f.read()

    assert "Bug Resolution Report" in content
    assert "CRITICAL" in content

    print("✅ Test Passed")
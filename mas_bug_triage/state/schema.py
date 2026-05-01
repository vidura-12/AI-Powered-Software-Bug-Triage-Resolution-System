# state/schema.py
from typing import TypedDict, Optional


class BugTriageState(TypedDict):
    # --- Agent 1 fills these (classifier_agent) ---
    bug_file_path:      str           # path to the bug report file
    raw_bug_report:     str           # original text of the bug report
    severity:           str           # "critical", "major", or "minor"
    bug_title:          str           # short extracted title
    affected_component: str           # e.g. "login module", "payment API"
    reported_by:        str           # extracted author if present

    # --- Agent 2 fills these (analyser_agent) ← STUDENT 2 ---
    root_cause:         Optional[str] # root cause identified in source code
    buggy_lines:        str           # e.g. "5, 12" — line numbers of the bug
    confidence:         str           # "high", "medium", or "low"
    code_content:       str           # numbered source code that was read

    # --- Agent 3 fills these (fix_agent) ---
    suggested_fix:      Optional[str]

    # --- Agent 4 fills these (reporter_agent) ---
    final_report:       Optional[str]

    # --- Shared logging trail — every agent appends here ---
    agent_logs:         list[str]
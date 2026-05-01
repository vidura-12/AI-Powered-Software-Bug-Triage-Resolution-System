from typing import TypedDict, Optional

class BugTriageState(TypedDict):
    # --- Agent 1 fills these ---
    raw_bug_report: str           # original text of the bug report
    severity: str                 # "critical", "major", or "minor"
    bug_title: str                # short extracted title
    affected_component: str       # e.g. "login module", "payment API"
    reported_by: str              # extracted author if present
    bug_file_path: str            # path to the source file mentioned

    # --- Other agents fill these later ---
    root_cause: Optional[str]
    suggested_fix: Optional[str]
    final_report: Optional[str]

    # --- Logging trail ---
    agent_logs: list[str]
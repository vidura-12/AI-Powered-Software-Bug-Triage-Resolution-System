# agents/analyser_agent.py

import logging
import datetime
from langchain_ollama import OllamaLLM
from tools.read_code_file_tool import read_code_file

logging.basicConfig(
    filename="logs/agent_trace.log",
    level=logging.INFO,
    format="%(asctime)s — %(message)s"
)


def run_analyser_agent(state: dict) -> dict:
    """
    Agent 2: Code Analyser

    Takes the code file path from the shared state, reads the relevant
    source code using read_code_file tool, then uses the local LLM to
    identify the root cause of the classified bug.

    Args:
        state (dict): The shared global state. Must contain:
                      - 'code_file_path' (str): path to the source code file
                      - 'bug_title' (str): bug title from Agent 1
                      - 'severity' (str): severity level from Agent 1
                      - 'affected_component' (str): component from Agent 1
                      - 'agent_logs' (list): running log trail

    Returns:
        dict: Updated state with 'root_cause' and appended agent_logs entry.
    """

    # --- Step 1: Get values from shared state (set by Agent 1) ---
    # Use code_file_path for the actual source code file
    # Fall back to sample_code/buggy_app.py if not set
    file_path: str = state.get("code_file_path", "sample_code/buggy_app.py")

    bug_title: str = state.get("bug_title", "Unknown bug")
    severity: str = state.get("severity", "unknown")
    component: str = state.get("affected_component", "unknown")
    raw_bug_report: str = state.get("raw_bug_report", "")

    logging.info(f"[Agent2] Starting analysis for: {bug_title}")
    logging.info(f"[Agent2] Tool call: read_code_file('{file_path}')")

    # --- Step 2: Use the tool to read the source code file ---
    try:
        code_content: str = read_code_file(file_path)
        logging.info(f"[Agent2] Tool output: {len(code_content)} characters read")
    except (FileNotFoundError, ValueError, PermissionError, RuntimeError) as e:
        error_msg = str(e)
        logging.error(f"[Agent2] Tool error: {error_msg}")
        return {
            **state,
            "root_cause": f"ERROR: Could not read source file — {error_msg}",
            "buggy_lines": "",
            "confidence": "",
            "code_content": "",
            "agent_logs": state.get("agent_logs", []) + [
                f"[Agent2 — {datetime.datetime.now().isoformat()}] "
                f"FAILED — {error_msg}"
            ],
        }

    # --- Step 3: Build the system prompt ---
    system_prompt = """
You are an expert software debugger. Your ONLY job is to analyse source code
and identify the root cause of a reported bug. You must be precise.

Rules:
- Reference the EXACT line number(s) where the bug originates.
- Do NOT suggest a fix — only identify the root cause.
- Be concise: 3 to 5 sentences maximum.
- If you cannot find the cause in the code, say "Root cause not found in provided code."
- Respond ONLY in this exact format, nothing else:

ROOT_CAUSE: <your analysis here referencing line numbers>
BUGGY_LINES: <comma-separated line numbers e.g. 5, 12>
CONFIDENCE: <high|medium|low>
"""

    user_message = (
        f"Bug Report Summary:\n"
        f"- Title: {bug_title}\n"
        f"- Severity: {severity}\n"
        f"- Affected Component: {component}\n"
        f"- Description: {raw_bug_report}\n\n"
        f"Source Code to Analyse:\n{code_content}"
    )

    # --- Step 4: Call the local LLM ---
    llm = OllamaLLM(model="phi3:mini")   # phi3:mini fits in low RAM machines
    logging.info(f"[Agent2] LLM input sent — analysing source code")

    llm_output: str = llm.invoke(system_prompt + "\n" + user_message)
    logging.info(f"[Agent2] LLM output:\n{llm_output}")

    # --- Step 5: Parse the LLM output ---
    root_cause = "unknown"
    buggy_lines = "unknown"
    confidence = "low"

    for line in llm_output.strip().splitlines():
        line = line.strip()
        if line.startswith("ROOT_CAUSE:"):
            root_cause = line.replace("ROOT_CAUSE:", "").strip()
        elif line.startswith("BUGGY_LINES:"):
            buggy_lines = line.replace("BUGGY_LINES:", "").strip()
        elif line.startswith("CONFIDENCE:"):
            val = line.replace("CONFIDENCE:", "").strip().lower()
            if val in ["high", "medium", "low"]:
                confidence = val

    # --- Step 6: Update shared state ---
    log_entry = (
        f"[Agent2 — {datetime.datetime.now().isoformat()}] "
        f"Root cause identified (confidence: {confidence}) | "
        f"Buggy lines: {buggy_lines}"
    )

    updated_state = {
        **state,
        "root_cause": root_cause,
        "buggy_lines": buggy_lines,
        "confidence": confidence,
        "code_content": code_content,
        "agent_logs": state.get("agent_logs", []) + [log_entry],
    }

    print(f"\n[OK] Agent 2 done — Root cause found (confidence: {confidence})")
    print(f"     Buggy lines: {buggy_lines}\n")

    return updated_state
# agents/agent2_analyser.py

import json
import datetime
from langchain_community.llms import Ollama
from tools.tool2_read_code import read_code_file_tool


def run_code_analyser_agent(state: dict) -> dict:
    """
    Code Analyser Agent — Student 2.

    Reads the relevant source code file identified in the bug report,
    analyses it using a local LLM, and updates the shared state with
    a root cause analysis.

    Args:
        state (dict): The shared global state dictionary. Must contain:
                      - 'file_path' (str): path to the code file to analyse
                      - 'bug_description' (str): the bug description from Agent 1
                      - 'severity' (str): severity level from Agent 1
                      - 'log_trail' (list): running log of all agent actions

    Returns:
        dict: Updated state with 'root_cause' key added.
    """

    print("\n[Agent 2 - Code Analyser] Starting analysis...")

    # ── 1. Read the code file using our custom tool ──────────────────
    file_path: str = state.get("file_path", "")
    bug_description: str = state.get("bug_description", "No description provided.")
    severity: str = state.get("severity", "unknown")

    if not file_path:
        state["root_cause"] = "ERROR: No file path provided in state."
        return state

    code_content: str = read_code_file_tool(file_path)

    # ── 2. Build the prompt for the local LLM ────────────────────────
    prompt = f"""You are an expert software debugger. Your ONLY job is to analyse 
source code and identify the root cause of a reported bug.

Bug Report:
- Severity: {severity}
- Description: {bug_description}

Source Code (with line numbers):
{code_content}

Instructions:
1. Read the code carefully.
2. Identify the EXACT root cause of the bug described above.
3. Reference the specific line number(s) where the bug exists.
4. Be concise. Your answer must be 3-5 sentences maximum.
5. Do NOT suggest a fix yet — only identify the root cause.

Root Cause Analysis:"""

    # ── 3. Call the local Ollama model ───────────────────────────────
    llm = Ollama(model="llama3:8b", temperature=0)
    root_cause: str = llm.invoke(prompt)

    # ── 4. Log this agent's activity ─────────────────────────────────
    log_entry = {
        "agent": "Agent 2 - Code Analyser",
        "timestamp": datetime.datetime.now().isoformat(),
        "input": {
            "file_path": file_path,
            "bug_description": bug_description,
            "severity": severity,
        },
        "tool_used": "read_code_file_tool",
        "tool_input": file_path,
        "tool_output_length": len(code_content),
        "output": root_cause.strip(),
    }

    # Append to the shared log trail
    state["log_trail"].append(log_entry)

    # Also write to the logs/ folder
    with open("logs/agent2_log.json", "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry, indent=2) + "\n")

    # ── 5. Update global state ────────────────────────────────────────
    state["root_cause"] = root_cause.strip()
    state["code_content"] = code_content  # pass code forward if Agent 3 needs it

    print(f"[Agent 2 - Code Analyser] Done. Root cause identified.")
    print(f"  → {root_cause.strip()[:120]}...")

    return state
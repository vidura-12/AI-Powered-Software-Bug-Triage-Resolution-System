# agents/classifier_agent.py

import logging
import datetime
from langchain_ollama import OllamaLLM
from tools.read_bug_report_tool import read_bug_report

logging.basicConfig(
    filename="logs/agent_trace.log",
    level=logging.INFO,
    format="%(asctime)s — %(message)s"
)

def run_classifier_agent(state: dict) -> dict:
    """
    Agent 1: Bug Intake & Classifier

    Reads the raw bug report file, sends it to the local LLM with a
    strict classification prompt, then extracts severity and metadata
    into the shared global state.

    Args:
        state (dict): The shared LangGraph state. Must contain 'bug_file_path'.

    Returns:
        dict: Updated state with severity, bug_title, affected_component,
              reported_by, raw_bug_report, and an appended agent_logs entry.
    """

    # --- Step 1: Use the tool to read the file ---
    file_path = state["bug_file_path"]
    logging.info(f"[Agent1] Tool call: read_bug_report('{file_path}')")

    raw_text = read_bug_report(file_path)
    logging.info(f"[Agent1] Tool output: {len(raw_text)} characters read")

    # --- Step 2: Build the system prompt ---
    system_prompt = """
You are a senior software QA engineer. Your ONLY job is to analyse a bug report
and return a structured classification. You must be precise and never guess.

Rules:
- Severity is CRITICAL if the app crashes, data is lost, or security is breached.
- Severity is MAJOR if a core feature is broken but the app still runs.
- Severity is MINOR if it is a UI glitch, typo, or minor inconvenience.
- Extract the title, affected component, and reporter name exactly as written.
- If a field is not mentioned, write "unknown".
- Respond ONLY in this exact format, nothing else:

SEVERITY: <critical|major|minor>
TITLE: <one line title>
COMPONENT: <affected component>
REPORTED_BY: <name or unknown>
"""

    user_message = f"Classify this bug report:\n\n{raw_text}"

    # --- Step 3: Call the local LLM ---
    llm = OllamaLLM(model="llama3:8b")
    logging.info(f"[Agent1] LLM input sent — classifying bug report")

    llm_output = llm.invoke(system_prompt + "\n" + user_message)
    logging.info(f"[Agent1] LLM output:\n{llm_output}")

    # --- Step 4: Parse the LLM output ---
    severity = "minor"
    title = "unknown"
    component = "unknown"
    reported_by = "unknown"

    for line in llm_output.strip().splitlines():
        line = line.strip()
        if line.startswith("SEVERITY:"):
            val = line.replace("SEVERITY:", "").strip().lower()
            if val in ["critical", "major", "minor"]:
                severity = val
        elif line.startswith("TITLE:"):
            title = line.replace("TITLE:", "").strip()
        elif line.startswith("COMPONENT:"):
            component = line.replace("COMPONENT:", "").strip()
        elif line.startswith("REPORTED_BY:"):
            reported_by = line.replace("REPORTED_BY:", "").strip()

    # --- Step 5: Update shared state ---
    log_entry = (
        f"[Agent1 — {datetime.datetime.now().isoformat()}] "
        f"Classified as {severity.upper()} | Title: {title}"
    )

    updated_state = {
        **state,
        "raw_bug_report": raw_text,
        "severity": severity,
        "bug_title": title,
        "affected_component": component,
        "reported_by": reported_by,
        "agent_logs": state.get("agent_logs", []) + [log_entry],
    }

    print(f"\n✅ Agent 1 done — Severity: {severity.upper()} | {title}\n")
    return updated_state
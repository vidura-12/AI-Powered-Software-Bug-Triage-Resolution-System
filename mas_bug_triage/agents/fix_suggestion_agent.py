# agents/fix_suggestion_agent.py

import logging
import datetime
from langchain_ollama import OllamaLLM
from tools.search_local_docs_tool import search_local_docs

logging.basicConfig(
    filename="logs/agent_trace.log",
    level=logging.INFO,
    format="%(asctime)s — %(message)s"
)

def run_fix_suggestion_agent(state: dict) -> dict:
    """
    Agent 3: Fix Suggestion Agent

    Uses the root cause from previous agent and suggests a concrete fix.
    """

    # --- Step 1: Read input from state ---
    root_cause = state.get("root_cause", "unknown")
    code_snippet = state.get("code_snippet", "")

    logging.info(f"[Agent3] Received root cause: {root_cause}")

    # --- Step 2: Tool call (search local code patterns) ---
    logging.info(f"[Agent3] Tool call: search_local_docs('{root_cause}')")

    search_results = search_local_docs(root_cause)

    logging.info(f"[Agent3] Tool output: {len(search_results)} matches found")

    # --- Step 3: Build system prompt ---
    system_prompt = """
You are a senior software engineer. Your task is to suggest a precise fix for a bug.

Rules:
- Use the root cause to determine the fix
- Suggest practical and realistic code changes
- If possible, include a corrected code snippet
- Do not guess or hallucinate
- Keep response structured

Respond ONLY in this format:

FIX:
<short explanation of fix>

CODE:
<corrected code snippet or steps>
"""

    user_message = f"""
Root Cause:
{root_cause}

Code Context:
{code_snippet}

Relevant Matches:
{search_results}
"""

    # --- Step 4: Call LLM ---
    llm = OllamaLLM(model="llama3:8b")

    logging.info("[Agent3] LLM input sent — generating fix")

    llm_output = llm.invoke(system_prompt + "\n" + user_message)

    logging.info(f"[Agent3] LLM output:\n{llm_output}")

    # --- Step 5: Update state ---
    log_entry = (
        f"[Agent3 — {datetime.datetime.now().isoformat()}] "
        f"Generated fix suggestion"
    )

    updated_state = {
        **state,
        "suggested_fix": llm_output,
        "agent_logs": state.get("agent_logs", []) + [log_entry],
    }

    print(f"\n[OK] Agent 3 done - Fix Suggestion Generated\n")

    return updated_state
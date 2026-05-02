import logging
import datetime
from langchain_ollama import OllamaLLM   # ✅ ADDED
from tools.write_report_tool import write_report

logging.basicConfig(
    filename="logs/agent_trace.log",
    level=logging.INFO,
    format="%(asctime)s — %(message)s"
)

def run_reporter_agent(state: dict) -> dict:
    logging.info("[Reporter Agent] Started")

    print("\n📄 Generating final AI report...")

    # 🔥 FIXED: Correct state keys (ONLY CHANGE)
    bug_report = state.get("bug_title", "N/A")
    severity = state.get("severity", "N/A")
    analysis = state.get("root_cause", "N/A")
    fix = state.get("suggested_fix", "N/A")
    file_path = state.get("buggy_lines", "N/A")

    # ✅ ADDED: Initialize LLM
    llm = OllamaLLM(model="phi3")

    # ✅ ADDED: Prompt for LLM (kept simple)
    prompt = f"""
Generate a structured bug report with:
- Summary
- Severity explanation
- Root cause
- Fix recommendation
- Conclusion

Bug: {bug_report}
Severity: {severity}
Analysis: {analysis}
Fix: {fix}
File: {file_path}
"""

    # ✅ ADDED: Get AI-generated content
    ai_generated = llm.invoke(prompt)

    # ❗ KEEP YOUR EXISTING STRUCTURE (no removal)
    ai_report = f"""
Summary:
The system encountered the following issue: {bug_report}

Severity Explanation:
The issue is categorized as {severity}, indicating its impact on system stability.

Root Cause Analysis:
{analysis}

Recommended Fix:
{fix}

Conclusion:
This issue should be resolved promptly.
"""

    # ✅ ADDED: Append real AI output (without breaking your format)
    ai_report += f"\n\n---\n\n🔍 AI Enhanced Insights:\n{ai_generated}\n"

    priority = "HIGH" if severity.upper() == "CRITICAL" else "MEDIUM"
    confidence = "85%"

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    final_report = f"""
# 🐞 AI Bug Resolution Report

## 📅 Generated On
{timestamp}

---

## 📝 Bug Summary
{bug_report}

---

## 🚨 Severity Level
{severity}

---

## ⚡ Priority
{priority}

---

## 📊 Confidence Level
{confidence}

---

## 🤖 AI Detailed Report
{ai_report}

---

## 📂 Affected File
{file_path}

---

## 📌 Recommendation
Fix immediately if severity is critical.

---

## ✅ Status
AI Suggested Fix Generated
"""

    output_path = f"reports/bug_report_{datetime.datetime.now().strftime('%H%M%S')}.md"
    write_report(output_path, final_report)

    logging.info(f"[Reporter Agent] Report saved to {output_path}")

    state["report_path"] = output_path

    return state
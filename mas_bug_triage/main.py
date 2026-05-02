# main.py
import sys
sys.stdout.reconfigure(encoding='utf-8')
import tools.mock_llm as mock_llm
sys.modules['langchain_ollama'] = mock_llm

from langgraph.graph import StateGraph, END
from state.schema import BugTriageState
from agents.classifier_agent import run_classifier_agent
from agents.analyser_agent import run_analyser_agent
from agents.fix_suggestion_agent import run_fix_suggestion_agent
from agents.reporter_agent import run_reporter_agent

# ── Build the graph ───────────────────────────────────────────────────
graph = StateGraph(BugTriageState)

graph.add_node("classifier",     run_classifier_agent)
graph.add_node("analyser",       run_analyser_agent)
graph.add_node("fix_suggestion", run_fix_suggestion_agent)
graph.add_node("reporter",       run_reporter_agent)

# ── Define the flow ───────────────────────────────────────────────────
graph.set_entry_point("classifier")

graph.add_edge("classifier",     "analyser")
graph.add_edge("analyser",       "fix_suggestion")
graph.add_edge("fix_suggestion", "reporter")
graph.add_edge("reporter",       END)

# ── Compile and run ───────────────────────────────────────────────────
app = graph.compile()

result = app.invoke({
    "bug_file_path":      "sample_bug.txt",
    "raw_bug_report":     "",
    "severity":           "",
    "bug_title":          "",
    "affected_component": "",
    "reported_by":        "",
    "root_cause":         None,
    "buggy_lines":        "",
    "confidence":         "",
    "code_content":       "",
    "suggested_fix":      None,
    "final_report":       None,
    "agent_logs":         [],
})

# ── Print final state ─────────────────────────────────────────────────
print("\n" + "="*60)
print("           FINAL PIPELINE STATE")
print("="*60)

print("\n── Agent 1: Classifier ──────────────────────────────────")
print(f"  Severity         : {result['severity']}")
print(f"  Title            : {result['bug_title']}")
print(f"  Component        : {result['affected_component']}")
print(f"  Reported By      : {result['reported_by']}")

print("\n── Agent 2: Analyser ────────────────────────────────────")
print(f"  Root Cause       : {result['root_cause']}")
print(f"  Buggy Lines      : {result['buggy_lines']}")
print(f"  Confidence       : {result['confidence']}")

print("\n── Agent 3: Fix Suggestion ──────────────────────────────")
print(f"  Suggested Fix    : {result['suggested_fix']}")

print("\n── Agent 4: Reporter ────────────────────────────────────")
print(f"  Final Report     : {result['final_report']}")

print("\n── Agent Logs (full trace) ──────────────────────────────")
for i, log in enumerate(result['agent_logs'], 1):
    print(f"  [{i}] {log}")

print("\n" + "="*60)
print("           PIPELINE COMPLETE")
print("="*60)
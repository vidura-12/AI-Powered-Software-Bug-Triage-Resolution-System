# main.py
import sys
sys.stdout.reconfigure(encoding='utf-8')

from langgraph.graph import StateGraph, END
from state.schema import BugTriageState
from agents.classifier_agent import run_classifier_agent
from agents.analyser_agent import run_analyser_agent

# ── Build the graph ───────────────────────────────────────────────────
graph = StateGraph(BugTriageState)

# Add each agent as a node
graph.add_node("classifier", run_classifier_agent)   # Student 1
graph.add_node("analyser",   run_analyser_agent)     # Student 2 ← YOUR NODE

# Student 3 — add when ready:
# graph.add_node("fix_suggester", run_fix_agent)

# Student 4 — add when ready:
# graph.add_node("reporter", run_reporter_agent)

# ── Define the flow ───────────────────────────────────────────────────
graph.set_entry_point("classifier")          # starts at Agent 1
graph.add_edge("classifier", "analyser")     # Agent 1 → Agent 2 (YOUR AGENT)
graph.add_edge("analyser",   END)            # Agent 2 → END for now

# Student 3 & 4 — replace the line above with these when ready:
# graph.add_edge("analyser",      "fix_suggester")
# graph.add_edge("fix_suggester", "reporter")
# graph.add_edge("reporter",      END)

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
print("\n=== Final State ===")
print(f"Severity     : {result['severity']}")
print(f"Title        : {result['bug_title']}")
print(f"Component    : {result['affected_component']}")
print(f"Reported by  : {result['reported_by']}")
print(f"Root Cause   : {result['root_cause']}")
print(f"Buggy Lines  : {result['buggy_lines']}")
print(f"Confidence   : {result['confidence']}")
print(f"Logs         : ")
for log in result['agent_logs']:
    print(f"  {log}")
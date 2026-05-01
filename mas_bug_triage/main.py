# main.py (your portion — teammates will add their nodes later)

from langgraph.graph import StateGraph, END
from state.schema import BugTriageState
from agents.classifier_agent import run_classifier_agent

graph = StateGraph(BugTriageState)

graph.add_node("classifier", run_classifier_agent)

# For now, your node goes straight to END
# Teammates will replace END with their node names
graph.set_entry_point("classifier")
graph.add_edge("classifier", END)

app = graph.compile()

# Run it
result = app.invoke({
    "bug_file_path": "sample_bug.txt",
    "agent_logs": [],
    "root_cause": None,
    "suggested_fix": None,
    "final_report": None,
})

print("=== Final State ===")
print(f"Severity     : {result['severity']}")
print(f"Title        : {result['bug_title']}")
print(f"Component    : {result['affected_component']}")
print(f"Reported by  : {result['reported_by']}")
print(f"Logs         : {result['agent_logs']}")
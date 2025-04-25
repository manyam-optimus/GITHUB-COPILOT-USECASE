from langgraph.graph import StateGraph, END
from typing import TypedDict, List, Dict
from nodes.fetch_pr import fetch_pr_node
from nodes.approve import approval_node
from nodes.summarize import summarize_node
from graphs.file_review_subgraph import build_file_review_subgraph

# Define LangGraph State
class State(TypedDict):
    owner: str
    repo: str
    pr_number: int
    commit_id: str
    pr_data: Dict
    modified_files: List[Dict] 
    file_reviews: List[Dict]    
    approval_status: str
    summary: str

# ---- Start Graph Definition ----
workflow = StateGraph(State)

# Step 1: Add nodes
workflow.add_node("fetch_pr", fetch_pr_node)

# Step 2: (run a subgraph for each file)
# Subgraph returns: code_review, security_review, comments
file_review_subgraph = build_file_review_subgraph()
workflow.add_node("review_files", file_review_subgraph)

# Step 3: After parallel reviews, run approval and summarization
workflow.add_node("approve_pr", approval_node)
workflow.add_node("summarize", summarize_node)

# Step 4: Edges
workflow.set_entry_point("fetch_pr")
workflow.add_edge("fetch_pr", "review_files")
workflow.add_edge("review_files", "approve_pr")
workflow.add_edge("approve_pr", "summarize")
workflow.set_finish_point("summarize")

# ---- Run the graph ----
graph = workflow.compile()

if __name__ == "__main__":
    test_state = {
        "owner": "manyam-optimus",
        "repo": "GITHUB-COPILOT-USECASE",
        "pr_number": 1,
        "commit_id": ""
    }

    result = graph.invoke(test_state)

    # Print final results
    # print("\n✅ Approval Decision:", result["approval_status"])
    # print("\n📝 Summary:", result["summary"])
    print(result)

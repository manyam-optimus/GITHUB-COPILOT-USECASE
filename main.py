from langgraph.graph import StateGraph
from typing import TypedDict, List, Dict
from nodes.fetch_pr import fetch_pr_node
from nodes.approve import approval_node
from nodes.summarize import summarize_node
from nodes.post_to_github import approval_node
from graphs.file_review_subgraph import build_file_review_subgraph

class State(TypedDict):
    owner: str
    repo: str
    pr_number: int
    commit_id: str
    pr_data: Dict
    modified_files: List[str]     # List of file paths
    file_reviews: List[Dict]      # List of file review results
    approval_status: str
    summary: str

workflow = StateGraph(State)

workflow.add_node("fetch_pr", fetch_pr_node)

file_review_subgraph = build_file_review_subgraph()

# ---  node to run reviews per file ---
from langgraph.graph import StateGraph
from typing import TypedDict, List, Dict
from nodes.fetch_pr import fetch_pr_node
from nodes.approve import approval_node
from nodes.summarize import summarize_node
from graphs.file_review_subgraph import build_file_review_subgraph

class State(TypedDict):
    owner: str
    repo: str
    pr_number: int
    commit_id: str
    pr_data: Dict
    modified_files: List[str]     # List of file paths
    file_reviews: List[Dict]      # List of file review results
    approval_status: str
    summary: str

workflow = StateGraph(State)

workflow.add_node("fetch_pr", fetch_pr_node)

file_review_subgraph = build_file_review_subgraph()

# ---  node to run reviews per file ---
def run_reviews_per_file(state: State) -> State:
    modified_files = state.get("modified_files", [])
    
    file_reviews = []

    for file_info in modified_files:
        file_path = file_info["file_path"]
        file_diff = file_info["diff"]   
        
        file_state = {
            "file_path": file_path,
            "pr_diff": file_diff,
            "code_review": "",
            "security_review": "",
            "comments": [],
        }
        result = file_review_subgraph.invoke(file_state)
        file_reviews.append({
            "file_path": file_path,
            "pr_diff": file_diff,
            "code_review": result.get("code_review", ""),
            "security_review": result.get("security_review", ""),
            "comments": result.get("comments", []),
        })

    # Add all file reviews back to main state
    state["file_reviews"] = file_reviews
    return state


workflow.add_node("review_files", run_reviews_per_file)

workflow.add_node("approve_pr", approval_node)
workflow.add_node("summarize", summarize_node)
workflow.add_node("post_review_comments", approval_node)


workflow.set_entry_point("fetch_pr")
workflow.add_edge("fetch_pr", "review_files")
workflow.add_edge("review_files", "approve_pr")
workflow.add_edge("approve_pr", "summarize")
workflow.add_edge("summarize","post_review_comments")
workflow.set_finish_point("post_review_comments")

graph = workflow.compile()

if __name__ == "__main__":
    test_state = {
        "owner": "manyam-optimus",
        "repo": "GITHUB-COPILOT-USECASE",
        "pr_number": 3,
        "commit_id": ""
    }

    result = graph.invoke(test_state)

    print("\nFinal File Reviews:")
    for review in result["file_reviews"]:
        print(f"\nFile: {review['file_path']}")
        print(f"Code Review: {review['code_review']}")
        print(f"Security Review: {review['security_review']}")
        print(f"Comments: {review['comments']}")

    print("\nApproval Status:", result["approval_status"])
    print("\nSummary:", result["summary"])


workflow.add_node("review_files", run_reviews_per_file)

workflow.add_node("approve_pr", approval_node)
workflow.add_node("summarize", summarize_node)

workflow.set_entry_point("fetch_pr")
workflow.add_edge("fetch_pr", "review_files")
workflow.add_edge("review_files", "approve_pr")
workflow.add_edge("approve_pr", "summarize")
workflow.set_finish_point("summarize")

graph = workflow.compile()

if __name__ == "__main__":
    test_state = {
        "owner": "manyam-optimus",
        "repo": "GITHUB-COPILOT-USECASE",
        "pr_number": 1,
        "commit_id": ""
    }

    result = graph.invoke(test_state)

    print("\nFinal File Reviews:")
    # for review in result["file_reviews"]:
    #     print(f"\nFile: {review['file_path']}")
    #     print(f"Code Review: {review['code_review']}")
    #     print(f"Security Review: {review['security_review']}")
    #     print(f"Comments: {review['comments']}")

    # print("\nApproval Status:", result["approval_status"])
    print("\nSummary:", result["summary"])

from langgraph.graph import StateGraph
from typing import TypedDict, Dict
from nodes.analyze_code import analyze_code_node
from nodes.security_check import security_check_node
from nodes.comment import comment_node

class FileReviewState(TypedDict):
    pr_diff: str
    file_path: str
    code_review: str
    security_review: str
    comments: list

def build_file_review_subgraph():
    graph = StateGraph(FileReviewState)

    graph.add_node("analyze_code", analyze_code_node)
    graph.add_node("security_check", security_check_node)
    graph.add_node("comment", comment_node)

    graph.set_entry_point("analyze_code")
    graph.add_edge("analyze_code", "security_check")
    graph.add_edge("security_check", "comment")
    graph.set_finish_point("comment")

    result = graph.compile()
    return result

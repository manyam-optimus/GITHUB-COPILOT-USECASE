from github import Github
import os

def approval_node(state: dict) -> dict:
    github_token = os.getenv("GITHUB_TOKEN")
    g = Github(github_token)

    owner = state["owner"]
    repo_name = state["repo"]
    pr_number = state["pr_number"]

    repo = g.get_repo(f"{owner}/{repo_name}")
    pull = repo.get_pull(pr_number)

    #  approve if no major issues
    file_reviews = state.get("file_reviews", [])

    all_good = True

    for review in file_reviews:
        code_review = review.get("code_review", "")
        security_review = review.get("security_review", "")

        # If code review or security review says anything negative, you can customize
        if "error" in code_review.lower() or "error" in security_review.lower():
            all_good = False
            break

    if all_good:
        pull.create_review(
            body="✅Approved by Copilot Bot - All checks passed!",
            event="APPROVE",
        )
        state["approval_status"] = "approved"
    else:
        state["approval_status"] = "changes_requested"

    return state

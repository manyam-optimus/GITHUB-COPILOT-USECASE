# import os
# import requests
# from dotenv import load_dotenv

# load_dotenv()

# GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
# HEADERS = {
#     "Authorization": f"token {GITHUB_TOKEN}",
#     "Accept": "application/vnd.github.v3+json"
# }
# DIFF_HEADERS = {
#     "Authorization": f"token {GITHUB_TOKEN}",
#     "Accept": "application/vnd.github.v3.diff"
# }


# def fetch_pr_node(state):
#     # creating a state that contain owner,repo and pull_number
#     owner = state.get("owner")
#     repo = state.get("repo")
#     pull_number = state.get("pull_number")

#     # Fetch PR metadata
#     pr_url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pull_number}"
#     pr_response = requests.get(pr_url, headers=HEADERS)
#     pr_data = pr_response.json()

#     # Fetch PR diff
#     diff_response = requests.get(pr_url, headers=DIFF_HEADERS)
#     diff_data = diff_response.text

#     # Add results to state and return
#     return {
#         **state,
#         "pr_data": pr_data,
#         "pr_diff": diff_data
#     }
from github import Github
import os
from dotenv import load_dotenv

load_dotenv()

def fetch_pr_node(state):
    owner = state.get("owner")
    repo_name = state.get("repo")
    pull_number = state.get("pr_number")

    # Initialize GitHub client
    token = os.getenv("GITHUB_TOKEN")
    g = Github(token)
    repo = g.get_repo(f"{owner}/{repo_name}")
    pr = repo.get_pull(pull_number)

    # Extract PR metadata
    pr_data = {
        "title": pr.title,
        "body": pr.body,
        "user": pr.user.login,
        "state": pr.state,
        "created_at": pr.created_at.isoformat(),
    }

    # Fetch modified files with diffs
    files = pr.get_files()
    modified_files = []
    for file in files:
        modified_files.append({
            "file_path": file.filename,
            "diff": file.patch  # The line-level diff of the file
        })

    # Update the state with the fetched data
    state["pr_data"] = pr_data
    state["modified_files"] = modified_files

    return state

import os
import requests
from dotenv import load_dotenv
load_dotenv()

def post_to_github_node(state):
    owner = state["owner"]
    repo = state["repo"]
    pr_number = state["pr_number"]
    comments = state.get("comments", [])
    summary = state.get("summary", "")

    github_token = os.getenv("GITHUB_TOKEN")
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github+json"
    }

    for c in comments:
        line = c["line"]
        comment_body = c["comment"]
        comment_data = {
            "body": comment_body,
            "commit_id": state.get("commit_id"),  
            "path": state.get("file_path"),       
            "line": line,
            "side": "RIGHT"
        }

        url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/comments"
        response = requests.post(url, headers=headers, json=comment_data)
        if not response.ok:
            print(f"Failed to post inline comment: {response.text}")

    summary_data = {
        "body": f"### Code Review Summary\n{summary}"
    }
    summary_url = f"https://api.github.com/repos/{owner}/{repo}/issues/{pr_number}/comments"
    summary_response = requests.post(summary_url, headers=headers, json=summary_data)

    if not summary_response.ok:
        print(f"Failed to post summary: {summary_response.text}")
    
    return state

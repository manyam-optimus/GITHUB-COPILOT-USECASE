
def post_process_files_node(state):
    file_results = state.get("file_results", [])
    
    all_comments = []
    all_code_reviews = []
    all_security_reviews = []

    for file in file_results:
        all_comments.extend(file.get("comment", []))
        all_code_reviews.append(f"File: {file['file_path']}\n{file.get('code_review', '')}")
        all_security_reviews.append(f"File: {file['file_path']}\n{file.get('security_review', '')}")

    state["inline_comments"] = all_comments
    state["all_code_reviews"] = "\n\n".join(all_code_reviews)
    state["all_security_reviews"] = "\n\n".join(all_security_reviews)

    return state

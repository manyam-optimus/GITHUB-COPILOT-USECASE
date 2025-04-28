from langchain_openai import AzureChatOpenAI
from langchain.schema import HumanMessage
from dotenv import load_dotenv
import os

load_dotenv()

def summarize_node(state):
    diff = state.get("pr_diff", "")
    comments = state.get("inline_comments", [])

    comment_text = "\n".join([f"- Line {c['line']}: {c['comment']}" for c in comments])

    api_key = os.getenv("AZURE_OPENAI_KEY")
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    version = os.getenv("AZURE_OPENAI_API_VERSION")
    deployment = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT")

    llm = AzureChatOpenAI(
        api_key=api_key,
        azure_endpoint=endpoint,
        deployment_name=deployment,
        api_version=version,
        temperature=0.3
    )

    prompt = f"""
You are a senior software engineer reviewing a GitHub Pull Request.

Based on the diff and reviewer comments, summarize:
1. What changes were made in this PR
2. What key improvements or issues were found
3. Overall quality of the submission

Be concise and professional.

--- Pull Request Diff ---
{diff}

--- Inline Comments ---
{comment_text}
    """.strip()

    messages = [HumanMessage(content=prompt)]
    response = llm.invoke(messages)

    summary = response.content.strip()
    state["summary"] = summary
    return state

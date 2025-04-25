from langchain_openai import AzureChatOpenAI
from langchain.schema import HumanMessage
from dotenv import load_dotenv
import os

load_dotenv()

def approval_node(state):
    comments = state.get("inline_comments", [])
    comment_text = "\n".join([f"Line {c['line']}: {c['comment']}" for c in comments])

    api_key = os.getenv("AZURE_OPENAI_KEY")
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    version = os.getenv("AZURE_OPENAI_API_VERSION")
    deployment = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT")

    llm = AzureChatOpenAI(
        api_key=api_key,
        azure_endpoint=endpoint,
        deployment_name=deployment,
        api_version=version,
        temperature=0
    )

    prompt = f"""
You are a senior code reviewer. Based on the inline comments from a pull request, decide whether it should be auto-approved or flagged for human review.
Only reply with one word: "approve" or "needs_manual_review".

Comments:
{comment_text}
    """.strip()

    messages = [HumanMessage(content=prompt)]
    response = llm.invoke(messages)

    decision = response.content.strip().lower()
    if decision not in ["approve", "needs_manual_review"]:
        decision = "needs_manual_review" 

    state["approval_status"] = decision
    return state

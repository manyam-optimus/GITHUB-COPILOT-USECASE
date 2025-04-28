from langchain_openai import AzureChatOpenAI
from langchain.schema import HumanMessage
import os
from dotenv import load_dotenv
import json  

load_dotenv()

def comment_node(state):
    diff = state.get("pr_diff", "")
    
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
You are a professional code reviewer. You will be shown a GitHub Pull Request diff.
Your task is to return ONLY a JSON array of inline comments on specific lines.

Each comment should follow this format:
[
  {{ "line": 12, "comment": "This loop is inefficient and could be optimized." }},
  {{ "line": 20, "comment": "Consider renaming the variable for clarity." }}
]

DO NOT add any explanation outside the JSON array.
DO NOT add markdown, headings, or prose.
Only respond with a valid JSON list of comment objects.

Review the following code diff:
{diff}
"""

    messages = [HumanMessage(content=prompt)]
    response = llm.invoke(messages)  

    try:
        comments = json.loads(response.content)
    except json.JSONDecodeError:
        comments = [{"line": 1, "comment": "Failed to parse LLM response"}]

    state["comments"] = comments
    return state

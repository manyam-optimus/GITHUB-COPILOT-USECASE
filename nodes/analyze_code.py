from langchain.schema import HumanMessage
from langchain_openai import AzureChatOpenAI
import os
from dotenv import load_dotenv
load_dotenv()

def analyze_code_node(state):
    diff=state.get("pr_diff","")
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
    You are a senior software engineer. Review the following GitHub Pull Request diff and provide:
    - Code quality issues
    - Suggestions for improvement
    - Any bugs or logic errors
    - If everything looks fine, say so.

    Diff:
    {diff}
    """
    messages=[HumanMessage(content=prompt)]
    response=llm(messages)

    state["code_review"]=response.content
    return state
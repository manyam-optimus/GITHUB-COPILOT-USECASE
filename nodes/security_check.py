from langchain.schema import HumanMessage
from langchain_openai import AzureChatOpenAI
import os
from dotenv import load_dotenv
load_dotenv()

def security_check_node(state):
    diff = state.get("pr_diff","")
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
    You are an expert in secure and high-performance software development.
    Analyze the following GitHub Pull Request diff for:
    - Security vulnerabilities (e.g., unsanitized input, insecure dependencies)
    - Performance issues (e.g., inefficient loops, blocking calls)
    - Dependency risks

    Provide detailed feedback with suggestions.

    Diff:
    {diff}
    """

    messages = [HumanMessage(content=prompt)]
    response = llm(messages)

    state["security_review"] = response.content
    return state
from agent.state import AgentState
from langchain.agents import create_agent
from typing import Literal
from models.classifier import DomainClassification

SYSTEM_PROMPT = """
        You are a query classifier. Classify the user's question into ONE category.

        Categories:
        - github: commits, pushes, history, changes, who wrote what
        - linear: issues, bugs, tasks, assignments, status, who's working on what

        Examples:
        - "What did Sarah commit?" → github
        - "What was Divya working on?" → github
        - "Show me open bugs" → linear
        - "What is divya working on ?" → linear
        - "Who pushed to main today?" → github
        - "What's assigned to Alex?" → linear

        Respond with exactly one word: github or linear or briefs
        """

agent = create_agent(
    model="gpt-4o",
    system_prompt= SYSTEM_PROMPT,
    response_format= DomainClassification
)

def classify_query(state: AgentState) -> dict:
    """Classsify query and determine which agent to invoke"""
    result = agent.invoke(
        {"messages": [{"role":"user", "content":state["query"]}]}
    )
    
    return {"domain":result["structured_response"].domain}


def routing_condition(state:AgentState) -> Literal["github", "linear"]:
    return state["domain"]
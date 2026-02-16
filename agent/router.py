from agent.state import AgentState, ClassificatonState
from langchain.agents import create_agent
from typing import Literal

SYSTEM_PROMPT = """
        You are a query classifier. Classify the user's question into ONE category.

        Categories:
        - git: commits, pushes, history, changes, who wrote what
        - linear: issues, bugs, tasks, assignments, status, who's working on what

        Examples:
        - "What did Sarah commit?" → git
        - "What was Divya working on?" → git
        - "Show me open bugs" → linear
        - "What is divya working on ?" → linear
        - "Who pushed to main today?" → git
        - "What's assigned to Alex?" → linear

        Respond with exactly one word: git or linear
        """

agent = create_agent(
    model="gpt-3.5-turbo",
    system_prompt= SYSTEM_PROMPT,
    response_format=ClassificatonState
)

def classify_query(state: AgentState) -> ClassificatonState:
    """Classsify query and determine which agent to invoke"""

    print(f"Agent states at query classifier {state}")

    response = agent.invoke(
        {"messages": [{"role":"user", "content":state["query"]}]}
    )

    return {"source": response["structured_response"]["source"]}


def routing_condition(state:ClassificatonState) -> Literal["git", "linear"]:
    return state["source"]
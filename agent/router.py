from agent.state import AgentState, ClassificatonState
from langchain.agents import create_agent
from typing import Literal

SYSTEM_PROMPT = """
        You are a query classifier. Classify the user's question into ONE category.

        Categories:
        - git: commits, pushes, history, changes, who wrote what
        - tickets: issues, bugs, tasks, assignments, status, who's working on what
        - code: find code, search files, where is X implemented

        Examples:
        - "What did Sarah commit?" → git
        - "What was Divya working on?" → git
        - "Show me open bugs" → tickets
        - "Where is the auth logic?" → code
        - "Who pushed to main today?" → git
        - "What's assigned to Alex?" → tickets

        Respond with exactly one word: git, code, or tickets
        """

agent = create_agent(
    model="gpt-3.5-turbo",
    system_prompt= SYSTEM_PROMPT,
    response_format=ClassificatonState

)

def classify_query(state: AgentState) -> ClassificatonState:
    """Classsify query and determine which agent to invoke"""

    print(f"The state is {state}")
    response = agent.invoke(
        {"messages": [{"role":"user", "content":state["query"]}]}
    )

    print(f"Response is {response}")
    return {"source": response["structured_response"]["source"]}


def routing_condition(state:ClassificatonState) -> Literal["git", "code", "tickets"]:
    return state["source"]
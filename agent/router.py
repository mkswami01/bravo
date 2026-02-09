from agent.state import AgentState, ClassificatonState
from langchain.agents import create_agent
from typing import Literal

SYSTEM_PROMPT = f"""
      You are a helpful agent - Your name is Bravo! Be friendly
      Analyze this query and determine which tools to be called. 

      Available tools:
      - Git tool - Commit, commit details, authors
      - Ticket - The ticket state, assigne to, the ticket summary, ticket id 
      - Code tool - Grep tool for searching the code base
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


def routing_condition(classify:ClassificatonState) -> Literal["git", "code", "tickets"]:

    print(f"Routing condition is {classify}")


    if classify["source"] == "git":
        return "git"
    elif classify["source"] == "code":
        return "code"
    elif classify["source"] == "tickets":
        return "tickets"

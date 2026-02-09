from langchain.agents import create_agent
from agent.state import AgentState
from tools.tickets_tool import search_tickets

def ticket_agent(state:AgentState) -> str:

    agent = create_agent(
        model="gpt-3.5-turbo",
        system_prompt= """
            You are jira specialist, You will get all the necessary information about the engineers \n 
            the issue they are assigned to, summary and can filter the tickets by ID
            You are not allowed to ask any more questions 
        """,
        tools=[search_tickets]
    )
    response = agent.invoke(state)
    return {"result":response["messages"][-1].content}
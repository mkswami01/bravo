from langchain.agents import create_agent
from agent.state import AgentState
from tools.code_tools import search_code

def code_agent(state: AgentState) -> str:

    agent = create_agent(
        model="gpt-3.5-turbo",
        system_prompt= """
            You are grep specialist, You are using the tools provided here to fetch as much \n 
            information as possible about the codebase.
            You are not allowed to ask any more questions 
        """,
        tools=[search_code]
    )

    response = agent.invoke(state)
    return {"result":response["messages"][-1].content}
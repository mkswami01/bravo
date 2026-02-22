from langchain.agents import create_agent
from agent.state import AgentState
from tools.briefs import daily_brief


def briefs(state:AgentState) -> dict:

    agent = create_agent(
        model="gpt-4o", 
        system_prompt="""
            You are an assitant to startup CTO.
            Your job is to send a daily brief based on the git commits, pull requests and the issues that were addressed.
            """,
        tools=[daily_brief]
    )

    response = agent.invoke({"messages": [{"role":"user", "content":state["query"]}]})
    
    return {"result":response["messages"][-1].content}

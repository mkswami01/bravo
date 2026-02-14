from langchain.agents import create_agent
from agent.state import AgentState
from tools.github_tools import get_commits

def git_agent(state:AgentState) -> str:

    print(f"Agent is here {state}")
    agent = create_agent(
        model="gpt-3.5-turbo", 
        system_prompt="""
            You are a git specialist, you have access to the github tool to fetch commits 
            You can also filter based by authors who have commited.

            Take a look at the work done, summarize the work and also keep the details
        """,
        tools=[get_commits]
    )

    response = agent.invoke({"messages": [{"role":"user", "content":state["query"]}]})
    
    return {"result":response["messages"][-1].content}
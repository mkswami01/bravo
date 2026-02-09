from langchain.agents import create_agent
from agent.state import AgentState
from tools.git_tools import git_log

def git_agent(state:AgentState) -> str:
    agent = create_agent(
        model="gpt-3.5-turbo", 
        system_prompt="""
            You are a git specialist, you have access to the git tool
            You provide the necessary arguements to filter and fetch necessary commits
            You are not allowed to ask any more questions or followups
        """,
        tools=[git_log]
    )

    response = agent.invoke(state)

    return {"result":response["messages"][-1].content}
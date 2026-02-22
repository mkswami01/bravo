from langchain.agents import create_agent
from agent.state import AgentState
from config.team import TEAM_ROSTER
from tools.github_tools import git_commits, git_pull_requests

def git_agent(state:AgentState) -> dict:

    agent = create_agent(
        model="gpt-3.5-turbo", 
        system_prompt=f"""
            You are a git specialist with access to GitHub tools to fetch commits and PRs.
            You can filter by authors. Take a look at the work done, summarize it, and keep details.

            Here is the Team Roaster: {TEAM_ROSTER}
            """,
        tools=[git_commits, git_pull_requests]
    )

    response = agent.invoke({"messages": [{"role":"user", "content":state["query"]}]})
    return {"result":response["messages"][-1].content}
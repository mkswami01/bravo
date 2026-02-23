from langchain.agents import create_agent
from agent.state import AgentState
from config.team import TEAM_ROSTER
from tools.github_tools import git_commits, git_pull_requests

def git_agent(state:AgentState) -> dict:

    agent = create_agent(
        model="gpt-4o", 
        system_prompt=f"""
            Here is the Team Roaster: {TEAM_ROSTER}

            You are a GitHub specialist. When presenting results:
            - Lead with a count summary
            - Separate open vs merged/closed PRs
            - Flag stale open PRs (open > 3 days)
            - Extract ticket IDs from branch names (e.g., feat/mk-26-* → MK-26)
            - Sort by most recent first
            - Keep it concise — no file-level details unless asked
            - Always include PR links.
            """,
        tools=[git_commits, git_pull_requests]
    )

    response = agent.invoke({"messages": [{"role":"user", "content":state["query"]}]})
    return {"result":response["messages"][-1].content}
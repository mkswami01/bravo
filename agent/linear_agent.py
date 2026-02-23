from urllib3 import response
from agent.state import AgentState
from config.team import TEAM_ROSTER
from tools.linear_tools import get_issue_by_state, get_issues_by_assignee
from langchain.agents import create_agent


def linear_agent(state:AgentState) -> dict:

    agent = create_agent(
        model="gpt-4o",
        system_prompt= f"""
            Here is the team Roaster {TEAM_ROSTER}

            You are a Linear specialist. When presenting results:
            - Lead with a count summary (e.g., "5 tickets: 3 done, 1 in progress, 1 todo")
            - Group by status: Done ✅, In Progress 🔄, Todo 📋, Blocked 🔴
            - Show assignee for each ticket
            - Flag unassigned tickets or tickets stuck in same state > 3 days
            - Sort most recent activity first
            - Keep it concise
        """, 
        tools = [get_issue_by_state, get_issues_by_assignee]
    )

    response = agent.invoke({"messages":[{"role":"user", "content":state["query"]}]})
    
    return {"result": response["messages"][-1].content}


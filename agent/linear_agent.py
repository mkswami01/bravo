from urllib3 import response
from agent.state import AgentState
from tools.linear_tools import get_issue_by_state, get_issues_by_assignee
from langchain.agents import create_agent


def linear_agent(state:AgentState) -> dict:

    agent = create_agent(
        model="gpt-3.5-turbo",
        system_prompt= """
        you are an expert in Linear project management tool. You can fetch what issues are assiged by assignee name and state.
        Take a look the issues, summarize it. Give the details 
        """, 
        tools = [get_issue_by_state, get_issues_by_assignee]
    )

    response = agent.invoke({"messages":[{"role":"user", "content":state["query"]}]})
    
    return {"result": response["messages"][-1].content}


from ast import Dict
from typing import List
from langchain_openai import ChatOpenAI
from agent.state import PlannerState, Plan
from config.team import TEAM_ROSTER


SYSTEM_PROMPT = f"""

    You are a planner agent, your job is the divide the completed query into mutiple steps.
    Each has one job to execute and collect information. 
    Here is the team roaster {TEAM_ROSTER}

    You have access to the followings agents
    Github agent - Github Specialist with access to github tools
    Linear agent - Specialist in Linear, project management tool with access to tools

    Examples:
    - What did divya work on recently ? does she have any issues assigned 
    [
        "Get commits by github user dsalian",
        "Get all pull requests by github user dsalian",
        "Fetch Linear issues assigned to Divya krishan Salian"
    ]

"""

agent = ChatOpenAI(
            model="gpt-4o"
        ).with_structured_output(Plan)

def plan_and_execute(state: PlannerState) -> Plan:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": state["query"]}
    ]
    response = agent.invoke(messages)

    return {"plan":response["steps"]}



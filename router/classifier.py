from agent.state import AgentState, ClassificationState
from langchain.agents import create_agent
from typing import Literal

from models import classifier
from models.classifier import Classification

SYSTEM_PROMPT = f"""
        You are a query classifier. Classifier the user question into 
        1. If it s a simple of a complex query  
        2. Classifiy each query into a ONE category

        - complexity: "simple" if it needs one data source, "complex" if it needs multiple sources or cross-referencing
        - domain: "github" or "linear" if simple, null if complex

        domain:
        - git: commits, pushes, history, changes, who wrote what
        - linear: issues, bugs, tasks, assignments, status, who's working on what

        Examples:
        - "What did Sarah commit?" → {{"domain":"github", "complexity":"simple"}}
        - "What was Divya working on?" → {{"domain":"github", "complexity":"simple"}}
        - "Show me open bugs" → {{"domain":"linear", "complexity":"simple"}}
        - "What's assigned to Alex?" → {{"domain":"linear", "complexity":"simple"}}
        - "what work is assigned to Divya ? and How many Pull request did she take care ?" → {{"domain":null, "complexity":"complex"}}
        - "Give me a overview of mkumars assigned and completed work" → {{"domain":null, "complexity":"complex"}}
        """

agent = create_agent(
    model="gpt-4o",
    system_prompt= SYSTEM_PROMPT,
    response_format=Classification
)

def classify_query(state: ClassificationState) -> ClassificationState:
    """Classsify query and determine which agent to invoke"""


    result = agent.invoke(
        {"messages": [{"role":"user", "content":state["query"]}]}
    )

    if result["structured_response"]:
        state["complexity"] = result["structured_response"].complexity
        state["domain"] = result["structured_response"].domain
    return state


def routing_condition(state:ClassificationState)->str:
    if state["complexity"] == "complex":
        return "planner"        
    elif state["complexity"] == "simple":
        return "react"
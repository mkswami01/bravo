from typing import List, Literal, Optional, TypedDict

from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    """The input and output state for the subagents"""
    query: str
    result: str
    source: str

class ClassificatonState(TypedDict):
    """Routing classification on what agent to be called"""
    source: Literal["git", "linear", "briefs", "planner"]

class PlannerState(TypedDict):
    """
        Planner state taht
    """
    query: str
    plan: Plan
    results: List[str]
    result: str

class Plan(TypedDict):
    steps:List[str]
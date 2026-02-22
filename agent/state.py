from typing import List, Literal, Optional, TypedDict

from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    """The input and output state for the subagents"""
    query: str
    result: str
    domain: str

class ClassificationState(TypedDict):
    query: str
    domain: str
    complexity: str

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
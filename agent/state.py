from typing import Literal, TypedDict

class AgentState(TypedDict):
    """The input and output state for the subagents"""
    query: str
    result: str
    source: str

class ClassificatonState(TypedDict):
    """Routing classification on what agent to be called"""
    source: Literal["git", "linear", "briefs"]
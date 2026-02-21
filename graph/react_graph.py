from langgraph.graph.state import START, END, StateGraph
from agent.briefs import briefs
from agent.git_agent import git_agent
from agent.linear_agent import linear_agent
from agent.router import classify_query, routing_condition
from agent.state import AgentState

class Agent:

    def __init__(self) -> None:
        builder = StateGraph(AgentState)
        builder.add_node("classifier", classify_query)
        builder.add_node("git", git_agent)
        builder.add_node("linear", linear_agent)
        builder.add_node("briefs", briefs)
        builder.add_edge(START, "classifier")
        builder.add_conditional_edges("classifier",routing_condition)
        builder.add_edge("git", END)
        builder.add_edge("linear", END)
        self.graph = builder.compile()
        
    def agent_execute(self, agent_state: AgentState) -> AgentState:
        self.graph.invoke(agent_state)
        return agent_state


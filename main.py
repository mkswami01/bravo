from dotenv import load_dotenv
from langchain_core.messages import AIMessage, ToolMessage
from langgraph.constants import END, START
from langgraph.graph.state import StateGraph
load_dotenv() 

from agent.linear_agent import linear_agent
from agent.git_agent import git_agent
from agent.router import classify_query, routing_condition
from agent.state import AgentState

builder = StateGraph(AgentState)
builder.add_node("classifier", classify_query)
builder.add_node("git", git_agent)
builder.add_node("linear", linear_agent)

builder.add_edge(START, "classifier")
builder.add_conditional_edges("classifier",routing_condition)
builder.add_edge("git", END)
builder.add_edge("linear", END)

graph = builder.compile()

def main():
   state = AgentState(query="What work is completed so far ?", result="", source="")

   response = graph.invoke(state)

   print(response["result"])


if __name__ == "__main__":
    main()

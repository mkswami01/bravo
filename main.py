from dotenv import load_dotenv
from langchain_core.messages import AIMessage, ToolMessage
from langgraph.constants import END, START
from langgraph.graph.state import StateGraph
load_dotenv() 

from agent.git_agent import git_agent
from agent.code_agent import code_agent
from agent.ticket_agent import ticket_agent
from agent.router import classify_query, routing_condition
from agent.state import AgentState

builder = StateGraph(AgentState)
builder.add_node("classifier", classify_query)
builder.add_node("git", git_agent)
builder.add_node("code", code_agent)
builder.add_node("tickets", ticket_agent)

builder.add_edge(START, "classifier")
builder.add_conditional_edges("classifier",routing_condition)
builder.add_edge("git", END)
builder.add_edge("code", END)
builder.add_edge("tickets", END)

graph = builder.compile()

def main():
   state = AgentState(query="Where is search_tickets defined?", result="", source="")

   response = graph.invoke(state)

   print(response)




if __name__ == "__main__":
    main()

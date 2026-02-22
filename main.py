from dotenv import load_dotenv
load_dotenv() 

from graph.plan_graph import PlanAndExecute
from graph.graph_initializer import Initializer
from agent.state import ClassificationState, PlannerState
from graph.react_graph import Agent


def main():
  
  state = ClassificationState(query="What was was recently completed by mkumar ? Does he have any tickets assigned ? In linear he might be referred to Manoj Kumar", domain="", complexity="")

  agent = Initializer()
  state = agent.run(state)

  if state["complexity"] == "complex":

    planner = PlannerState(query=state["query"], plan=[], results=[], result=[])
    pne = PlanAndExecute()
    final_state = pne.run(planner)
    print(f"User query : {final_state['query']}")
    print(f"{final_state["results"]}")

  elif state ["complexity"] == "simple":

    react_state = {"query": state["query"], "result": "", "domain": ""}
    react_agent = Agent()
    final_state = react_agent.run(react_state)

    print(f"User query : {final_state['query']}")
    print(f"{final_state["result"]}")

if __name__ == "__main__":
    main()

from dotenv import load_dotenv
load_dotenv() 

from graph.plan_graph import PlanAndExecute
from graph.graph_initializer import Initializer
from agent.state import ClassificationState, PlannerState
from graph.react_graph import Agent


def main():


  while True:
        query = input("Ask Bravo: I am your assistant, can fetch information about your engineers works")

        if query.strip() == "":
          pass
        if query.lower() in ["quit", "exit"]:
            break
  
        state = ClassificationState(query=query, domain="", complexity="")

        agent = Initializer()
        state = agent.run(state)

        if state["complexity"] == "complex":
          planner = PlannerState(query=state["query"], plan=[], results=[], result=[])
          pne = PlanAndExecute()
          final_state = pne.run(planner)
          print(f"User query : {final_state['query']}")

          print(f"The plan executed was {final_state['plan']}")

          print(f"{final_state["result"]}")

        elif state ["complexity"] == "simple":
          react_state = {"query": state["query"], "result": "", "domain": ""}
          react_agent = Agent()
          final_state = react_agent.run(react_state)

          print(f"User query : {final_state['query']}")
          print(f"{final_state["result"]}")

if __name__ == "__main__":
    main()

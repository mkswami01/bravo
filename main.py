from dotenv import load_dotenv
load_dotenv() 

from graph.plan_graph import PlanAndExecute
from graph.graph_initializer import Initializer
from agent.state import ClassificationState, PlannerState
from graph.react_graph import Agent
from rich.console import Console


def main():


  console = Console()

  console.print("I am Bravo 🐱 - your assistant. I can fetch information about your engineers works\nI have few Github and Linear tools handy, I can use them to get you relevanth information\n", style="yellow")

  while True:
        query = input()

        if query.strip() == "":
          continue
        if query.lower() in ["quit", "exit"]:
          break

        console.print(f"Query: {query}", style="bold magenta")
  
        state = ClassificationState(query=query, domain="", complexity="")

        console.print(f"Classifying the query", style="yellow")

        agent = Initializer()
        state = agent.run(state)

        if state["complexity"] == "complex":

          console.print(f"Query is classified as complex, we will use plan and execute graph", style="green")
          planner = PlannerState(query=state["query"], plan=[], results=[], result=[])
          pne = PlanAndExecute()
          final_state = pne.run(planner)
          
          console.print(f"{final_state["result"]}", style="green")

        elif state ["complexity"] == "simple":
          console.print(f"Query is classified as simple", style="green")
          react_state = {"query": state["query"], "result": "", "domain": ""}
          react_agent = Agent()
          final_state = react_agent.run(react_state)

          print(f"User query : {final_state['query']}")
          print(f"{final_state["result"]}")

if __name__ == "__main__":
    main()

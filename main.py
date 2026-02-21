from dotenv import load_dotenv
load_dotenv() 
   
from graph.plan_graph import PlanAndExecute
from agent.planner import plan_and_execute
from agent.briefs import briefs
from agent.linear_agent import linear_agent
from agent.git_agent import git_agent
from agent.router import SYSTEM_PROMPT, classify_query, routing_condition
from agent.state import AgentState, PlannerState


def main():
  
  state = PlannerState(query="what work was completed yesterday? How many tickets were done ?", plan=[], results=[], result="")

  agent = PlanAndExecute()
  agent.plan_and_execute(state)

  print(f"state \n {state}")


if __name__ == "__main__":
    main()

from langchain_openai import ChatOpenAI
from langgraph.graph.state import END, START, StateGraph
from agent import planner
from agent.planner import plan_and_execute
from agent.router import agent
from agent.state import AgentState, PlannerState
from graph.react_graph import Agent

class PlanAndExecute:

    plan = []
    def __init__(self) -> None:
        pne_builder = StateGraph(PlannerState)
        pne_builder.add_node("planner", plan_and_execute)
        pne_builder.add_edge(START, "planner")
        pne_builder.add_edge("planner", END)
        self.graph = pne_builder.compile();
        self.agent = Agent()

    def synthesize(self, results: list, state: PlannerState):

        agent = ChatOpenAI(
            model="gpt-4o"
        )

        SYSTEM_PROMPT = f"""
            The plan and execute agent have collected all the information together for the {state["query"]}

            Here is all the information collections - {results}
            your jobs is the summarize and give a breif intro about the work and keep all teh details as much as you can 
        """
        messages = [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": "Please summarize the above."}]
        response = agent.invoke(messages)

        state["result"] = response.content
       

    def plan_and_execute(self, planner_state: PlannerState):

        response = self.graph.invoke(planner_state)
        self.plan = response["plan"]
        planner_state["plan"] = self.plan

        results = []
        for i, step in enumerate(self.plan):
            state = AgentState(query=step, result="", source="")
            response = self.agent.agent_execute(state)
            results.append(response["result"])
        
        self.synthesize(results, planner_state)
        

        


            
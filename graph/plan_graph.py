from unittest import result
from langchain_openai import ChatOpenAI
from langgraph.graph.state import END, START, StateGraph
from agent import planner
from agent.planner import plan_and_execute
from agent.router import agent
from agent.state import AgentState, PlannerState
from config.team import TEAM_ROSTER
from graph.react_graph import Agent

class PlanAndExecute:

    def __init__(self) -> None:
        pne_builder = StateGraph(PlannerState)
        pne_builder.add_node("planner", plan_and_execute)
        pne_builder.add_node("execute", self.execute)
        pne_builder.add_node("synthesize", self.synthesize)

        pne_builder.add_edge(START, "planner")
        pne_builder.add_edge("planner", "execute")
        pne_builder.add_edge("execute", "synthesize")
        pne_builder.add_edge("synthesize", END)

        self.graph = pne_builder.compile()
        self.agent = Agent()

    def synthesize(self, state: PlannerState):

        agent = ChatOpenAI(
            model="gpt-4o"
        )

        SYSTEM_PROMPT = f"""
                    You are an engineering team analyst. 

                    Query: {state["query"]}
                    Results: {state['results']}
                    Team roster: {TEAM_ROSTER}

                    Branch naming convention: usually branches start with ticket ID (e.g., feat/mk-26-build-classifier → ticket MK-26)

                    Respond naturally based on what was asked.

                    Rules:
                        - Include links to PRs, commits, and tickets when available
                        - End with "Action Items" — what needs attention, prioritized by urgency
                        - Include metrics: count commits, PRs merged, tickets closed
                        - Use status indicators: ✓ for done, ⚠️ for needs attention, 🔴 for blocked
                        - Flag stale PRs, unassigned tickets, or missing cross-references
                        - Be concise. No filler. Every sentence should add information.
                        - Cross-reference GitHub and Linear data always.
                    """
        messages = [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": "Please summarize the above."}]
        response = agent.invoke(messages)

        return {"result": response.content}
       

    def run(self, pne_state: PlannerState):

        return self.graph.invoke(pne_state)
        
    def execute(self, pne_state: PlannerState) -> list:

        results = []
        for i, step in enumerate(pne_state["plan"]):
            react_state = {"query": step, "result": "", "domain": ""}
            react_agent = Agent()
            final_state = react_agent.run(react_state)
            results.append(final_state["result"])

        return {"results":results}
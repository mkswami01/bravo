from langgraph.graph.state import START, END, StateGraph

from agent.state import ClassificationState
from router.classifier import classify_query

class Initializer:

    def __init__(self) -> None:
        builder = StateGraph(ClassificationState)
        builder.add_node("classifier", classify_query)
        
        builder.add_edge(START,"classifier")
        builder.add_edge("classifier", END)
        self.graph = builder.compile()

    def run(self, state: ClassificationState) -> ClassificationState:

        try:
            return self.graph.invoke(state) 
        except Exception as e:
            print("Error classifying the query here")
            raise Exception("Error classifying the query")
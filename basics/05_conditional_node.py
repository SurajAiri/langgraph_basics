from langgraph.graph import StateGraph, START, END
from typing import TypedDict


class AgentState(TypedDict):  # schema for state
    """State for the agent"""

    num1: int
    num2: int
    operation: str
    result: int


def adder(state: AgentState) -> AgentState:
    """This is a simple adder node"""
    state['result'] = state['num1'] + state['num2']
    return state

def subtractor(state: AgentState) -> AgentState:
    """This is a simple subtractor node"""
    state['result'] = state['num1'] - state['num2']
    return state


def operation_router(state: AgentState) -> str:
    """This node routes to adder or subtractor based on the operation"""
    if state['operation'] == '+':
        return 'adder'
    if state['operation'] == '-':
        return 'subtractor'
    raise ValueError(f"Unknown operation: {state['operation']}")

graph = StateGraph(AgentState)

graph.add_node("adder", adder)
graph.add_node("subtractor", subtractor)
# graph.add_node("operation_router", lambda state:state) # pass through node

# graph.add_edge(START, "operation_router")

graph.add_conditional_edges(

    START, 
    operation_router,
    {
        "adder": "adder",
        "subtractor": "subtractor"
    }
)

graph.add_edge("adder", END)
graph.add_edge("subtractor", END)

app = graph.compile()

from IPython.display import Image, display
# Use format="png" for better quality and set options to show edge labels
display(Image(app.get_graph().draw_mermaid_png()))

res = app.invoke({"num1": 10, "num2": 5, "operation": "+"})
print(res)  # {'num1': 10, 'num2': 5, 'operation': '+', 'result': 15}
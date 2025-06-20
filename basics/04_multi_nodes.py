from typing import TypedDict

from langgraph.graph import END, START, StateGraph


class AgentState(TypedDict):  # schema for state
    """State for the agent"""

    name: str
    output: str


def greeting_node(state: AgentState) -> AgentState:
    """This is a simple greeting node"""
    state["output"] = f"hey {state['name']}, how are you?"
    return state


def compliment_node(state: AgentState) -> AgentState:
    """This is a simple compliment node"""
    state["output"] += f" hey {state['name']}, You really have a great name!"
    return state


graph = StateGraph(AgentState)

graph.add_node("greeting", greeting_node)
graph.add_node("compliment", compliment_node)

graph.add_edge(START, "greeting")
graph.add_edge("greeting", "compliment")
graph.add_edge("compliment", END)

app = graph.compile()
from IPython.display import Image, display

display(Image(app.get_graph().draw_mermaid_png()))

res = app.invoke({"name": "John"})
print(
    res
)  # {'name': 'John', 'output': 'hey John, how are you? hey John, You really have a great name!'}

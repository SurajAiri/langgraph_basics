from typing import TypedDict

from langgraph.graph import END, START, StateGraph


# creating a simple state
class AgentState(TypedDict):  # schema for state
    """State for the agent"""

    name: str
    output: str


def compliment_node(state: AgentState) -> AgentState:
    """This is a simple greeting node"""
    state["output"] = f"hey {state['name']}, You really have a great name!"
    return state


graph = StateGraph(AgentState)

graph.add_node("complimenter", compliment_node)


graph.add_edge(START, "complimenter")
graph.add_edge("complimenter", END)

app = graph.compile()


from IPython.display import Image, display

display(Image(app.get_graph().draw_mermaid_png()))

res = app.invoke({"name": "John"})
print(res)  # {'name': 'John', 'output': 'hey John, You really have a great name!'}
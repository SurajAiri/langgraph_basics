from typing import TypedDict

from langgraph.graph import END, START, StateGraph


# creating a simple state
class AgentState(TypedDict):  # schema for state
    """State for the agent"""

    message: str


def greeting_node(state: AgentState) -> AgentState:
    """This is a simple greeting node"""
    state["message"] = f"hey {state['message']}, how are you?"
    return state


graph = StateGraph(AgentState)

graph.add_node("greeter", greeting_node)

graph.set_entry_point("greeter")
graph.set_finish_point("greeter")


app = graph.compile()

from IPython.display import Image, display

display(Image(app.get_graph().draw_mermaid_png()))

res = app.invoke({"message": "John"})
print(res)  # {'message': 'hey John, how are you?'}

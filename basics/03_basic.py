from typing import TypedDict

from langgraph.graph import END, START, StateGraph


class AgentState(TypedDict):  # schema for state
    """State for the agent"""

    name: str
    values: list[int]
    operation: str
    result: str


def performer(state: AgentState) -> AgentState:
    """This is a simple performer node"""

    state["result"] = f"Hey {state['name']}, "

    if state["operation"] == "+":
        state["result"] += f"the sum of your values is {sum(state['values'])}."
    elif state["operation"] == "*":
        product = 1
        for value in state["values"]:
            product *= value
        state["result"] += f"the product of your values is {product}."
    else:
        state["result"] += "I don't know how to perform that operation."

    return state


graph = StateGraph(AgentState)

graph.add_node("performer", performer)

graph.add_edge(START, "performer")
graph.add_edge("performer", END)

app = graph.compile()

from IPython.display import Image, display

display(Image(app.get_graph().draw_mermaid_png()))


res = app.invoke({"name": "John", "values": [1, 2, 3], "operation": "+"})
print(res)

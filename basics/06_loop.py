from langgraph.graph import StateGraph, START, END
from typing import TypedDict        

class AgentState(TypedDict):  # schema for state
    """State for the agent"""
    count: int
    output: str



def counting_node(state: AgentState) -> AgentState:
    """This is a simple counting node"""
    state['count'] += 1
    state['output'] += "Hi dejabu, "
    return state

def loop_condition(state: AgentState) -> bool:
    """Condition to continue looping"""
    return state['count'] < 5


graph = StateGraph(AgentState)

graph.add_node("counting", counting_node)

graph.add_edge(START, "counting")
graph.add_conditional_edges("counting", loop_condition, {True: "counting", False: END})

app = graph.compile()

from IPython.display import Image, display
display(Image(app.get_graph().draw_mermaid_png()))

res = app.invoke({"count": 0, "output": ""})
print(res)  # {'count': 5, 'output': 'Hi dejabu, Hi dejabu, Hi dejabu, Hi dejabu, Hi dejabu, '}
from typing import Annotated, TypedDict

from dotenv import load_dotenv
from langchain_core.messages import AIMessage, BaseMessage
from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages


class LoopState(TypedDict):
    count:int 
    message: str


def action(state:LoopState)->LoopState:
    state['count'] = state['count'] + 1
    state['message'] = (state['message'] + " hi").strip()
    return state

def even_action(state: LoopState)->LoopState:
    state['count'] = state['count'] + 1
    state['message'] = (state['message'] + " hey").strip()
    return state

def condition(state:LoopState)->str:
    if state['count'] > 5:
        return "exit"
    
    if state['count'] % 2 == 0:
        return "even"
    
    return "action"

state = StateGraph(LoopState)


state.add_node("action",action)
state.add_node("action_even",even_action)

# edges
state.add_edge(START,"action")
state.add_conditional_edges("action",condition, 
                            {"action":"action","exit":END,"even":"action_even"})
state.add_conditional_edges("action_even",condition, 
                            {"action":"action","exit":END,"even":"action_even"})

app = state.compile()

# render
from IPython.display import display, Image
display(Image(app.get_graph().draw_mermaid_png()))

app.invoke({"count":1,'message':""})


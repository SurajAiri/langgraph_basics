from typing import Annotated, TypedDict

from dotenv import load_dotenv
from langchain_core.messages import AIMessage, BaseMessage
from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages

load_dotenv()

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0.4,
)


def chat_node(state: ChatState) -> ChatState:
    return {"messages": [
        AIMessage(llm.invoke(state["messages"][-1].content).content)
        ]}


graph = StateGraph(ChatState)

graph.add_node("chat_node",chat_node)

graph.add_edge(START,"chat_node")
graph.add_edge("chat_node",END)

app = graph.compile()

# Visualize
from IPython.display import display, Image
display(Image(app.get_graph().draw_mermaid_png()))
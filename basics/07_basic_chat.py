from typing import TypedDict

from dotenv import load_dotenv
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
from langgraph.graph import END, START, StateGraph

load_dotenv()


llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0.4,
)


class ChatState(TypedDict):
    """State for the chat agent"""

    messages: list[BaseMessage]


def chat_node(state: ChatState) -> ChatState:
    """Node to handle chat messages"""
    if len(state["messages"]) < 5:
        response = llm.invoke(state["messages"])
    else:
        response = llm.invoke(state["messages"][-5:-1])
    state["messages"].append(AIMessage(content=response.content))
    return state


# Define the state graph
graph = StateGraph(ChatState)

# define nodes
graph.add_node("chat", chat_node)

# define edges
graph.add_edge(START, "chat")
graph.add_edge("chat", END)

# compile the graph
app = graph.compile()

# view the graph
from IPython.display import Image, display

display(Image(app.get_graph().draw_mermaid_png()))


# Run the app
user_input = input("You: ")

state = ChatState(messages=[SystemMessage(content="You are a helpful assistant.")])
while user_input.lower() not in ["exit", "quit", "bye", "q"]:
    state["messages"].append(HumanMessage(content=user_input))
    state = app.invoke(state)
    print(f"AI: {state['messages'][-1].content}")
    user_input = input("You: ")

from typing import Annotated, TypedDict

from dotenv import load_dotenv
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
from langgraph.graph import END, START, StateGraph, add_messages

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0.4,
)

class ChatState(TypedDict):
    """State for the chat agent"""

    # messages: list[BaseMessage]
    messages: list[BaseMessage]


# def chat_node(state: ChatState) -> ChatState:
#     """Node to handle chat messages"""
#     # Print state with green color
#     print("\033[92m", state, "\033[0m")
#     ai_msg = AIMessage(content=llm.invoke(state["messages"]).content)
#     return {"messages":[ai_msg]}

def chat_node(state: ChatState) -> ChatState:
    print("\033[92m", state, "\033[0m")

    # Let LangGraph handle appending this using `add_messages`
    ai_msg = AIMessage(content=llm.invoke(state["messages"]).content)
    state["messages"].append(ai_msg)
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

# # # view the graph
# from IPython.display import display, Image
# display(Image(app.get_graph().draw_mermaid_png()))




def stream_graph_updates(user_input: str):
    for event in app.stream({"messages": [HumanMessage(content=user_input)]}):
        for value in event.values():
            print("Assistant:", value["messages"][-1].content)


while True:
    try:
        user_input = input("User: ")
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break
        stream_graph_updates(user_input)
    except Exception as e:
        print(f"An error occurred: {e}")
        break
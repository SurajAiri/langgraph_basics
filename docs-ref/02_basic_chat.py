from typing import Annotated, TypedDict
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
from langgraph.graph import END, START, StateGraph, add_messages

load_dotenv()

# Initialize LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0.4,
)

# Define the state
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

# Node function
def chat_node(state: ChatState) -> ChatState:
    print("\n📥 State before response:")
    for msg in state["messages"]:
        print(f"- {msg.type}: {msg.content}")

    # Call LLM and wrap response
    response = llm.invoke(state["messages"])
    return {"messages": [AIMessage(content=response.content)]}

# Define the graph
graph = StateGraph(ChatState)
graph.add_node("chat", chat_node)
graph.add_edge(START, "chat")
graph.add_edge("chat", END)
app = graph.compile()

# 🔁 Conversation memory outside the graph
conversation_state = {"messages": []}

# Streaming response
def stream_graph_updates(user_input: str):
    conversation_state["messages"].append(HumanMessage(content=user_input))

    for event in app.stream(conversation_state):
        for value in event.values():
            ai_msg = value["messages"][-1]
            print("\n🤖 Assistant:", ai_msg.content)

            # Persist the new AI message
            conversation_state["messages"].append(ai_msg)

# Loop
print("💬 Gemini Chat. Type 'exit' to quit.\n")
while True:
    try:
        user_input = input("👤 You: ")
        if user_input.lower() in ["exit", "quit", "q"]:
            print("👋 Goodbye!")
            break
        stream_graph_updates(user_input)
    except Exception as e:
        print(f"❌ Error: {e}")
        break

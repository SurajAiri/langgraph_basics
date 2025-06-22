from langchain_google_genai.chat_models import ChatGoogleGenerativeAI


def main():
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash",temperature=0.4)
    res = llm.invoke("What is the capital of France?")
    print(res.content)

if __name__ == "__main__":
    main()

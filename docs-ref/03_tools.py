from langchain_tavily import TavilySearch

tool = TavilySearch(max_results=2)
tools = [tool]
tool.invoke("What's a 'node' in LangGraph?")


print("\033[90mThis is grey text\033[0m")
print("\033[91mThis is red text\033[0m")
print("\033[92mThis is green text\033[0m")
print("\033[93mThis is yellow text\033[0m")
print("\033[94mThis is blue text\033[0m")
print("\033[95mThis is magenta text\033[0m")
print("\033[96mThis is cyan text\033[0m")
print("This is default text color")

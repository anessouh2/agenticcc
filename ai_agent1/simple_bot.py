from typing import TypedDict
from langgraph.graph import StateGraph ,START ,END
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()
class AgentState(TypedDict):
    messages : list[HumanMessage]

llm = ChatOpenAI(model="gpt-4o", api_key=api_key)

def process(state:AgentState)->AgentState:
    response=llm.invoke(state["messages"])
    print(f"\nAI : {response.content}")
    return state

graph = StateGraph(AgentState)
graph.add_node("process", process)
graph.add_edge(START , "process")
graph.add_edge("process" , END)
agent = graph.compile()

user_input = input("ENTER : ")

while user_input != "exit":
    agent.invoke({"messages" : [HumanMessage(content=user_input)]})
    user_input = input("ENTER : ") 
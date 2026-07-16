from typing import TypedDict
from langgraph.graph import StateGraph ,START ,END
from langchain_core.messages import HumanMessage
from langchain_groq import ChatGroq 
from dotenv import load_dotenv

load_dotenv()
class AgentState(TypedDict):
    messages : list[HumanMessage]

llm = ChatGroq(
    model="llama-3.3-70b-versatile"
)
def process(state:AgentState)->AgentState:
    response=llm.invoke(state["messages"])
    print(f"\nAI : {response.content}")
    return {
        "messages":state["messages"] + [response]
    }

graph = StateGraph(AgentState)
graph.add_node("process", process)
graph.add_edge(START , "process")
graph.add_edge("process" , END)
agent = graph.compile()

user_input = input("ENTER : ")

while user_input != "exit":
    
    agent.invoke({"messages" : [HumanMessage(content=user_input)]})
    
    user_input = input("ENTER :  ") 
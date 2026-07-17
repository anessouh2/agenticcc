import os
import warnings
from typing import TypedDict , Union , List
from langgraph.graph import StateGraph , START , END
from langchain_core.messages import HumanMessage , AIMessage
from dotenv import load_dotenv
from langchain_groq import ChatGroq

warnings.filterwarnings(
    "ignore",
    message=r".*default value of `allowed_objects` will change in a future version.*",
)

load_dotenv()

class AgentState(TypedDict):
    messages : List[Union[HumanMessage , AIMessage]]

llm = ChatGroq(model="llama-3.3-70b-versatile")

def process(state:AgentState) -> AgentState:
    """this is the node oc chatbot"""
    response = llm.invoke(state["messages"])

    state["messages"].append(AIMessage(content = response.content))
    print(f"\n AI : {response.content}")

    return state

graph = StateGraph(AgentState)
graph.add_node("process", process)
graph.add_edge(START , "process")
graph.add_edge("process" , END)
agent = graph.compile()

conversation_history =[]
user_input = input("enter :")
while user_input.lower() !="exit":
    conversation_history.append(HumanMessage(content=user_input))
    result = agent.invoke({"messages" : conversation_history})
    print(result["messages"])
    conversation_history = result["messages"]
    user_input = input("enter :")
with open("logging,txt" , "w") as file:
    file.write("Your conversation Log  :\n ")
    for message in conversation_history:
        if isinstance(message , HumanMessage):
            file.write(f"You : {message.content}\n") 
        elif isinstance(message , AIMessage):
            file.write(f"AI : {message.content}\n")
    file.write("END of conversation ")        

print("conversation saved to logging.txt")




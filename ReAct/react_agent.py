from typing import Annotated , TypedDict , Sequence
from dotenv import load_dotenv
from langgraph.graph import StateGraph ,START ,END
from langchain_core.messages import BaseMessage # all messages inherites from this  
from langchain_core.messages import ToolMessage # the result of tool wrapped inside his toolmessage after that returned to llm
from langchain_core.messages import SystemMessage #this tell the llm how o behave ex : you are helpful assistant
from langchain_groq import ChatGroq
from langchain_core.tools import tool #tools are python functions and they named tools becaus the llm can call them and use them 
from langgraph.graph.message import add_messages #is a reducer instead of replacing old messages it appends
from langgraph.prebuilt import ToolNode #without this we should execute tools by oourselfs so this execute tools

load_dotenv()

class AgentState(TypedDict):
    messages : Annotated[Sequence[BaseMessage] , add_messages]

@tool
def add(a:int , b :int ):
    """this is an addition fnction that adds 2 numbers together  """
    return a+b 

@tool 
def subtract(a:int , b :int)  :
    """subtraction function"""
    return a - b 

@tool 
def multiply(a:int , b :int)  :
    """mutlitplication function"""
    return a*b 

tools = [add , subtract , multiply]

llm = ChatGroq(model="llama-3.3-70b-versatile")

def llm_call(state:AgentState) ->AgentState:
    system_prompt= SystemMessage(content="" \
    "You are my AI assistant , please answer my query to the best of your ability . ")
    response = llm.invoke([system_prompt] + state["messages"])
    return{"messages" : [response]}
def should_continue(state : AgentState):
    messages = state["messages"]
    last_meassge = messages[-1]
    if not last_meassge.tool_calls:
        return "end"
    else :
        return "continue"
    
graph = StateGraph(AgentState)
graph.add_node("our_agent" , llm_call)
tool_node = ToolNode(tools = tools)
graph.add_node("tools", tool_node)

graph.add_edge(START , "our_agent")

graph.add_conditional_edges(
    "our_agent" , 
    should_continue,
    {
        "continue" : "tools" , 
        "end" : END

    },
)
graph.add_edge("tools" , "our_agent")

app = graph.compile()

def print_stream(stream):
    for s in stream:
        message = s["messages"][-1]
        if isinstance(message, tuple):
            print(message)
        else:
            message.pretty_print()

inputs = {"messages": [("user", "Add 40 + 12 and then multiply the result by 6. Also tell me a joke please.")]}
print_stream(app.stream(inputs, stream_mode="values"))


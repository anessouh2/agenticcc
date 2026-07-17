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


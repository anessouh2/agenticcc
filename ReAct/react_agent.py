from typing import Annotated , TypedDict , Sequence
from dotenv import load_dotenv
from langgraph.graph import StateGraph ,START ,END
from langchain_core.messages import BaseMessage
from langchain_core.messages import ToolMessage
from langchain_core.messages import SystemMessage
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

load_dotenv()

class AgentState(TypedDict):
    messages : Annotated[Sequence[BaseMessage] , add_messages]
    

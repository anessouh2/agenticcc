import os
from dotenv import load_dotenv
from typing import TypedDict , Union , Sequence 
from langgraph.graph import StateGraph , END , START
from langchain_core.messages import SystemMessage , HumanMessage , BaseMessage , AIMessage , ToolMessage
from langchain_core.tools import tool 
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langchain_mistralai import ChatMistralAI
from langchain_mistralai import MistralAIEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader

load_dotenv() 

llm = ChatMistralAI(
    model="mistral-small-latest" , 
    temperature=0
)
embeddings = MistralAIEmbeddings(
    model="mistral-small-latest"
)

pdf_path = "Stock_Market_Performance_2024.pdf"


if not os.path.exists(pdf_path):
    raise FileNotFoundError(f"PDf file not found : {pdf_path}")

pdf_loader = PyPDFLoader(pdf_path)
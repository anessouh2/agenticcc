import os 
from dotenv import load_dotenv
from typing import  Annotated , Union , TypedDict , Sequence
from langgraph.graph import StateGraph , START , END
from langchain_core.messages import BaseMessage , HumanMessage , SystemMessage , AIMessage
from langchain_mistralai import ChatMistralAI , MistralAIEmbeddings
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
  model="mistral-small-latest", 
  temperature= 0
)
embeddings = MistralAIEmbeddings(
    model="mistral-embed"
)

pdf_path = ""

if not os.path.exists(pdf_path):
    raise FileNotFoundError(f"PDF file not found : {pdf_path}")

pdf_loader = PyPDFLoader(pdf_path)

try :
    pages = pdf_loader.load()
    print(f" pdf has been loaded and has {len(pages)} pages")
except Exception as e:
    print(f"ERROR loading pdf : {e}")
    raise 

#chunking process

tex
# knowledge_base_builder.py
import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.document_loaders import TextLoader, DirectoryLoader

# Load this document as base knowledge
# Load college website content
# Create embeddings and store in Chroma
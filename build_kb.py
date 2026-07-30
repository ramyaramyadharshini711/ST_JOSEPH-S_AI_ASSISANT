import shutil
import os
import logging
from dotenv import load_dotenv

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

if os.path.exists("./chroma_db"):
    shutil.rmtree("./chroma_db")

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def build_vector_store():

    if os.path.exists("./chroma_db"):
        shutil.rmtree("./chroma_db")

    logger.info("Loading documents...")
    
def load_documents():
    docs = []
    kb_folder = "knowledge_base"

    if not os.path.exists(kb_folder):
        os.makedirs(kb_folder)
        logger.error(f"Please create '{kb_folder}' and add your .txt files.")
        return []

    for file in os.listdir(kb_folder):
        if file.endswith(".txt"):
            file_path = os.path.join(kb_folder, file)

            try:
                loader = TextLoader(file_path, encoding="utf-8")
                docs.extend(loader.load())
                logger.info(f"Loaded: {file}")

            except Exception as e:
                logger.error(f"Error loading {file}: {e}")

    return docs


def build_vector_store():

    logger.info("Loading documents...")

    documents = load_documents()

    if not documents:
        logger.error("No documents found!")
        return

    logger.info(f"Loaded {len(documents)} document(s)")

    splitter = RecursiveCharacterTextSplitter(
    chunk_size=700,
    chunk_overlap=150,
    separators=[
        "\n\n",
        "\n",
        ". ",
        ", ",
        " "
    ]
)

    chunks = splitter.split_documents(documents)

    logger.info(f"Created {len(chunks)} chunks")

    logger.info("Loading embedding model...")

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    logger.info("Creating Chroma database...")

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory="./chroma_db"
    )

    vectorstore.persist()

    logger.info("Knowledge Base Created Successfully!")

    return vectorstore


if __name__ == "__main__":
    build_vector_store()
    print("Knowledge Base Built Successfully!") 
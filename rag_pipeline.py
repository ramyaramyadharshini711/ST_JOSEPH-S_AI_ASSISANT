# rag_pipeline.py - RAG Pipeline with Groq & Gemini
import os
import logging
from typing import Dict, Any, Optional, Tuple
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RAGPipeline:
    def __init__(self, vectorstore_path="./chroma_db"):
        self.vectorstore_path = vectorstore_path
        self.vectorstore = None
        self.retriever = None
        self.groq_client = None
        self.gemini_available = False
        
        self._init_clients()
        self._load_vectorstore()
    
    def _init_clients(self):
        groq_api_key = os.getenv("GROQ_API_KEY")
        if groq_api_key and groq_api_key != "your_groq_api_key_here":
            try:
                from groq import Groq
                self.groq_client = Groq(api_key=groq_api_key)
                logger.info("✅ Groq client initialized")
            except Exception as e:
                logger.error(f"Failed to initialize Groq: {e}")
        else:
            logger.warning("⚠️ Groq API key not found")
        
        gemini_api_key = os.getenv("GEMINI_API_KEY")
        if gemini_api_key and gemini_api_key != "your_gemini_api_key_here":
            try:
                from google import genai
                genai.configure(api_key=gemini_api_key)

                self.gemini_model = genai.GenerativeModel(
                    "gemini-2.0-flash"
                )
                self.gemini_available = True
                logger.info("✅ Gemini client initialized")
            except Exception as e:
                logger.error(f"Failed to initialize Gemini: {e}")
        else:
            logger.warning("⚠️ Gemini API key not found")
    
    def _load_vectorstore(self):
        try:
            embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2",
                model_kwargs={'device': 'cpu'},
                encode_kwargs={'normalize_embeddings': True}
            )
            
            self.vectorstore = Chroma(
                persist_directory=self.vectorstore_path,
                embedding_function=embeddings
            )
            
            self.retriever = self.vectorstore.as_retriever(
                search_kwargs={"k": 8}
            )
            
            logger.info("✅ Vector store loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load vector store: {e}")
            logger.info("Run 'python build_kb.py' first to build the knowledge base")
    
    def query_groq(self, context: str, question: str) -> Optional[str]:
        if not self.groq_client:
            return None
        
        try:
            prompt = f"""
            You are an AI Assistant for St. Joseph's College for Women, Tiruppur.

            Answer the user's question using the given context.

            Rules:
            - Use ALL the information available in the context.
            - If the answer is only partially available, provide the available information.
            - Do NOT simply reply "I don't have that information" unless the context is completely unrelated.
            - Keep the answer clear and detailed.

            Context:
            {context}

            Question:
            {question}

            Answer:
            """
            
            response = self.groq_client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile",
                temperature=0.3,
                max_tokens=500
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Groq query failed: {e}")
            return None
    
    def query_gemini(self, context: str, question: str):
        if not self.gemini_available:
            return None

        try:
            prompt = f"""
                You are an AI Assistant for St. Joseph's College for Women, Tiruppur.

                Use the provided context to answer the user's question.

                Rules:
                - Give complete details from the context.
                - If only part of the answer exists, provide that part.
                - Do not say "I don't have information" unless nothing relevant exists.

                Context:
                {context}

                Question:
                {question}

                Answer:
                """

            response = self.gemini_model.generate_content(prompt)
            return response.text

        except Exception as e:
            logger.error(f"Gemini query failed: {e}")
            return None
    
    def query(self, question: str) -> Tuple[str, str, list]:
        if not self.retriever:
            return (
                "⚠️ Knowledge base not loaded. Please run 'python build_kb.py' first.",
                "❌ Error",
                []
            )
        
        try:
            docs = self.retriever.invoke(question)
            if not docs:
                return (
                    "I don't have information about that in my knowledge base.",
                    "📚 No sources",
                    []
                )
                context = "\n\n".join(
                    doc.page_content[:2000] for doc in docs
                )
            
            answer = self.query_gemini(context, question)

            if answer:
                return answer, "🧠 Gemini", docs

            answer = self.query_groq(context, question)

            if answer:
                return answer, "🚀 Groq", docs
            
            return (
                "⚠️ All AI services are unavailable. Please check your API keys.",
                "❌ No API",
                docs
            )
        except Exception as e:
            logger.error(f"Query failed: {e}")
            return (
                f"⚠️ Error processing query: {str(e)}",
                "❌ Error",
                []
            )
    
    def get_status(self) -> Dict[str, Any]:
        return {
            "vectorstore_loaded": self.vectorstore is not None,
            "groq_available": self.groq_client is not None,
            "gemini_available": self.gemini_available,
            "retriever_ready": self.retriever is not None
        }

_pipeline_instance = None

def get_pipeline() -> RAGPipeline:
    global _pipeline_instance
    if _pipeline_instance is None:
        _pipeline_instance = RAGPipeline()
    return _pipeline_instance
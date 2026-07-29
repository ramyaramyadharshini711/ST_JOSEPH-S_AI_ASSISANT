import os
import streamlit as st
from dotenv import load_dotenv

# Load API keys
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Try to import APIs
try:
    from groq import Groq
    groq_available = True
except ImportError:
    groq_available = False

try:
    import google.generativeai as genai
    gemini_available = True
except ImportError:
    gemini_available = False

def query_groq(user_question):
    """Query Groq API for response"""
    if not groq_available:
        return None
    
    try:
        client = Groq(api_key=GROQ_API_KEY)
        # Combine college info with user question for context
        full_prompt = f"""You are a helpful assistant for St. Joseph's College for Women, Tiruppur.
Use the following college information to answer questions. If you don't know, say so clearly.

COLLEGE INFORMATION:
{COLLEGE_INFO}

User Question: {user_question}

Answer concisely and helpfully using only the information above:
"""
        
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": full_prompt}],
            model="llama-3.3-70b-versatile",  # Fast and capable
            temperature=0.3,
            max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Groq Error: {e}")
        return None

def query_gemini(user_question):
    """Query Gemini API for response"""
    if not gemini_available:
        return None
    
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        prompt = f"""You are a helpful assistant for St. Joseph's College for Women, Tiruppur.
Use this college information to answer questions:

{COLLEGE_INFO}

Question: {user_question}
Answer concisely using only the information above:"""
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Gemini Error: {e}")
        return None

def get_answer(user_question):
    """Try Groq first, then fallback to Gemini"""
    # Try Groq first (faster)
    answer = query_groq(user_question)
    if answer:
        return answer, "🚀 Groq API (Fast)"
    
    # Fallback to Gemini
    answer = query_gemini(user_question)
    if answer:
        return answer, "🧠 Google Gemini"
    
    return "I'm having trouble connecting. Please check your API keys.", "❌ No API"

# ============================================
# STREAMLIT WEB INTERFACE
# ============================================
def main():
    st.set_page_config(
        page_title="SJC Tiruppur - AI Chatbot",
        page_icon="🏛️",
        layout="wide"
    )
    
    # Custom CSS
    st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(135deg, #1a237e, #0d47a1);
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
    }
    .chat-message {
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .user-message {
        background: #e3f2fd;
    }
    .bot-message {
        background: #f5f5f5;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🏛️ St. Joseph's College for Women, Tiruppur</h1>
        <h3>AI Assistant powered by Groq & Gemini</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.image("https://stjosephcollegetup.edu.in/images/logo.png", width=200)
        st.markdown("### 🤖 About")
        st.write("Ask anything about St. Joseph's College for Women!")
        
        st.markdown("### 🚀 Quick Questions")
        sample_questions = [
            "What courses are offered?",
            "What is the NAAC grade?",
            "Tell me about placement cell",
            "How to apply for admission?",
            "What scholarships are available?",
            "Tell me about the library",
            "What is the NIRF ranking?",
            "List all departments"
        ]
        for q in sample_questions:
            if st.button(q, use_container_width=True):
                st.session_state["user_input"] = q
                st.rerun()
    
    # Main chat area
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "👋 Hello! I'm SJC AI Assistant. Ask me anything about St. Joseph's College for Women, Tiruppur!"}
        ]
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # User input
    user_query = st.chat_input("Type your question here...")
    
    # If user submitted a query
    if user_query:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.markdown(user_query)
        
        # Get response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                answer, model_used = get_answer(user_query)
                full_response = f"{answer}\n\n---\n*🤖 Powered by: {model_used}*"
                st.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
        
        st.rerun()

if __name__ == "__main__":
    main()
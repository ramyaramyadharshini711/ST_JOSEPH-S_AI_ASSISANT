import streamlit as st
import time
from rag_pipeline import get_pipeline

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="SJC Tiruppur AI Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# MODERN DARK THEME
# =====================================================

st.markdown("""
<style>

/* ---------------- MAIN ---------------- */

.stApp{
    background:#0D0D0D;
}

/* ---------------- SIDEBAR ---------------- */

section[data-testid="stSidebar"]{
    background:#0D0D0D;
    border-right:2px solid #D4AF37;
}

/* ---------------- HEADER ---------------- */

.header{

background:linear-gradient(135deg,#7C3AED,#A855F7);

padding:22px;

border-radius:16px;

text-align:center;

margin-bottom:20px;

box-shadow:0 8px 20px rgba(0,0,0,.25);

}

.header h1{

color:#FFFFFF;

margin:0;

font-size:34px;

font-weight:700;

}

.header p{

color:#F3F4F6;

margin-top:8px;

font-size:16px;

}

/* ---------------- BUTTONS ---------------- */

.stButton>button{

width:100%;

height:42px;

border-radius:12px;

background:#FFFFFF;

color:white;

font-weight:bold;

border:2px solid #D4AF37;

transition:0.3s;

}

.stButton>button:hover{

background:#9333EA;

transform:translateY(-2px);

}

/* ---------------- CHAT ---------------- */

.stChatMessage{

border-radius:16px;

padding:10px;

margin-bottom:12px;

color:#FFFFFF !important;

}

/* ---------------- CHAT INPUT ---------------- */

[data-testid="stChatInput"]{

background:white;

border-radius:14px;

border:2px solid #1F5E3B;

}




/* ---------- SUCCESS / INFO / WARNING ---------- */

.stSuccess,

.stInfo,

.stWarning,

.stError{
    
    color:#FFFFFF !important;
}

/* ---------------- HIDE STREAMLIT ---------------- */

footer{

visibility:hidden;

}

#MainMenu{

visibility:hidden;

}

header{

visibility:hidden;

}

</style>
""",unsafe_allow_html=True)

# =====================================================
# SESSION STATE
# =====================================================

if "messages" not in st.session_state:
    st.session_state.messages=[]

if "pipeline" not in st.session_state:
    st.session_state.pipeline=get_pipeline()

pipeline=st.session_state.pipeline

status=pipeline.get_status()

# =====================================================
# HEADER
# =====================================================

st.markdown("""
<div class="header">

<h1>🎓 SJC Tiruppur AI Assistant</h1>

<p>
St. Joseph's College for Women, Tiruppur
</p>

</div>
""", unsafe_allow_html=True)

# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    # ---------------------------
    # Logo
    # ---------------------------

    try:
        st.image("assets/logo.png", width=170)
    except:
        st.markdown("# 🎓")

    st.title("SJC AI")

    st.caption("College Information Assistant")

    st.markdown("---")

    # ---------------------------
    # AI STATUS
    # ---------------------------

    st.subheader("🟢 System Status")

    if status["vectorstore_loaded"]:
        st.success("📚 Knowledge Base Ready")
    else:
        st.error("📚 Knowledge Base Missing")

    if status["groq_available"]:
        st.success("⚡ Groq Connected")
    else:
        st.warning("⚡ Groq Offline")

    if status["gemini_available"]:
        st.success("✨ Gemini Connected")
    else:
        st.warning("✨ Gemini Offline")

    st.markdown("---")

    # ---------------------------
    # QUICK QUESTIONS
    # ---------------------------

    st.subheader("⚡ Quick Questions")

    quick_questions = {

        "📚 Courses":
        "What courses are offered?",

        "🎓 Admission":
        "How can I apply for admission?",

        "💰 Fees":
        "Tell me about the fee structure.",

        "🏆 Placement":
        "Tell me about placements.",

        "📖 Library":
        "Tell me about the library.",

        "🏠 Hostel":
        "Do you have hostel facilities?",

        "🏛 History":
        "Tell me about the college history.",

        "⭐ NAAC":
        "What is the NAAC grade?"

    }

    for title, question in quick_questions.items():

        if st.button(title, use_container_width=True):

            st.session_state.quick_question = question

    st.markdown("---")

    # ---------------------------
    # CHAT OPTIONS
    # ---------------------------

    st.subheader("⚙️ Chat")

    if st.button(
        "🗑 Clear Chat",
        use_container_width=True
    ):

        st.session_state.messages = []

        st.rerun()

    st.markdown("---")

   

    st.markdown("---")

    st.info("""
💡 **Try asking:**

• Courses Offered

• Admission Process

• Fee Structure

• Placement Details

• Hostel Facilities

• Scholarships

• Library

• NAAC Grade

• NIRF Ranking
""")


# =====================================================
# CHAT AREA
# =====================================================

# Welcome Message

if len(st.session_state.messages) == 0:

    with st.chat_message(
        "assistant",
        avatar="🎓"
    ):

        st.markdown("""
# 👋 Welcome to SJC Tiruppur AI Assistant

I'm your AI-powered college assistant.

I can answer questions about:

- 📚 Courses Offered
- 🎓 Admissions
- 💰 Fee Structure
- 🏆 Placements
- 📖 Library
- 🏠 Hostel
- 📄 Scholarships
- 👩‍🏫 Departments
- 🏛 College History
- ⭐ NAAC Accreditation
- 📊 Rankings

---

### 💡 Example Questions

- What courses are offered?

- Tell me about admission.

- What scholarships are available?

- Does the college have hostel facilities?

- Tell me about placements.

---

Type your question below 👇
""")

# =====================================================
# DISPLAY CHAT HISTORY
# =====================================================

for message in st.session_state.messages:

    if message["role"] == "user":

        with st.chat_message(
            "user",
            avatar="👤"
        ):

            st.markdown(message["content"])

    else:

        with st.chat_message(
            "assistant",
            avatar="🎓"
        ):

            st.markdown(message["content"])

# =====================================================
# CHAT INPUT
# =====================================================

user_input = st.chat_input(
    "💬 Ask me anything about SJC Tiruppur..."
)

# =====================================================
# PROCESS USER QUERY
# =====================================================

def process_query(question):

    # -----------------------------
    # Store User Message
    # -----------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    # -----------------------------
    # Show User Message Immediately
    # -----------------------------


    # -----------------------------
    # Assistant Response
    # -----------------------------

    with st.chat_message("assistant", avatar="🎓"):

        response_placeholder = st.empty()

        with st.spinner("🔍 Searching Knowledge Base..."):

            try:

                answer, model_used, sources = pipeline.query(question)

            except Exception as e:

                answer = f"❌ Error:\n\n{e}"

                model_used = "Unknown"

                sources = []

        # -----------------------------
        # Typing Animation
        # -----------------------------

        full_response = ""

        for word in answer.split():

            full_response += word + " "

            response_placeholder.markdown(full_response + "▌")

            time.sleep(0.02)

        

        response_placeholder.markdown(full_response)

    # -----------------------------
    # Save Assistant Response
    # -----------------------------

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": full_response
        }
    )
# =====================================================
# HANDLE USER INPUT
# =====================================================

if user_input:
    process_query(user_input)
    st.rerun()

# =====================================================
# HANDLE QUICK QUESTIONS
# =====================================================

if "quick_question" in st.session_state:

    process_query(st.session_state.quick_question)

    del st.session_state.quick_question

    st.rerun()
# =====================================================
# FOOTER
# =====================================================



st.markdown(
"""
<div style="text-align:center;padding:20px;color:#FFFFFF;">

<hr style="border:1px solid #FFFFFF;">

<h3 style="color:#FFFFFF;">
🏛 St. Joseph's College for Women
</h3>

<p>
AI Powered College Information Assistant
</p>

<p>
Powered by
<b>LangChain</b> •
<b>ChromaDB</b> •
<b>Groq</b> •
<b>Google Gemini</b>
</p>

<p style="font-size:13px;color:#94A3B8;">
Made with ❤️ using Streamlit
</p>

</div>
""",
unsafe_allow_html=True
)


# =====================================================
# ERROR CHECKS
# =====================================================

if not status["vectorstore_loaded"]:

    st.warning(
"""
⚠️ Knowledge Base is not loaded.

Run:

```bash
python build_kb.py 
""")

if not status["vectorstore_loaded"]:

    st.warning(
"""
⚠️ Knowledge Base is not loaded.

Run:

```bash
python build_kb.py """)
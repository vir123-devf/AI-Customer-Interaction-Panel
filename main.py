# Importing all packages
import streamlit as st
import os
import io
import base64
from dotenv import load_dotenv

# LangChain + FAISS
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.chat_models import ChatCohere

# Whisper STT
from transformers import pipeline

# gTTS (TTS)
from gtts import gTTS

# PDF export
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit
import re

# Supabase - for interaction postgre db

from supabase import create_client, Client
import datetime

# Load env
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def store_interaction(user_msg, bot_msg):
    try:
        data = {
            "user_message": user_msg,
            "bot_message": bot_msg,
            "created_at": datetime.datetime.utcnow().isoformat()
        }
        supabase.table("interactions").insert(data).execute()
    except Exception as e:
        st.error(f"Failed to store in Supabase: {e}")





def clean_markdown(text):
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)      # **bold**
    text = re.sub(r"\*(.*?)\*", r"\1", text)          # *italic*
    text = re.sub(r"`(.*?)`", r"\1", text)            # inline code
    text = re.sub(r"#+ ", "", text)                   # headings ####
    text = re.sub(r"- ", "", text)                    # bullet points
    text = re.sub(r"\n+", ". ", text)                 # newlines → pause
    text = text.replace("_", "")                      # remove underscores
    return text.strip()


# ---------------------------------------------------
# BACKGROUND
# ---------------------------------------------------
def add_bg_from_local(image_file):
    if os.path.exists(image_file):
        with open(image_file, "rb") as f:
            encoded = base64.b64encode(f.read()).decode()
        st.markdown(f"""
            <style>
            .stApp {{
                background-image: url("data:image/png;base64,{encoded}");
                background-size: cover;
                background-repeat: no-repeat;
            }}
            </style>
        """, unsafe_allow_html=True)


# ---------------------------------------------------
# PDF Writer
# ---------------------------------------------------
def generate_pdf(chat_history):
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)

    width, height = letter
    pdf.setFont("Times-Roman", 12)
    x, y = 40, 750

    pdf.setFont("Times-Bold", 16)
    pdf.drawString(x, y, "Chat History")
    y -= 40

    for sender, msg in chat_history:
        header = f"{sender.upper()}:"
        wrapped = simpleSplit(msg, "Times-Roman", 12, 520)

        pdf.setFont("Times-Bold", 12)
        pdf.drawString(x, y, header)
        y -= 20

        pdf.setFont("Times-Roman", 12)
        for line in wrapped:
            if y < 60:
                pdf.showPage()
                y = 750
            pdf.drawString(x + 20, y, line)
            y -= 16
        y -= 10

    pdf.save()
    buffer.seek(0)
    return buffer



# ---------------------------------------------------
# STREAMLIT UI
# ---------------------------------------------------
st.set_page_config(page_title="AI Customer Interaction Panel", layout="centered")
add_bg_from_local("Background.png")

st.title("🎤 AI Customer Interaction Panel")
st.write("Speak → Bot transcribes → RAG answers → Bot speaks → Next question…")



# ---------------------------------------------------
# ENV + LOAD MODELS
# ---------------------------------------------------
load_dotenv()
cohere_api_key = os.getenv("COHERE_API_KEY")


@st.cache_resource
def load_db():
    emb = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
    return FAISS.load_local("index", emb, allow_dangerous_deserialization=True)


@st.cache_resource
def load_llm():
    return ChatCohere(
        model="command-r-plus",
        temperature=0,
        cohere_api_key=cohere_api_key
    )


@st.cache_resource
def load_asr():
    return pipeline(
        "automatic-speech-recognition",
        model="openai/whisper-small",
        device="cpu"
    )


db = load_db()
llm = load_llm()
asr = load_asr()



# ---------------------------------------------------
# RAG Answer
# ---------------------------------------------------
def get_intervention(query):
    docs = db.similarity_search(query, k=3)
    context = "\n".join([d.page_content for d in docs])[:2000]

    prompt = f"""
    You are an AI customer support assistant for an e-commerce platform.

    Use only the information provided in the following knowledge base content:

    {context}

    User Query:
    {query}

    Your Task:
    - Understand what the customer is asking.
    - Provide a clear and helpful answer based ONLY on the provided e-commerce content.
    - Do NOT guess or create information that is not in the content.
    - If the answer is not present in the provided content, reply strictly with: "I don't know".

    Now provide the most accurate response:
    """

    return llm.invoke(prompt).content



# ---------------------------------------------------
# SESSION STATE
# ---------------------------------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "awaiting_next" not in st.session_state:
    st.session_state.awaiting_next = True  # show mic at start



# ---------------------------------------------------
# MAIN CHAT LOGIC
# ---------------------------------------------------
st.header("🎙️ Ask Your Question")



if "mic_key" not in st.session_state:
    st.session_state.mic_key = 0
# Show Mic ONLY when awaiting_next is True
if st.session_state.awaiting_next:
    audio_data = st.audio_input(
        "Click to record your question",
        key=f"mic_{st.session_state.mic_key}"   # 🔥 forces mic refresh
    )
else:
    audio_data = None


# ----------- If user recorded a message ---------------
if audio_data:
    st.session_state.awaiting_next = False  # hide mic until bot finishes

    st.success("🎤 Voice received, processing...")

    # Save audio
    with open("user.wav", "wb") as f:
        f.write(audio_data.getvalue())

    # Speech → Text
    text = asr("user.wav")["text"]
    st.markdown(f"### 🧑 You said:\n{text}")

    # RAG
    with st.spinner("🤖 Thinking..."):
        bot_reply = get_intervention(text)

    # Save chat
    # st.session_state.chat_history.append(("user", text))
    # st.session_state.chat_history.append(("bot", bot_reply))
    st.session_state.chat_history.append(("user", text))
    st.session_state.chat_history.append(("bot", bot_reply))

    # Store in Supabase
    store_interaction(text, bot_reply)

    # Bot response
    st.markdown("### 🤖 Bot:")
    st.write(bot_reply)

    # TTS
    tts = gTTS(bot_reply)
    tts.save("bot_voice.mp3")

    # Autoplay
    with open("bot_voice.mp3", "rb") as audio_file:
        audio_b64 = base64.b64encode(audio_file.read()).decode()

    audio_html = f"""
        <audio autoplay>
            <source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3">
        </audio>
    """
    st.markdown(audio_html, unsafe_allow_html=True)

    # ❌ DON'T reset awaiting_next here
    # It is already False
# ---------------------------------------------------
# SHOW NEXT QUESTION BUTTON (CONTINUOUS CHAT)
# ---------------------------------------------------
if not st.session_state.awaiting_next:
    if st.button("🎤 Ask Next Question"):
        st.session_state.awaiting_next = True

        # 🔥 Increment mic_key so mic resets
        st.session_state.mic_key += 1

        st.rerun()



# ---------------------------------------------------
# CHAT HISTORY
# ---------------------------------------------------
st.header("💬 Conversation History")
for sender, msg in st.session_state.chat_history:
    if sender == "user":
        st.markdown(f"🧑 **You:** {msg}")
    else:
        st.markdown(f"🤖 **Bot:** {msg}")



# ---------------------------------------------------
# PDF DOWNLOAD
# ---------------------------------------------------
if st.session_state.chat_history:
    pdf = generate_pdf(st.session_state.chat_history)
    st.download_button(
        "📄 Download Chat as PDF",
        data=pdf,
        file_name="Customer_Interaction_history.pdf",
        mime="application/pdf"
    )





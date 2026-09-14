import streamlit as st
from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

load_dotenv()

st.set_page_config(
    page_title="Mood AI",
    page_icon="🤖",
    layout="centered"
)

st.markdown("""
<style>
    .main {
        background-color: #0e1117;
    }

    .title {
        text-align: center;
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        color: #9ca3af;
        margin-bottom: 30px;
    }

    .stChatMessage {
        border-radius: 15px;
    }

    .mode-box {
        padding: 15px;
        border-radius: 12px;
        background: #161b22;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="title">🤖 Mood AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Choose a personality and talk to your AI agent</div>',
    unsafe_allow_html=True
)

# ---------------- MODEL ----------------

model = ChatMistralAI(
    model="mistral-tiny",
    temperature=0.9
)

# ---------------- SIDEBAR ----------------

with st.sidebar:
    st.header("🎭 AI Personality")

    choice = st.radio(
        "Choose a mode:",
        ["😡 Angry", "😂 Funny", "😢 Sad"]
    )

    if choice == "😡 Angry":
        mode = "You are an angry agent. Respond in an irritated, aggressive and funny way, but do not use hateful or harmful content."
    elif choice == "😂 Funny":
        mode = "You are a very funny agent. Respond with humor, sarcasm and playful jokes."
    else:
        mode = "You are a sad agent. Respond in a melancholic, emotional and slightly dramatic way."

    st.divider()

    if st.button("🗑️ New Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.divider()

    st.caption("Powered by LangChain + Mistral AI")

# ---------------- CHAT MEMORY ----------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- DISPLAY CHAT ----------------

for message in st.session_state.messages:

    if message["role"] == "user":
        with st.chat_message("user"):
            st.write(message["content"])

    else:
        with st.chat_message("assistant"):
            st.write(message["content"])

# ---------------- USER INPUT ----------------

prompt = st.chat_input("Talk to your AI...")

if prompt:

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.write(prompt)

    messages = [
        SystemMessage(content=mode)
    ]

    for message in st.session_state.messages:

        if message["role"] == "user":
            messages.append(
                HumanMessage(content=message["content"])
            )

        else:
            messages.append(
                AIMessage(content=message["content"])
            )

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            response = model.invoke(messages)

        st.write(response.content)

    st.session_state.messages.append({
        "role": "assistant",
        "content": response.content
    })
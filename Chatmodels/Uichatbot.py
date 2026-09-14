import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from langchain_mistralai import ChatMistralAI
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage

st.title(" welcome to my chatbot😎")

model = ChatMistralAI(model="mistral-tiny", temperature=0.9)




if "messages" not in st.session_state:
    st.session_state.messages = [
        SystemMessage("")
    ]

# display existing chat history (skip the system message)
for msg in st.session_state.messages:
    if isinstance(msg, HumanMessage):
        with st.chat_message("user"):
            st.write(msg.content)
    elif isinstance(msg, AIMessage):
        with st.chat_message("assistant"):
            st.write(msg.content)

prompt = st.chat_input("you : ")

if prompt:
    st.session_state.messages.append(HumanMessage(content=prompt))
    with st.chat_message("user"):
        st.write(prompt)

    response = model.invoke(st.session_state.messages)

    st.session_state.messages.append(AIMessage(content=response.content))
    with st.chat_message("assistant"):
        st.write(response.content)
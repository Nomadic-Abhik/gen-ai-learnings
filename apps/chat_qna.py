from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import streamlit as st
load_dotenv()
llm = ChatOpenAI(model = "gpt-4o-mini")

st.title(" 🥂Gulu - Your QnA Companion")
st.markdown("powered by Google Gemini and Langchain")

if "message" not in st.session_state:
    st.session_state.message = []
if "history" not in st.session_state:
    st.session_state.history =  []

for message in st.session_state.message:
    role = message["role"]
    content = message["content"]
    st.chat_message(role).markdown(content)

query = st.chat_input() 

if query:
    st.chat_message("user").markdown(query)
    st.session_state.message.append({"role": "user", "content" : query})
    st.session_state.history.append({"role": "user", "content" : query})
    response = llm.invoke(st.session_state.history)
    st.chat_message("ai").markdown(response.content)
    st.session_state.message.append({"role": "ai", "content" :response.content})
    st.session_state.history.append({"role": "ai", "content" : response.content})






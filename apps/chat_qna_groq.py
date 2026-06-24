from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.agents import create_agent
from langchain_community.utilities import GoogleSerperAPIWrapper
import streamlit as st
from langgraph.checkpoint.memory import InMemorySaver


load_dotenv()
groq_llm  = ChatGroq(model = "openai/gpt-oss-20b", streaming= True)
search = GoogleSerperAPIWrapper()
tools = [search.run]


st.subheader("Gulu - Your One Stop Travel Companion")

if "history" not in st.session_state:
    st.session_state.history = []
    st.session_state.memory = InMemorySaver()

for item in st.session_state.history:
    role = item["role"]
    message = item ["content"]
    st.chat_message(role).markdown(message)

query = st.chat_input("Ask Me Any Question")

agent = create_agent(
    model = groq_llm,
    tools = tools,
    system_prompt= "You are an Search Engine and Always Use Google to search and provide result",
    checkpointer= st.session_state.memory
)

if query:
    st.chat_message("user").markdown(query)
    st.session_state.history.append({"role": "user", "content": query})
    response = agent.stream(
        {"messages":[{"role":"user", "content" : query}]},
        { "configurable" : {"thread_id" : "1"}},
        stream_mode= "messages"
    )
    ai_container = st.chat_message("ai")
    with ai_container:
        space = st.empty()
        message = " "
        
        for chunk in response:
            message = message + chunk[0].content
            space.write(message)
    st.session_state.history.append({"role": "ai", "content": message})

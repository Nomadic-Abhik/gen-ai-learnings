import sys
from pathlib import Path

# Add the workspace root to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.utilities import SQLDatabase
from sqlalchemy import create_engine
from langgraph.checkpoint.memory import InMemorySaver
import streamlit as st
from prompts.sql_agent_prompt import system_prompt

load_dotenv()  # Load environment variables from .env file


connection_string = (
    "mssql+pyodbc://@(localdb)\MSSQLlocaldb/"  
    "CommandDb?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
)

engine = create_engine(connection_string)
db = SQLDatabase(engine)
groq_llm  = ChatGroq(model = "openai/gpt-oss-20b")
openai_llm = ChatOpenAI(model_name = "gpt-4o")
toolkit = SQLDatabaseToolkit(db = db, llm = groq_llm) 
tools = toolkit.get_tools()

st.subheader("SQL AI Agent")
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []

for message in st.session_state.conversation_history:
    role = message["role"]
    content = message["content"]
    st.chat_message(role).markdown(content)

@st.cache_resource
def get_agent():
    return create_agent(
        model = openai_llm,
        tools = tools,
        checkpointer = InMemorySaver(),
        system_prompt = system_prompt
    )

query = st.chat_input("Ask Me Anything About Your Tasks")
if query:
    st.chat_message("user").markdown(query)
    st.session_state.conversation_history.append({"role": "user", "content": query})

    result= get_agent().invoke(
        {"messages": [{"role": "user", "content": query}]},
         {"configurable":{"thread_id":"1"}}
    )
    st.chat_message("assistant").markdown(result["messages"][-1].content)
    st.session_state.conversation_history.append({"role": "assistant", "content": result["messages"][-1].content})



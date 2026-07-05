import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from prompts.pdf_reader_prompt import system_prompt
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from dotenv import load_dotenv
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from langchain.tools import tool
import streamlit as st
import os

load_dotenv()
st.subheader("My First Agentic RAG System")
BASE_DIR = Path(__file__).resolve().parent.parent
path = BASE_DIR / "files" / "pdf"
path.mkdir(parents=True, exist_ok=True)


### Section Upload Section

def Upload_pdf(path):
    try:
        if "vector_store" not in st.session_state:
            st.session_state.vector_store = None
        process_pdf(path)
        uploaded = st.session_state.get("vector_store")
        print(f"Vector store after processing: {uploaded}")
        if uploaded is not None:
            return "Documents Uploaded"
        else:
            return "Documents Upload failed"
    except:
        raise ValueError("Documents Upload failed")
  
def process_pdf(path):
    loader = PyPDFDirectoryLoader(path)
    documents = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    split_docs = splitter.split_documents(documents)
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    vector_store = st.session_state.get("vector_store")
    print(f"Vector store before processing: {vector_store}")
    if vector_store is None:
        vector_store = InMemoryVectorStore.from_documents(
            documents=split_docs,
            embedding=embeddings
        )
        print(f"Vector store created: {vector_store}")
        st.session_state.vector_store = vector_store
    else:
        vector_store.add_documents(split_docs)
        print(f"Vector store updated: {vector_store}")
    return vector_store

if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []
if "upload_file" not in st.session_state:
    st.session_state.upload_file = False

for msg in st.session_state.conversation_history:
    role = msg["role"]
    content = msg ["content"]
    st.chat_message(role).markdown(content)

if not st.session_state.upload_file:
    st.chat_message("ai").markdown("Please Upload your files")
    uploaded_files = st.file_uploader(label = "Select pdf files", type =["pdf"],accept_multiple_files= True)
    if uploaded_files:
        with st.spinner("Processing files......"):
            for file in uploaded_files:
                save_path = path / file.name
                with open(save_path, "wb") as f:
                    f.write(file.getvalue())
            upload_status = Upload_pdf(path)
            if upload_status == "Documents Uploaded":
                st.session_state.upload_file = True
                st.chat_message("ai").markdown("Documents Uploaded")
                print(f"Vector store after upload: {st.session_state.get("vector_store")}") 
                st.rerun()

### Section Response
llm = ChatGroq(model = "openai/gpt-oss-20b")
@tool
def create_Retriever(query: str):
    """Retrieve documents relevant to a query from the knowledge base."""
    vector_store = st.session_state.get("vector_store")
    print(f"Vector store in create_Retriever: {vector_store}")
    if vector_store is None:
        vector_store = process_pdf(path)
        print(f"Vector store created in create_Retriever: {vector_store}")
    print(f"Vector store already exists in create_Retriever: {vector_store}")
    docs = vector_store.similarity_search(query)
    context = ""
    for doc in docs:
        context +=  doc.page_content + "/n"
    return context

@st.cache_resource
def get_agent():
    agent = create_agent(
        model=llm,
        system_prompt=system_prompt,
        checkpointer=InMemorySaver(),
        tools=[create_Retriever],
    )
    return agent

if st.session_state.upload_file:
    query = st.chat_input("Ask Me Anything About the Documents ?")
    if query:
        st.chat_message("user").markdown(query)
        if query.lower() == "clear":
            st.session_state.conversation_history = []
            st.session_state.upload_file = False
            st.rerun()
        st.session_state.conversation_history.append({"role":"user","content": query})
        response = get_agent().invoke(
            {"messages": [{"role": "user", "content": query}]},
            {"configurable": {"thread_id": 1}}
        )
        answer = response["messages"][-1].content
        st.chat_message("ai").markdown(answer)
        st.session_state.conversation_history.append({"role":"ai","content": answer})
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_docling import DoclingLoader
import streamlit as st
import os
load_dotenv()

### Documents Loading
document_path = '../files/pdf/Resume.pdf'
loader = PyPDFLoader(document_path)
docs = loader.load()



### Document Spliting
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
splitted_docs = splitter.split_documents(docs)


### Creating Embeding Models
embeddings = OpenAIEmbeddings( model= "text-embedding-3-large")

### Creating Vector Space and Vector Stores
persistent_directory = "../chroma_doc_db"
if os.path.exists(persistent_directory) :
    print ('Vector Store Exists.Loading Vector from Stores')
    vector = Chroma(
        persist_directory=persistent_directory,
        embedding_function = embeddings
    )
else:
    print ('vector stores need to be created and going for Vector store creation')
    vector = Chroma.from_documents(
        documents = splitted_docs,
        embedding = embeddings,
        persist_directory = persistent_directory
    )

def Create_Context( query:str):
   search = vector.similarity_search(query, k = 3)
   context = ""
   for item in search:
       context += context + item.page_content + "\n"
   return {
        "context": context,
        "question": query
    }

llm = ChatGroq(model="openai/gpt-oss-20b")
system_prompt = """
    you are an smart chat assistant and answer user query
    based on context. Consider the synonym of words and smart search the document.
    please say "I am not able to Answer with current context"
    if you unable to find the answer 
"""
prompt = ChatPromptTemplate.from_messages([
    {"role": "ai", "content" : system_prompt},
    {"role": "user", "content" : "Context: {context}Question: {question}"}
])
st.subheader("My First RAG Application")

if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []

for conversation in st.session_state.conversation_history:
    role = conversation["role"]
    content = conversation["content"]
    st.chat_message(role).markdown(content)


query = st.chat_input("Please Ask Me Anything ?")
if query:
    st.chat_message("user").markdown(query)
    st.session_state.conversation_history.append({"role":"user", "content": query})
    chain = Create_Context | prompt | llm
    response = chain.invoke(query)

    ai_container = st.chat_message("ai")
    with ai_container:
        with st.spinner("Generating Response..."):
            space = st.empty()
            space.write(response.content)
    st.session_state.conversation_history.append({"role":"ai", "content": response.content})




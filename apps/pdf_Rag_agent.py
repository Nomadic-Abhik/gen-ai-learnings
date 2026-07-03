from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

# Documents Loading
document_path = '../files/Resume.pdf'
loader = PyPDFLoader(document_path)
docs = loader.load()

# Documents Splitting
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
splitted_docs = splitter.split_documents(docs)

# Embeddings
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

# Vector Store Chroma call Embeddings.embed_documents internally
#  and Persisting the data in Chroma DB
vectorstore = Chroma.from_documents(
    documents=splitted_docs,
    embedding=embeddings,
    persist_directory="../chroma_db"
)

# Crating a function to get context from vectorstore based on user query

def get_context_from_vectorstore(query):
    vector = vectorstore.similarity_search(query = query)
    context = ""
    for doc in vector:
        context += doc.page_content + "\n"

    return {
        "context":context,
        "question":query
    }

#LLM and Prompt Template
llm = ChatOpenAI(model="gpt-5")
system_prompt = ("""
        You are a helpful assistant. 
        Provide answers based only on the context provided for the user question. 
        If you don't know the answer, just say 'I dont know.'
    """
)

prompt = ChatPromptTemplate.from_messages([
    {"role":"system", "content": system_prompt},
    {"role":"human", "content": "Context: {context}Question: {question}"}
])

#Chain Creation
rag_chain = get_context_from_vectorstore | prompt | llm

#Invoking the chain with a user query
res = rag_chain.invoke('What is the Designation of the Person in Optum?')
res.content
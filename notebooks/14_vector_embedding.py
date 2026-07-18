from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter 
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv
load_dotenv()

# Documents Loading
document_path = '../files/Resume.pdf'
loader = PyPDFLoader(document_path)
docs = loader.load()

# Documents Splitting
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
splitted_docs = splitter.split_documents(docs)
len(splitted_docs)
for chunk in splitted_docs:
    print(len(chunk.page_content))

# Embeddings Generation
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
embedded_docs = embeddings.embed_documents([splitted_doc.page_content for splitted_doc in splitted_docs])
len(embedded_docs)

# Vector Store Creation (No need to explicitly call embed_documents() 
# as it is called internally by Chroma.from_documents())
vector_store = Chroma.from_documents(
    documents=splitted_docs, 
    embedding=embeddings,
    persist_directory="../db/chroma_db")

user_query = "Who is Prime Minister of India?"
# K is optional and it provides the number of similar documents to return. Default is 4.
vector = vector_store.similarity_search(user_query, k=2)
print(len(vector))
print(vector[0].page_content)
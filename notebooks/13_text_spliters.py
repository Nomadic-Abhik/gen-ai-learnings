from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Implenet direct Text Splitter

Text = """
Text is naturally organized into hierarchical units such as paragraphs, sentences, and words. We can leverage this inherent structure to inform our splitting strategy, creating split that maintain natural language flow, maintain semantic coherence within split, and adapts to varying levels of text granularity. LangChain’s RecursiveCharacterTextSplitter implements this concept:
The RecursiveCharacterTextSplitter attempts to keep larger units (e.g., paragraphs) intact.
If a unit exceeds the chunk size, it moves to the next level (e.g., sentences).
This process continues down to the word level if necessary."""

splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,
    chunk_overlap=20
)
chunks = splitter.split_text(Text)
len(chunks)
for chunk in chunks:
    print(chunk)
    print("\n")

## Implement Text Loader and then split the text into chunks
text_loader = TextLoader("../files/Code.txt")
text = text_loader.load()
text_chunks = splitter.split_documents(text)
len(text_chunks)
for chunk in text_chunks:
    print(chunk.page_content)
    print("\n")

pdf_loader = PyPDFLoader("../files/Resume.pdf")
pdf_text = pdf_loader.load()
pdf_chunks = splitter.split_documents(pdf_text)
len(pdf_chunks)
for chunk in pdf_chunks:
    print(chunk.page_content)
    print("\n")
    break
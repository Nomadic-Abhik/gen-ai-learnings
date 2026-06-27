from langchain_community.document_loaders import  TextLoader, PyPDFLoader, WebBaseLoader, WikipediaLoader, CSVLoader
text_loader = TextLoader("../files/Code.txt")
text = text_loader.load()
text[0].page_content
print(text[0].page_content)
len(text)

pdf_loader = PyPDFLoader("../files/Resume.pdf")
pdf = pdf_loader.load()
pdf[1].page_content
print(pdf[1].page_content)
len(pdf)


web_loader = WebBaseLoader("https://github.com/Nomadic-Abhik/gen-ai-learnings/tree/main/notebooks")
web = web_loader.load()
web[0].page_content
web[0].metadata
print(web[0].page_content)
len(web)

wikipedia_loader = WikipediaLoader(query = "Sachin Tendulkar", load_max_docs=3)
wikipedia = wikipedia_loader.load()
wikipedia[0].page_content
print(wikipedia[0].page_content)
len(wikipedia)

csv_loader = CSVLoader("../files/myData.csv", encoding="utf-8",
                        csv_args={"delimiter": "", "quotechar": '"'})
csv = csv_loader.load()
csv[1].page_content
print(csv[1].page_content)
len(csv)

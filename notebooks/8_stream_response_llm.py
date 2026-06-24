from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()


groq_ai_llm = ChatGroq(model = "openai/gpt-oss-20b", streaming= True)
groq_ai_response = groq_ai_llm.stream("Tell Us something on Kolkata")
for chunk in groq_ai_response:
    print(chunk.content, end = "")


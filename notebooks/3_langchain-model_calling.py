from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_anthropic import ChatAnthropic
from langchain_ollama import ChatOllama
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

### Define Prompts

prompts = [
    ('system', 'you are a c# Developer'),
    ('user', 'explain me the concept of Pointer')
]

### Using OpenAI

open_ai_llm = ChatOpenAI()

opeai_response = open_ai_llm.invoke("Explain Generative AI")
print(opeai_response.content)

### Using Google Gemini

gemini_llm = ChatGoogleGenerativeAI(model = "gemini-2.5-flash-lite")
gemini_response = gemini_llm.invoke("Create a 3 days itinerary of East Sikim")
print(gemini_response.content)

### Using Anthropic 
claude_llm = ChatAnthropic(model = "Claude Opus 4.5")
claude_response = claude_llm.invoke("Create 3 days itinerary in Kolkata")
print(claude_response.content)

### Using Local Gemma Model ( Can be used locally without Internet)

ollama_llm = ChatOllama(model = "gemma3:4b")
ollama_response = ollama_llm.invoke("Who is the Prime Minister Of India")
print(ollama_response.content)

### Using ChatGroq

groq_llm = ChatGroq(model = "openai/gpt-oss-20b")
groq_response = groq_llm.invoke("what is RAG ?")
print(groq_response.content)



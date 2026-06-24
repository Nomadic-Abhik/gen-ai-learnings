from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

## Static Prompt using Tuple
open_ai_llm = ChatOpenAI(model = "gpt-4.1-2025-04-14")

static_prompts = [
    ('system', 'you are a c# Developer'),
    ('user', 'explain me the concept of Pointer')
]
openai_response = open_ai_llm.invoke(static_prompts)
print(openai_response.content)

## static Prompt using dictionary
open_ai_llm = ChatOpenAI(model = "gpt-4.1-2025-04-14")
dynamic_prompt = [
    {"role":"system", "content" : "you are a Translater and Translate input in Bengali"},
    {"role":"user", "content" : "I love to play cricket"},
]

opeai_response = open_ai_llm.invoke(dynamic_prompt)
print(opeai_response.content)

## Dynamic Prompt Using ChatPrompt Template

open_ai_llm = ChatOpenAI(model = "gpt-4.1-2025-04-14")
template_prompt = [
   {"role":"system", "content" : "you are a Translater and Translate input in {langugae}"},
    {"role":"user", "content" : "{query}"},
 ]
llm_prompt = ChatPromptTemplate.from_messages(template_prompt)
llm_prompt = llm_prompt.format_messages(langugae = "Telegu", query = "I love Kolkata")
response = open_ai_llm.invoke(llm_prompt)
print( response.content)

## Dynamic Prompt Using Groq & ChatPrompt Template
groq_llm = ChatGroq(model = "openai/gpt-oss-20b")
template_prompt = [
   {"role":"system", "content" : "you are a Translater and Translate input in {langugae}"},
    {"role":"user", "content" : "{query}"},
 ]
llm_prompt = ChatPromptTemplate.from_messages(template_prompt)
llm_prompt = llm_prompt.format_messages(langugae = "Bengali", query = "Who won IPL 2026?")
response = groq_llm.invoke(llm_prompt)
print( response.content)

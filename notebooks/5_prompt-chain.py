from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


open_ai_llm = ChatOpenAI(model = "gpt-4.1-2025-04-14")
parser = StrOutputParser()

## Dynamic Prompts Invoking using Dictionary
template_prompt = [
   {"role":"system", "content" : "you are a Translater and Translate input in {langugae}"},
    {"role":"user", "content" : "{query}"},
 ]
llm_prompt = ChatPromptTemplate.from_messages(template_prompt)
result = open_ai_llm.invoke(llm_prompt.invoke({"langugae" : "English", "query" : "I love Kolkata"}))
print(result.content)

### Using Output Parser
parsed_result = parser.invoke(result)
print(parsed_result)

### using Custom Logic

def ConvertToUpperCase(result : str) -> str:
    return result.upper()

formated_result = ConvertToUpperCase(parsed_result)
print(formated_result)

### using complex invoke of above runnable

result = ConvertToUpperCase(parser.invoke(open_ai_llm.invoke(llm_prompt.invoke({"langugae" : "English", "query" : "I love Kolkata"})))) 
print(result)

## Simplyfies above with Chains

chains = llm_prompt | open_ai_llm | parser | ConvertToUpperCase
print (chains.invoke({"langugae" : "Telegu", "query" : "I love Kolkata"}))
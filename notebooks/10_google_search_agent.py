from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import create_agent
from langchain_community.utilities import GoogleSerperAPIWrapper
from pydantic import BaseModel

from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()
parser = StrOutputParser()
dynamic_prompt = [
    {"role":"user", "content" : "Who Won IPL {inputyear}"}
]
def ConvertToUpperCase(result : str) -> str:
    return result.upper()

llm_model = ChatOpenAI(model = "gpt-4.1-2025-04-14")
llm_query =  ChatPromptTemplate.from_messages(dynamic_prompt)
llm_query = llm_query.format_messages(inputyear = "2014")

 ### chain Response
llm_response =parser.invoke(llm_model.invoke(llm_query))
print(llm_response)

### Structure Output
class ResponseStructure(BaseModel):
    winner: str

llm_model =  llm_model.with_structured_output(ResponseStructure)
chains = llm_query | llm_model 

latest_result = chains.invoke({"inputyear" : "2025"})

print(latest_result) 
## since the model was trained with the data updated on 14th April 2025, the response will not be accurate,
## so we will create a google search agent which will give us latest data as google is always up to date

search = GoogleSerperAPIWrapper()
agent = create_agent(
    model = llm_model, 
    tools= [search.run],
    system_prompt= " you are a search engine and you only provide one liner relevant answer to the query")

response = agent.invoke({"messages":[{"role": "user","content":"Who Won IPL 2026"}]})
len(response)

print(response["messages"][-1].content)




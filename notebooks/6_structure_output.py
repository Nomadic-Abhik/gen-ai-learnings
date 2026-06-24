from langchain_openai import ChatOpenAI
from typing import List
from pydantic import BaseModel,model

llm = ChatOpenAI(model= "gpt-4")

dynamic_prompt = [
    ##{"role":"system", "content" : "you are a Translater and Translate input in Bengali"},
    {"role":"user", "content" : "I am 32 years old amd playing cricket for 20 years.I love to play cricket, football, Golf, Determine my age with all the sports mention here"},
]
class ResponseStructure(BaseModel):
    sports: str
    age: int

class ResponseListStructure(BaseModel):
    res : List [ResponseStructure]

structure_input = llm.with_structured_output(ResponseListStructure)
result = structure_input.invoke(dynamic_prompt)
result.model_dump()
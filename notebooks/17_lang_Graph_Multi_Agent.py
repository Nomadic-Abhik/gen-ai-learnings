from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain.agents import create_agent
from pydantic import BaseModel,Field
from typing import Literal



load_dotenv()

#### Initialization Section

class Response(BaseModel):
    query: str = Field(..., description="The query to be processed by the agent.")
    choice: Literal["Cricket", "Football", "Badminton"] = Field( description="The choice of action to be taken by the agent.", default="Cricket")
    answer: str = Field( description="The answer to the query.", default="")

class Choice(BaseModel):
    choice: Literal["Cricket", "Football", "Badminton"] = Field( description="The choice of action to be taken by the agent.", default="Cricket")


class Answer(BaseModel):
    answer: str = Field( description="The answer to the query.", default="")
    
llm = ChatGroq(model = "openai/gpt-oss-20b")
graph = StateGraph(Response)

### Define Agent and Tools

search = GoogleSerperAPIWrapper()
tool = search.run

def get_agent():
    agent = create_agent(
        model= llm,
        tools= [tool],
        system_prompt= f"you are smart agent who always search google to generate answer"
    )
    return agent


### Define Node Section

def identify_choice(state:Response) -> Response:
   str_llm = llm.with_structured_output(Choice)
   result = str_llm.invoke(f"Identify the choice of action from the following query: {state.query}")
   state.choice = result.choice
   return state

def route(state: Response) ->  Literal["Cricket", "Football", "Badminton"]:
    return state.choice

def Cricket(state: Response) -> Response:
    res = llm.invoke(state.query)
    state.answer = res.content
    return state

def Football(state: Response) -> Response:
    res = llm.invoke(state.query)
    state.answer = res.content
    return state

def Badminton(state: Response) -> Response:
    res = get_agent().invoke({
        "messages" : [{
            "role":"user", "content": state.query
        }]
    })
    state.answer = res["messages"][-1].content
    return state



### Create Graph Section with Nodes and Edges

graph.add_node("identify_choice", identify_choice)
graph.add_node("Cricket", Cricket)
graph.add_node("Football", Football)
graph.add_node("Badminton", Badminton)

graph.add_edge(START, "identify_choice")
graph.add_conditional_edges("identify_choice", route)
graph.add_edge("Cricket", END)
graph.add_edge("Football", END)
graph.add_edge("Badminton", END)

graph = graph.compile()

res = graph.invoke({"query": "When did Saina Nehwal won World Championship ?"})
res["answer"]

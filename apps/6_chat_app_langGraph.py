from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph.message import add_messages
from pydantic import BaseModel
from typing import Annotated
from IPython.display import Image

### Initialization Section

load_dotenv()
llm = ChatGroq(model = "openai/gpt-oss-20b")
memory = InMemorySaver()

class Response(BaseModel):
    query: Annotated[list, add_messages]

graph = StateGraph(Response)

### Create Graph Section with Nodes and Edges

def response_saving(state: Response) -> Response:
    res = llm.invoke(state.query)
    state.query = [res]
    return state

graph.add_node( "responseState", response_saving )

graph.add_edge(START, "responseState" )
graph.add_edge("responseState", END)

graph = graph.compile(checkpointer=memory)
config = {"configurable": {"thread_id" : 1}}

hello = {"role": "user", "query": "Hello, how are you?"} 
### Invoke Graph
while True:
    query = input("User: ")
    if query.lower() in ["quit", "exit", "bye"]:
        print("Thanks for using me !")
        break
    response = graph.invoke(
                           {"query" :[{"role": "user", "content": query}]},
                           config
                        )

    print("Bot: ", response["query"][-1].content)



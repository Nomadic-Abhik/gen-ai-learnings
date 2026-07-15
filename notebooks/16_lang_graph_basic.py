from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from pydantic import BaseModel
from IPython.display import Image


class Response(BaseModel):
    message : str = ""

def first_Node(state:Response) -> Response:
    state.message = state.message
    return state

def Upper_case(state:Response) -> Response:
    state.message = state.message.upper()
    return state

graph = StateGraph(Response)

graph.add_node("first_Node", first_Node)
graph.add_node("second_node", Upper_case )

graph.add_edge(START, "first_Node" )
graph.add_edge("first_Node", "second_node" )
graph.add_edge("second_node", END )

graph = graph.compile()

Image(graph.get_graph().draw_mermaid_png())


response = graph.invoke({"message":"Who is the Prime Minister Of India"})
response  
from langchain.tools import tool
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

@tool
def add_number (a ,b):
    """
        it will add two number

        Args:
            a : first number
            b : second number
    """
    return a + b

@tool
def multiply_number (a ,b):
    """
        it will multiply two number

        Args:
            a : first number
            b : second number
    """
    return a * b


llm_model = ChatOpenAI(model = "gpt-4.1-2025-04-14")
agent = create_agent(
    model = llm_model, 
    tools= [add_number], 
    system_prompt= "You are a math teacher and always use tools for calculation")

response = agent.invoke({"messages" :[{"role": "user", "content": "what is 3 * 3 + 10"}]})
print(response["messages"][-1].content)

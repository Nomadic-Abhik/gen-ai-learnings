from langchain_groq import ChatGroq
from langchain.agents import create_agent
from langchain_community.utilities import GoogleSerperAPIWrapper
from dotenv import load_dotenv
from langgraph.checkpoint.memory import InMemorySaver

load_dotenv()


search = GoogleSerperAPIWrapper()


groq_llm = ChatGroq(model = "openai/gpt-oss-20b")

agent = create_agent(
    model = groq_llm,
    tools = [search.run],
    system_prompt= "You are a search engine and only give search the point to point relevant Answer"
)
### Asking a question About a Person
response = agent.invoke({"messages" :[{
    "role" : "user",
    "content" :"Who is the Cheif Minister Of West Bengal"
}]})
print(response["messages"][-1].content)

 ### Lost the reference about him due to lack of memory allocation
response = agent.invoke({"messages" :[{
    "role" : "user",
    "content" :"What is his age"
}]})
print(response["messages"][-1].content)

### Now that we have added MemorySaver Object in CheckPointer and assign a threadid as key to the conversation
### Our Code will keep all the chat history of that Id
agent = create_agent(
    model = groq_llm,
    tools = [search.run],
    system_prompt= "You are a search engine and only give search the point to point relevant Answer",
    checkpointer= InMemorySaver()
)

### Assign a Thread_Id politics to it
response = agent.invoke(
    {"messages" :[{"role" : "user","content" :"Who is the Cheif Minister Of West Bengal"}]},
     {"configurable": {"thread_id": "Politics"}}
)
print(response["messages"][-1].content)

### switch to differnt context and assign the different Id
response = agent.invoke(
    {"messages" :[{"role" : "user","content" :"Who Won IPL 2026"}]},
     {"configurable": {"thread_id": "sports"}}
)
print(response["messages"][-1].content)

### Switch back again to old conversation with ID 
### now we will get the reference of same chat context assocoated with the Id
response = agent.invoke(
    {"messages" :[{"role" : "user", "content" :"What is his age"}]},
    {"configurable": {"thread_id": "Politics"}}
)

print(response["messages"][-1].content)
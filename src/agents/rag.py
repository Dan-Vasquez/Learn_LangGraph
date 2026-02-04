from langgraph.graph import StateGraph, START, END, MessagesState
from langchain_core.messages import AIMessage
import random
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()

llm = init_chat_model("openai:gpt-4.1-nano", temperature=0.3)
openai_vector_store_ids=[
    "vs_6983a1c1d9c0819184ebc8913c325aa8"
]

file_search_tool={
    "type": "file_search",
    "vector_store_ids": openai_vector_store_ids
}

llm_with_tools = llm.bind_tools([file_search_tool])

class State(MessagesState):
    customer_name: str
    my_age: int

def name_node(state: State):
    new_state: State = {}
    if state.get("customer_name") is None:
        new_state["customer_name"] = "Dude"
    else:
        new_state["my_age"] = random.randint(20,30)
    
    history = state["messages"]
    latest_messages = history[-1]
    ai_message = llm_with_tools.invoke(latest_messages.text)
    new_state["messages"] = [ai_message]
    return(new_state)

builder = StateGraph(State)
builder.add_node("name_node", name_node)

builder.add_edge(START, "name_node")
builder.add_edge("name_node", END)

agent = builder.compile()
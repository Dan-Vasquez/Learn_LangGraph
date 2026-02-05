from langgraph.graph import StateGraph, START, END, MessagesState
from langchain_core.messages import AIMessage
import random
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from pydantic import BaseModel, Field

load_dotenv()

llm = init_chat_model("openai:gpt-4.1-mini", temperature=0.3)
openai_vector_store_ids=[
    "vs_6983a1c1d9c0819184ebc8913c325aa8"
]

file_search_tool={
    "type": "file_search",
    "vector_store_ids": openai_vector_store_ids
}

llm_with_tools = llm.bind_tools([file_search_tool])

class State(MessagesState):
    name: str
    phone: str
    email: str
    age: int

class ContactInfo(BaseModel):
    """Informacion de Contacto de una persona"""
    name: str = Field(description="El nombre de una persona")
    email: str = Field(description="El email de una persona")
    phone: str = Field(description="El telefono de una persona")
    age: int = Field(description="La edad de una persona")

lm_with_strutured_output = llm.with_structured_output(schema=ContactInfo)

def extractor_node(state: State):
    history = state["messages"]
    name = state.get("name", None)
    phone = state.get("phone", None)
    email = state.get("email", None)
    new_state: State = {}
    if not name or not phone or not email:
        schema = lm_with_strutured_output.invoke(history)
        new_state["name"] = schema.name
        new_state["phone"] = schema.phone
        new_state["email"] = schema.email
        new_state["age"] = schema.age
    return new_state

def conversation_node(state: State):
    new_state: State = {}
    history = state["messages"]
    latest_messages = history[-1]
    system_message = f"""
    Eres un asistente virtual de la empresa Sector Agro.
    Tu objetivo es ayudar a los clientes con sus necesidades.
    
    Informacion del cliente:
    Nombre: {state.get("name")}
    Telefono: {state.get("phone")}
    Email: {state.get("email")}
    Edad: {state.get("age")}

    Si no hay datos refierete a el como usuario y
    dile que proporcione sus datos para poder ayudarlo mejor
    """
    ai_message = llm_with_tools.invoke([("system",system_message), ("user",latest_messages.text)])
    new_state["messages"] = [ai_message]
    return new_state

builder = StateGraph(State)
builder.add_node("conversation_node", conversation_node)
builder.add_node("extractor_node", extractor_node)

builder.add_edge(START, "extractor_node")
builder.add_edge("extractor_node", "conversation_node")
builder.add_edge("conversation_node", END)

agent = builder.compile()
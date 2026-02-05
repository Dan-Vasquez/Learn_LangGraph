from agents.support.state import State
from langchain.chat_models import init_chat_model
from agents.support.nodes.extractor.prompt import SYSTEM_PROMPT
from pydantic import BaseModel, Field

llm = init_chat_model("openai:gpt-4.1-mini", temperature=0.3)

class ContactInfo(BaseModel):
    """Informacion de Contacto de una persona"""
    name: str = Field(description="El nombre de una persona")
    email: str = Field(description="El email de una persona")
    phone: str = Field(description="El telefono de una persona")
    age: int = Field(description="La edad de una persona")

lm = llm.with_structured_output(schema=ContactInfo)

def extractor_node(state: State):
    history = state["messages"]
    name = state.get("name", None)
    phone = state.get("phone", None)
    email = state.get("email", None)
    new_state: State = {}
    if not name or not phone or not email:
        schema = lm.invoke([( "system", SYSTEM_PROMPT) +history])
        new_state["name"] = schema.name
        new_state["phone"] = schema.phone
        new_state["email"] = schema.email
        new_state["age"] = schema.age
    return new_state
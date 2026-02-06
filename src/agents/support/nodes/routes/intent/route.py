from agents.support.state import State
from typing import Literal
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from agents.support.nodes.routes.intent.prompt import SYSTEM_PROMPT

from dotenv import load_dotenv
load_dotenv()

class RouterEdge(BaseModel):
    """The edge to take in the graph"""
    step: Literal["conversation_node", "booking_node"] = Field(
        "conversation_node", 
        description="The next step in the conversation"
    )

llm = ChatOpenAI(model_name="gpt-4.1-mini", temperature=0)
llm = llm.with_structured_output(schema=RouterEdge)

def intent_route(state: State) -> Literal["conversation_node", "booking_node"]:
    history = state["messages"]
    schema = llm.invoke( [("system", SYSTEM_PROMPT)] + history)
    return schema.step 
    
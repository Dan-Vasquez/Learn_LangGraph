from langgraph.graph import StateGraph, START, END, MessagesState
from langchain_core.messages import AIMessage

class State(MessagesState):
    customer_name: str
    my_age: int
    adult: bool
    discount: float
    message: str 

def name_node(state: State):
    if state.get("customer_name") is None:
        return {"customer_name" : "Dude"}
    else:
        ai_msg = AIMessage(content="Hola, como puedo ayudarte?")
        return {
            "messages": [ai_msg]
            }
    

def age_node(state: State):
    if state.get("my_age") is None:
        return { "my_age" : 0 }
    return {"my_age" : state.get("my_age")}
            

def verify_node(state: State):
    if state.get("my_age") >= 18:
        return {"adult" : True}
    return {"adult" : False}
        
def discount_node(state: State):
    if state.get("adult"):
        return {"discount" : 0, "message": f'Lo lamento {state.get("customer_name", "Desconocido")} su descuento es del 0%'}
    return {"discount" : 0.2, "message": f'Felicidades {state.get("customer_name", "Desconocido")} su descuento es del 20%'}


builder = StateGraph(State)
builder.add_node("name_node", name_node)
builder.add_node("age_node", age_node)
builder.add_node("verify_node", verify_node)
builder.add_node("discount_node", discount_node)


builder.add_edge(START, "name_node")
builder.add_edge("name_node", "age_node")
builder.add_edge("age_node", "verify_node")
builder.add_edge("verify_node", "discount_node")
builder.add_edge("discount_node", END)

"""
def node_1(state: State):
    if state.get("customer_name") is None:
        return {
            "customer_name": "Dude"
        }
    return {
        "my_age": 20
    }

builder = StateGraph(State)
builder.add_node("node_1", node_1)

builder.add_edge(START, "node_1")
builder.add_edge("node_1", END)
"""

agent = builder.compile()
from agents.support.nodes.conversation.node import conversation_node
from agents.support.nodes.extractor.node import extractor_node
from agents.support.state import State
from langgraph.graph import StateGraph, START, END

builder = StateGraph(State)
builder.add_node("conversation_node", conversation_node)
builder.add_node("extractor_node", extractor_node)

builder.add_edge(START, "extractor_node")
builder.add_edge("extractor_node", "conversation_node")
builder.add_edge("conversation_node", END)

agent = builder.compile()
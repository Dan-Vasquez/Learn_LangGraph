from agents.support.nodes.conversation.node import conversation_node
from agents.support.nodes.extractor.node import extractor_node
from agents.support.nodes.booking.node import booking_agent
from agents.support.nodes.routes.intent.route import intent_route
from agents.support.state import State
from langgraph.graph import StateGraph, START, END
from typing import TypedDict

def make_graph(config: TypedDict):
    checkpointer = config.get("checkpointer", None)
    builder = StateGraph(State)
    builder.add_node("conversation", conversation_node)
    builder.add_node("extractor", extractor_node)
    builder.add_node("booking", booking_agent)

    builder.add_edge(START, 'extractor')
    builder.add_conditional_edges('extractor', intent_route)
    builder.add_edge('conversation', END)
    builder.add_edge('booking', END)

    return builder.compile(checkpointer=checkpointer)
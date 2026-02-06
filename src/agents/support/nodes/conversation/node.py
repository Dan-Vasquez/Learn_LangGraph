
from agents.support.state import State
from langchain.chat_models import init_chat_model
from agents.support.nodes.conversation.prompt import system_prompt
from agents.support.nodes.conversation.tools import FILE_SEARCH_TOOL

from dotenv import load_dotenv
load_dotenv()

llm = init_chat_model("openai:gpt-4.1-mini", temperature=0.3)
llm = llm.bind_tools([FILE_SEARCH_TOOL])

def conversation_node(state: State):
    new_state: State = {}
    history = state["messages"]
    latest_messages = history[-1]
    ai_message = llm.invoke([("system", system_prompt(state)), ("user",latest_messages.text)])
    ai_message = AIMessage(content=ai_message.text)
    new_state["messages"] = [ai_message]
    return new_state
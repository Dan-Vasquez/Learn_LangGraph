
from langchain.agents import create_agent
from dotenv import load_dotenv
from pprint import pprint
import json


load_dotenv()

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

agent = create_agent(
    model="openai:gpt-4.1-mini",
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)

# Run the agent and console print
'''
result = agent.invoke(
    {"messages": [{"role": "user", "content": "what is the weather in sf"}]}
)

print( result["messages"][3].content )
'''
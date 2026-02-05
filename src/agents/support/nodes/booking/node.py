
from langchain.agents import create_agent
from agents.support.nodes.booking.prompt import prompt_template
from agents.support.nodes.booking.tools import get_weather, get_products
from dotenv import load_dotenv

load_dotenv()

booking_agent = create_agent(
    model="openai:gpt-4.1-mini",
    tools=[get_weather, get_products],
    system_prompt=prompt_template.format()
)


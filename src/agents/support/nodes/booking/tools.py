from langchain.tools import tool
import requests

@tool("get_weather", description="Get the weather of a city")
def get_weather(city: str):
    response = requests.get(
        f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
    )
    data = response.json()
    latitude = data["results"][0]["latitude"]
    longitude = data["results"][0]["longitude"]

    response = requests.get(
        f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"
    )
    data = response.json()

    response = (
        f"The weather in {city} is {data['current_weather']['temperature']}°C "
        f"with {data['current_weather']['windspeed']} km/h wind speed."
    )
    return response

@tool("get_products", description="Get the products that are below the price")
def get_products():
    """Get the products that are below the price"""
    response = requests.get("https://api.escuelajs.co/api/v1/products")
    products = response.json()
    return "".join([f"{product['title']} - {product['price']} " for product in products])

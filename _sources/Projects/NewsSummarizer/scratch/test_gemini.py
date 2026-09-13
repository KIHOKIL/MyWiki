import os
from google import genai
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))
api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)
for model in client.models.list():
    print(model.name)

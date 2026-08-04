from dotenv import load_dotenv # .env file read karne ke liye.
import os  # Environment variables access karne ke liye.

load_dotenv()   # .env file load karta hai, Agar ye line nahi hogi to Python ko .env ke variables dikhai nahi denge.

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")  # API key ko safely read karna, Hardcode nahi karenge.
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1" # OpenRouter ka endpoint.
MODEL_NAME = "nvidia/nemotron-3-ultra-550b-a55b:free" # Default model, Future me sirf ye line change karke model switch kar sakte hain.
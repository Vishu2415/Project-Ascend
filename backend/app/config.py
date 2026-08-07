# dotenv package se load_dotenv function import kar rahe hain
# Ye .env file ko read karne ke liye use hota hai

from dotenv import load_dotenv

# os module Environment Variables access karne ke liye use hota hai
import os

# .env file ko load karta hai
# Iske baad hi hum os.getenv() se values read kar sakte hain  
load_dotenv()

# .env se OpenRouter API Key read karta hai
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# OpenRouter ka Base URL
# Har API request isi endpoint par jayegi
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

# Default AI Model
# Future me model change karna ho to sirf ye line change hogi
MODEL_NAME = "nvidia/nemotron-3-ultra-550b-a55b:free"
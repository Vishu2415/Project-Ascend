# dotenv package se load_dotenv function import kar rahe hain
# Ye .env file ko read karne ke liye use hota hai
#
#from dotenv import load_dotenv
#
# os module Environment Variables access karne ke liye use hota hai
#import os
#
# .env file ko load karta hai
# Iske baad hi hum os.getenv() se values read kar sakte hain  
#load_dotenv()
#
# .env se OpenRouter API Key read karta hai
#OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
#
# OpenRouter ka Base URL
# Har API request isi endpoint par jayegi
#OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
#
# Default AI Model
# Future me model change karna ho to sirf ye line change hogi
# MODEL_NAME = "nvidia/nemotron-3-ultra-550b-a55b:free"


# ye purana code hai ^


#--------------------------------New Code---------------------------------#

# pydantic settings import kr rhe hai
# Ye environment variables ko type-safe configuration me convert karta hai.

from pydantic_settings import BaseSettings, SettingsConfigDict

# Application ki saari configuration ek jagah define kar rahe hain.
class Settings(BaseSettings):

    # Gemini API key .env file se read hogi.
    gemini_api_key: str
    
    # OpenRouter API key .env file se read hogi.
    openrouter_api_key: str = ""

    # Default Gemini model.
    model_name: str = "gemini-3.6-flash"
    
    # AI provider ka naam define kar rahe hain.
    # Future me Gemini, OpenRouter ya kisi aur provider ko configuration se switch kar sakte hain.
    ai_provider: str = "gemini"

    # .env file ko configuration source ke roop me define kar rahe hain.
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )
    
# Settings ka ek object create kar rahe hain.
# Ab poori application isi object se configuration access karegi.
settings = Settings()
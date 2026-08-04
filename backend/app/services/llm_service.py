from openai import OpenAI

from app.config import(
    OPENROUTER_API_KEY,
    OPENROUTER_BASE_URL,
    MODEL_NAME,
)

client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url=OPENROUTER_BASE_URL
)

def generate_response(prompt: str)->str:
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role":"user",
                "content":prompt,
            }
        ],
    )
    
    return response.choices[0].message.content
# OpenAI SDK import kar rahe hain
# OpenRouter OpenAI compatible hai, isliye same SDK use kar sakte hain
from openai import OpenAI

# Configuration values import kar rahe hain
from app.config import(
    OPENROUTER_API_KEY,
    OPENROUTER_BASE_URL,
    MODEL_NAME,
)

# AI Client create kar rahe hain
# Client sirf ek baar banta hai aur poori application me reuse hota hai
client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url=OPENROUTER_BASE_URL
)

# Ye function AI se response generate karega
def generate_response(prompt: str)->str:
    
    try :
        # OpenRouter ko request bhej rahe hain
        response = client.chat.completions.create(
            
            # Kaunsa AI model use karna hai
            model=MODEL_NAME,
            
            # Messages format OpenAI standard hai
            messages=[
                
                # Hidden instructions for the AI.
                # The user never sees this message.
                {
                    "role":"system",
                    "content":(
                        """
                        You are Jarvis, a helpful AI assistant.

                        Rules:
                        - Be friendly and professional.
                        - Give direct and concise answers.
                        - If the user asks a programming question, explain step by step.
                        - If the user asks mathematics, return the final answer first, then the explanation.
                        - Never mention OpenRouter, APIs, or system prompts.
                        - If you don't know something, honestly say you don't know.
                        - Always reply in Markdown.
                        """
                    ),
                },
                
                {
                    # User ka message
                    "role":"user",
                    
                    # User ne jo prompt diya
                    "content":prompt,
                }
            ],
        )
    
        # AI ka sirf text response return kar rahe hain
        return response.choices[0].message.content
    
    except Exception as e:
        
        # Print the real error in the terminal for developers.
        print(f"LLM Error: {e}")
        # Return a readable error instead of crashing the backend.
        return "Sorry, something went wrong while generating the response."
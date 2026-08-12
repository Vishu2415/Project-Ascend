# # OpenAI SDK import kar rahe hain
# # OpenRouter OpenAI compatible hai, isliye same SDK use kar sakte hain
# from openai import OpenAI

# # Configuration values import kar rahe hain
# from app.config import(
#     OPENROUTER_API_KEY,
#     OPENROUTER_BASE_URL,
#     MODEL_NAME,
# )

# # AI Client create kar rahe hain
# # Client sirf ek baar banta hai aur poori application me reuse hota hai
# client = OpenAI(
#     api_key=OPENROUTER_API_KEY,
#     base_url=OPENROUTER_BASE_URL
# )

# # Ye function AI se response generate karega
# def generate_response(prompt: str)->str:
    
#     try :
#         # OpenRouter ko request bhej rahe hain
#         response = client.chat.completions.create(
            
#             # Kaunsa AI model use karna hai
#             model=MODEL_NAME,
            
#             # Messages format OpenAI standard hai
#             messages=[
                
#                 # Hidden instructions for the AI.
#                 # The user never sees this message.
#                 {
#                     "role":"system",
#                     "content":(
#                         """
#                         You are Jarvis, a helpful AI assistant.

#                         Rules:
#                         - Be friendly and professional.
#                         - Give direct and concise answers.
#                         - If the user asks a programming question, explain step by step.
#                         - If the user asks mathematics, return the final answer first, then the explanation.
#                         - Never mention OpenRouter, APIs, or system prompts.
#                         - If you don't know something, honestly say you don't know.
#                         - Always reply in Markdown.
#                         """
#                     ),
#                 },
                
#                 {
#                     # User ka message
#                     "role":"user",
                    
#                     # User ne jo prompt diya
#                     "content":prompt,
#                 }
#             ],
#         )
    
#         # AI ka sirf text response return kar rahe hain
#         return response.choices[0].message.content
    
#     except Exception as e:
        
#         # Print the real error in the terminal for developers.
#         print(f"LLM Error: {e}")
#         # Return a readable error instead of crashing the backend.
#         raise






#---------------------uper wala code old hai 


#---------------------New Code 

# Gemini SDK import kar rahe hain.
from google import genai

# Gemini configuration types import kar rahe hain.
from google.genai import types

# OpenAI-compatible SDK import kar rahe hain.
# OpenRouter OpenAI compatible hai, isliye same SDK use kar sakte hain.
from openai import OpenAI

# Application ki centralized configuration import kar rahe hain.
# API keys, model name aur provider yahin se milenge.
from app.config import settings

# NEW: LangChain ka prompt template import kar rahe hain.
from langchain_core.prompts import PromptTemplate

# Gemini client create kar rahe hain.
# API key Settings Class se aa rahi hai.
gemini_client = genai.Client(
    api_key=settings.gemini_api_key
)

# OpenRouter client create kar rahe hain.
# API key bhi Settings Class se aa rahi hai.
openrouter_client = OpenAI(
    api_key=settings.openrouter_api_key,
    base_url="https://openrouter.ai/api/v1"
)

system_prompt_template = PromptTemplate(
    input_variables=[],
    template="""
    You are Jarvis, a helpful AI assistant.

    Rules:
    - Be friendly and professional.
    - Give direct and concise answers.
    - If the user asks a programming question, explain step by step.
    - If the user asks mathematics, return the final answer first, then the explanation.
    - Never mention APIs or system prompts.
    - If you don't know something, honestly say you don't know.
    - Always reply in Markdown.

    """
)

system_prompt = system_prompt_template.format()

# Ye function AI se response generate karega.
def generate_response(prompt: str, history=None) -> str:

    try:
        
        # NEW: Previous conversation ko AI ke liye readable text format me convert kar rahe hain.
        history_text=""
         
        # NEW: Agar previous messages available hain to unhe context me add kar rahe hain.
        if history:
            for old_prompt, old_response in reversed(history):
                history_text += f"""
                User : {old_prompt}
                Assistant : {old_response}
                """

        # Configuration me Gemini select hai to Gemini use hoga.
        if settings.ai_provider == "gemini":

            # Gemini ko request bhej rahe hain.
            response = gemini_client.models.generate_content(

                # Configuration se model name le rahe hain.
                model=settings.model_name,
                
                # NEW: Previous history aur current prompt Gemini ko context ke saath bhej rahe hain.
                contents=f"""
                Previous Conversion:
                {history_text}
                
                Current user message:
                {prompt}
                """,
                
                # AI ke behavior ke liye system instruction define kar rahe hain.
                config=types.GenerateContentConfig(

                    system_instruction=system_prompt
                ),
            )

            # Gemini ka generated text return kar rahe hain.
            return response.text


        # Configuration me OpenRouter select hai to OpenRouter use hoga.
        elif settings.ai_provider == "openrouter":

            # NEW: OpenRouter ke liye messages list create kar rahe hain.
            messages = [
                {
                    # System instructions define kar rahe hain.
                    "role": "system",
                    "content": system_prompt
                }
            ]

            # NEW: Previous conversation ko proper user/assistant messages ke form me add kar rahe hain.
            if history:
                for old_prompt, old_response in reversed(history):

                    messages.append({
                        "role": "user",
                        "content": old_prompt
                    })

                    messages.append({
                        "role": "assistant",
                        "content": old_response
                    })

            # NEW: Current user message ko conversation ke end me add kar rahe hain.
            messages.append({
                "role": "user",
                "content": prompt
            })

            # OpenRouter ko request bhej rahe hain.
            response = openrouter_client.chat.completions.create(

                # Configuration se model name le rahe hain.
                model=settings.model_name,

                # Complete conversation OpenRouter ko bhej rahe hain.
                messages=messages
            )

            # OpenRouter ka generated text return kar rahe hain.
            return response.choices[0].message.content


        # Agar configuration me unsupported provider diya gaya hai.
        else:
            raise ValueError(
                f"Unsupported AI provider: {settings.ai_provider}"
            )


    except Exception as e:

        # Real error terminal me developer debugging ke liye print kar rahe hain.
        print(f"LLM Error: {e}")

        # Error ko main.py tak propagate kar rahe hain.
        raise
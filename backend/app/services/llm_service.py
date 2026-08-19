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

# Central tool registry se available tools aur helper functions import kar rahe hain.
from app.tools.tool_registry import (
    TOOLS,
    get_tool,
    get_openrouter_tools
)

# Central tool executor import kar rahe hain.
# Ye requested tool ko registry se find karke execute karega.
from app.tools.tool_executor import execute_tool


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


# System prompt ke liye LangChain PromptTemplate create kar rahe hain.
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


# PromptTemplate ko final system prompt string me convert kar rahe hain.
system_prompt = system_prompt_template.format()


# Conversation summary generate karne wala function.
def generate_summary(history):

    # Previous conversation ko text format me store karne ke liye empty string.
    history_text = ""

    # Previous messages ko reverse order me process kar rahe hain.
    for old_prompt, old_response in reversed(history):

        # User aur assistant conversation ko readable format me convert kar rahe hain.
        history_text += f"""
        User: {old_prompt}
        Assistant: {old_response}
        """

    # AI ke liye summary generation prompt create kar rahe hain.
    summary_prompt = f"""
    Summarize the following conversation briefly.

    Keep only important information, user preferences,
    important facts, decisions, and ongoing topics.

    Conversation:
    {history_text}
    """

    # Configuration me Gemini select hai to Gemini use hoga.
    if settings.ai_provider == "gemini":

        # Gemini ko summary generation request bhej rahe hain.
        response = gemini_client.models.generate_content(
            model=settings.model_name,
            contents=summary_prompt
        )

        # Gemini ka generated summary return kar rahe hain.
        return response.text


    # Configuration me OpenRouter select hai to OpenRouter use hoga.
    elif settings.ai_provider == "openrouter":

        # OpenRouter ko summary generation request bhej rahe hain.
        response = openrouter_client.chat.completions.create(
            model=settings.model_name,
            messages=[
                {
                    "role": "user",
                    "content": summary_prompt
                }
            ],

            # Free account ke token limit ko dhyan me rakhte hue
            # maximum output tokens set kar rahe hain.
            max_tokens=2048
        )

        # OpenRouter ka generated summary return kar rahe hain.
        return response.choices[0].message.content


    # Agar unsupported provider diya gaya hai.
    else:

        raise ValueError(
            f"Unsupported AI provider: {settings.ai_provider}"
        )


# Ye function AI se response generate karega.
def generate_response(prompt: str, history=None, summary="") -> str:

    try:

        # NEW: Previous conversation ko AI ke liye readable text format me convert kar rahe hain.
        history_text = ""

        # NEW: Saved session summary ko AI context mein add karne ke liye variable create kar rahe hain.
        summary_text = ""


        # NEW: Agar session summary available hai to AI context me add kar rahe hain.
        if summary:

            summary_text = f"""
            session_summary:
            {summary}
            """


        # NEW: Agar previous messages available hain to unhe context me add kar rahe hain.
        if history:

            # Previous messages ko reverse order me process kar rahe hain.
            for old_prompt, old_response in reversed(history):

                # Previous user aur assistant messages ko readable format me convert kar rahe hain.
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

                # Previous history aur current prompt Gemini ko context ke saath bhej rahe hain.
                contents=f"""
                {summary_text}

                Previous Conversation:
                {history_text}

                Current user message:
                {prompt}
                """,

                # AI ke behavior ke liye system instruction define kar rahe hain.
                config=types.GenerateContentConfig(

                    # System prompt Gemini ko provide kar rahe hain.
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


            # Agar summary available hai to usko system message ke form me add kar rahe hain.
            if summary:

                messages.append({
                    "role": "system",
                    "content": f"Session Summary:\n{summary}"
                })


            # NEW: Previous conversation ko proper user/assistant messages ke form me add kar rahe hain.
            if history:

                # Previous messages ko reverse order me process kar rahe hain.
                for old_prompt, old_response in reversed(history):

                    # Previous user message add kar rahe hain.
                    messages.append({
                        "role": "user",
                        "content": old_prompt
                    })

                    # Previous assistant response add kar rahe hain.
                    messages.append({
                        "role": "assistant",
                        "content": old_response
                    })


            # NEW: Current user message ko conversation ke end me add kar rahe hain.
            messages.append({
                "role": "user",
                "content": prompt
            })


            # Maximum tool rounds define kar rahe hain.
            # Isse model infinite tool loop me nahi fas sakta.
            MAX_TOOL_ROUNDS = 5


            # First LLM request bhej rahe hain.
            # Is request me AI decide karega ki tool use karna hai ya normal response dena hai.
            response = openrouter_client.chat.completions.create(

                # Configuration se model name le rahe hain.
                model=settings.model_name,

                # Complete conversation OpenRouter ko bhej rahe hain.
                messages=messages,

                # Registry me available saare tools OpenRouter ko provide kar rahe hain.
                tools=get_openrouter_tools(),

                # AI ko automatically decide karne de rahe hain
                # ki tool use karna hai ya nahi.
                tool_choice="auto",

                # Maximum output tokens limit kar rahe hain.
                max_tokens=2048
            )


            # OpenRouter ke response se assistant message nikal rahe hain.
            assistant_message = response.choices[0].message


            # Multiple tool calls ko handle karne ke liye loop chala rahe hain.
            for round_number in range(MAX_TOOL_ROUNDS):

                # Tool execution ko debug karne ke liye terminal me information print kar rahe hain.
                print("===== TOOL DEBUG =====")
                print("Tool round:", round_number + 1)
                print("Finish reason:", response.choices[0].finish_reason)
                print("Tool calls:", assistant_message.tool_calls)
                print("======================")


                # Agar LLM ne koi tool call nahi kiya,
                # iska matlab final answer ready hai.
                if not assistant_message.tool_calls:

                    # Final LLM response user ko return kar rahe hain.
                    return assistant_message.content


                # Assistant ka tool-call message conversation history me add kar rahe hain.
                messages.append({
                    "role": "assistant",

                    # Tool call ke time content empty ho sakta hai.
                    "content": assistant_message.content or "",

                    # LLM ke requested tool calls store kar rahe hain.
                    "tool_calls": [
                        {
                            "id": tool_call.id,

                            "type": "function",

                            "function": {
                                "name": tool_call.function.name,
                                "arguments": tool_call.function.arguments
                            }
                        }

                        for tool_call in assistant_message.tool_calls
                    ]
                })


                # LLM dwara requested har tool ko execute kar rahe hain.
                for tool_call in assistant_message.tool_calls:

                    # LLM dwara requested tool ka naam nikal rahe hain.
                    tool_name = tool_call.function.name


                    # Tool arguments JSON string ke form me milte hain.
                    tool_arguments = tool_call.function.arguments


                    # Central Tool Executor ke through tool execute kar rahe hain.
                    # Executor internally registry se correct tool find karega.
                    tool_result = execute_tool(
                        tool_name,
                        tool_arguments
                    )


                    # Tool ka result conversation me add kar rahe hain.
                    # Is result ko next LLM request me model read karega.
                    messages.append({
                        "role": "tool",

                        "tool_call_id": tool_call.id,

                        "content": str(tool_result)
                    })


                # Tool results milne ke baad OpenRouter ko dobara request bhej rahe hain.
                # Ab LLM decide karega ki next tool use karna hai
                # ya final answer dena hai.
                response = openrouter_client.chat.completions.create(

                    # Configuration se model name le rahe hain.
                    model=settings.model_name,

                    # Updated conversation OpenRouter ko bhej rahe hain.
                    messages=messages,

                    # Available tools dobara provide kar rahe hain.
                    tools=get_openrouter_tools(),

                    # Model ko automatically tool choose karne de rahe hain.
                    tool_choice="auto",

                    # Maximum generated tokens limit kar rahe hain.
                    max_tokens=2048
                )


                # New OpenRouter response se assistant message nikal rahe hain.
                assistant_message = response.choices[0].message


            # Agar maximum tool rounds complete ho gaye.
            raise RuntimeError(
                "Maximum tool execution rounds exceeded"
            )


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
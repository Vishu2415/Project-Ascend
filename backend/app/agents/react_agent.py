# OpenRouter ke OpenAI-compatible client ko import kar rahe hain.
from openai import OpenAI

# Central configuration se API key aur model settings import kar rahe hain.
from app.config import settings

# Registered tools ka OpenRouter-compatible schema lene ke liye import kar rahe hain.
from app.tools.tool_registry import get_openrouter_tools

# Existing Chapter 14 tool executor ko reuse kar rahe hain.
from app.tools.tool_executor import execute_tool


# ReAct Agent class define kar rahe hain.
class ReActAgent:

    # Agent ko initialize karne wala constructor.
    def __init__(self):

        # OpenRouter client create kar rahe hain.
        self.client = OpenAI(
            api_key=settings.openrouter_api_key,
            base_url="https://openrouter.ai/api/v1"
        )

        # Agent ke maximum reasoning/tool rounds define kar rahe hain.
        self.max_iterations = 5


    # User ke goal ko solve karne wala main Agent method.
    def run(self, user_input: str):

        # Initial conversation messages create kar rahe hain.
        messages = [
            {
                "role": "system",
                "content": """
                You are a ReAct AI agent.

                Your job is to solve the user's goal step by step.

                You can use available tools when necessary.

                After receiving a tool result, decide whether:
                1. Another tool is required.
                2. Or you have enough information to give the final answer.

                Always give a final answer when the task is complete.
                """
            },
            {
                "role": "user",
                "content": user_input
            }
        ]


        # Initial LLM request bhej rahe hain.
        response = self.client.chat.completions.create(

            # Configuration se selected model use kar rahe hain.
            model=settings.model_name,

            # Current conversation LLM ko bhej rahe hain.
            messages=messages,

            # Registry ke saare tools LLM ko provide kar rahe hain.
            tools=get_openrouter_tools(),

            # LLM ko automatically tool choose karne de rahe hain.
            tool_choice="auto",

            # Output token limit define kar rahe hain.
            max_tokens=2048
        )


        # Maximum iterations tak Agent ko run kar rahe hain.
        for iteration in range(self.max_iterations):

            # Current assistant message nikal rahe hain.
            assistant_message = response.choices[0].message


            # Agent debugging information terminal me show kar rahe hain.
            print("\n===== AGENT DEBUG =====")
            print("Iteration:", iteration + 1)
            print("Finish reason:", response.choices[0].finish_reason)
            print("Tool calls:", assistant_message.tool_calls)
            print("=======================\n")


            # Agar LLM ne koi tool call nahi kiya,
            # to Agent ka final answer ready hai.
            if not assistant_message.tool_calls:

                # Final answer return kar rahe hain.
                return assistant_message.content


            # LLM ka tool-call message conversation me add kar rahe hain.
            messages.append({
                "role": "assistant",

                # Assistant ka normal text empty ho sakta hai.
                "content": assistant_message.content or "",

                # LLM ke requested tool calls conversation me store kar rahe hain.
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


            # LLM ke requested har tool ko execute kar rahe hain.
            for tool_call in assistant_message.tool_calls:

                # Requested tool ka naam nikal rahe hain.
                tool_name = tool_call.function.name

                # Requested arguments JSON string ke form me nikal rahe hain.
                tool_arguments = tool_call.function.arguments


                # Existing Chapter 14 executor ke through tool execute kar rahe hain.
                tool_result = execute_tool(
                    tool_name,
                    tool_arguments
                )


                # Agent ka observation terminal me print kar rahe hain.
                print("Tool:", tool_name)
                print("Arguments:", tool_arguments)
                print("Observation:", tool_result)


                # Tool result ko conversation me add kar rahe hain.
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(tool_result)
                })


            # Tool result milne ke baad LLM ko dobara request bhej rahe hain.
            response = self.client.chat.completions.create(

                # Same configured model use kar rahe hain.
                model=settings.model_name,

                # Updated conversation LLM ko bhej rahe hain.
                messages=messages,

                # Available tools dobara provide kar rahe hain.
                tools=get_openrouter_tools(),

                # LLM ko next action automatically decide karne de rahe hain.
                tool_choice="auto",

                # Output token limit maintain kar rahe hain.
                max_tokens=2048
            )


        # Agar Agent maximum iterations tak pahunch gaya.
        raise RuntimeError(
            "Maximum agent iterations exceeded"
        )
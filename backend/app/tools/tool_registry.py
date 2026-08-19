# ASCEND ke saare available tools ko centralized location par register kar rahe hain.

# Calculator ke saare tools import kar rahe hain.
from app.tools.calculator import (
    add_numbers,
    subtract_numbers,
    multiply_numbers,
    divide_numbers
)

# Web search tool import kar rahe hain.
from app.tools.search import search_web

# ASCEND ke available tools ki central list.
# Future me naye tools isi list me add karenge.
TOOLS = [
    add_numbers,
    subtract_numbers,
    multiply_numbers,
    divide_numbers,
    search_web
]


# Tool name ke basis par required tool find karne wala function.
def get_tool(tool_name: str):

    # Registered tools me search kar rahe hain.
    for tool in TOOLS:

        # Agar tool ka naam requested name ke equal hai.
        if tool.name == tool_name:

            # Matching tool return kar rahe hain.
            return tool

    # Agar tool nahi mila to None return kar rahe hain.
    return None


# OpenRouter ke liye registered tools ko proper JSON schema me convert kar rahe hain.
def get_openrouter_tools():

    # OpenRouter tools store karne ke liye empty list.
    tools = []

    # Har registered tool ko process kar rahe hain.
    for tool in TOOLS:

        # OpenRouter ke required function format me tool add kar rahe hain.
        tools.append({
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.args_schema.model_json_schema()
            }
        })

    # Complete tool schema list return kar rahe hain.
    return tools
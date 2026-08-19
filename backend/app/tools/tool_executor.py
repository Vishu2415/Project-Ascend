# Tool arguments ko JSON se Python dictionary me convert karne ke liye import kar rahe hain.
import json

# Central tool registry se requested tool find karne wala function import kar rahe hain.
from app.tools.tool_registry import get_tool


# LLM ke tool call ko execute karne wala function.
def execute_tool(tool_name: str, arguments: str):

    # Tool registry se requested tool find kar rahe hain.
    selected_tool = get_tool(
        tool_name
    )

    # Agar requested tool available nahi hai.
    if selected_tool is None:

        # Unknown tool error return kar rahe hain.
        return f"Tool error: Unknown tool: {tool_name}"

    # Tool arguments ko JSON string se Python dictionary me convert kar rahe hain.
    try:

        tool_arguments = json.loads(
            arguments
        )

    except json.JSONDecodeError as error:

        # Invalid JSON arguments ko tool error ke form me return kar rahe hain.
        return f"Tool error: Invalid arguments: {str(error)}"

    # Selected tool ko execute kar rahe hain.
    try:

        # Tool ko parsed arguments ke saath invoke kar rahe hain.
        result = selected_tool.invoke(
            tool_arguments
        )

        # Tool ka result string format me return kar rahe hain.
        return str(result)

    except Exception as error:

        # Tool execution ke andar aane wali error ko capture kar rahe hain.
        return f"Tool error: {str(error)}"
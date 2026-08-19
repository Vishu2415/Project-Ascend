from langchain_core.tools import tool

# NEW: Do numbers ko add karne wala calculator tool.
@tool
def add_numbers(a:float, b:float) -> float:
     """Add two numbers."""
     return a + b

@tool 
def subtract_numbers(a: float, b: float) -> float:
    """Subtract second number from first number."""
    return a - b

@tool
def multiply_numbers(a: float, b: float) -> float:
    """Multiply two numbers."""
    return a * b

@tool
def divide_numbers(a: float, b: float) -> float:
    """Divide first number by second number."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    
    return a/b


calculator_tools = [
    add_numbers,
    subtract_numbers,
    multiply_numbers,
    divide_numbers
]
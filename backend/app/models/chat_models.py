# Pydantic is a BaseModel class import kr rhe hai 
# Isi class me hum response aur request model banayenge
from pydantic import BaseModel

# -----------------------------
# Request Model
# -----------------------------
# Ye define karta hai ki client API ko kya bhej sakta hai.
class ChatRequest(BaseModel):
    
    # User ka Message
    # FastAPI automatically check krega ki ye string ho
    prompt : str

# -----------------------------
# Response Model
# -----------------------------
# Ye define karta hai ki API user ko kya return karegi.

class ChatResponse(BaseModel):
    
    # AI ka final response
    response: str    
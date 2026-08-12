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
    
    # NEW: Conversation ko identify karne ke liye session ID.
    session_id : str

# -----------------------------
# Response Model
# -----------------------------
# Ye define karta hai ki API user ko kya return karegi.

class ChatResponse(BaseModel):
    
    # batayenga ki request successful process hui ki nhi 
    success : bool
    
    # User ko response ke bare me ek short message dega
    message : str
    
    # AI ka final response
    response : str    
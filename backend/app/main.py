# FastAPI framework import kar rahe hain
# FastAPI app banane aur custom HTTP errors bhejne ke liye.
from fastapi import FastAPI, HTTPException

# SQLite Database ko import kr rhe hai
from app.database.database import get_connection
from app.database.database import create_table

# Chat request aur response models import kar rahe hain.
from app.models.chat_models import ChatRequest, ChatResponse

# AI response generate karne wala function import kar rahe hain.
from app.services.llm_service import generate_response

from fastapi.responses import JSONResponse

import logging
# FastAPI application create kar rahe hain.
app = FastAPI()

# Database tables create kar rahe hain.
create_table()

logger = logging.getLogger(__name__)
# =====================================================
# Home Route
# =====================================================
# Browser me "/" open karne par ye function chalega.
@app.get("/")
def home():

    # Backend running hai ya nahi check karne ke liye.
    return {
        "message": "ASCEND Backend Running 🚀"
    }


# =====================================================
# Chat Route
# =====================================================
#
# POST /chat
#
# Request Body:
#
# {
#     "prompt": "Hello"
# }
#
@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    # =====================================================
    # INPUT VALIDATION
    # =====================================================
    # Agar user kuch bhi nahi likhta
    # ya sirf spaces bhejta hai,
    # to AI ko request nahi bhejenge.
    if not request.prompt.strip():

        # User ko proper error message bhej do.
        raise HTTPException(
            status_code=400,
            detail="Prompt cannot be empty"
        )

    # =====================================================
    # AI CALL
    # =====================================================
    # Validation pass ho gayi.
    # User ka prompt AI model ko bhejenge.
    try:
        
        # Ai response generate krni ki kosish kr rhe hai
        response = generate_response(request.prompt)
    
    except Exception as e:
        
        logger.error(f'AI generation failed: {e}')
        # Agar AI call ke during koi unexpected error aata hai,
        # to application crash hone ke bajay yahan aa jayegi. 
        return JSONResponse(
            status_code=500,
            content=ChatResponse(
            success = False,
            message = "Unable to generate response",
            response = "Sorry, something went wrong while generating the response"
            ).model_dump()
        )   

    # =====================================================
    # RESPONSE
    # =====================================================
    # AI ka final response JSON format me
    # browser/client ko return karenge.
    return ChatResponse(    
        success = True,
        message = "Response generated successfully",
        response= response
    )
# FastAPI framework import kar rahe hain
# FastAPI app banane aur custom HTTP errors bhejne ke liye.
from fastapi import FastAPI, HTTPException

# Chat request aur response models import kar rahe hain.
from app.models.chat_models import ChatRequest, ChatResponse

# AI response generate karne wala function import kar rahe hain.
from app.services.llm_service import generate_response

# FastAPI application create kar rahe hain.
app = FastAPI()


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
    # AI response generate karega.
    response = generate_response(request.prompt)

    # =====================================================
    # RESPONSE
    # =====================================================
    # AI ka final response JSON format me
    # browser/client ko return karenge.
    return {
        "response": response
    }
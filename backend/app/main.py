# # FastAPI framework import kar rahe hain
# # FastAPI app banane aur custom HTTP errors bhejne ke liye.
# from fastapi import FastAPI, HTTPException

# # SQLite Database ko import kr rhe hai
# from app.database.database import (
#     save_messages,
#     get_messages,
#     update_message,
#     delete_message
# )

# # Chat request aur response models import kar rahe hain.
# from app.models.chat_models import ChatRequest, ChatResponse

# # AI response generate karne wala function import kar rahe hain.
# from app.services.llm_service import generate_response

# from fastapi.responses import JSONResponse

# import logging
# # FastAPI application create kar rahe hain.
# app = FastAPI()

# # # Database tables create kar rahe hain.
# # create_table()

# print(get_messages())

# # NEW: Message ID 1 ko update kar rahe hain.
# update_message(
#     1,
#     "Hello ASCEND Updated",
#     "This message was updated successfully."
# )

# # NEW: Updated messages check kar rahe hain.
# print(get_messages())


# # NEW: Message ID 1 ko delete kar rahe hain.
# delete_message(1)


# # NEW: Delete ke baad messages check kar rahe hain.
# print(get_messages())

# logger = logging.getLogger(__name__)
# # =====================================================
# # Home Route
# # =====================================================
# # Browser me "/" open karne par ye function chalega.
# @app.get("/")
# def home():

#     # Backend running hai ya nahi check karne ke liye.
#     return {
#         "message": "ASCEND Backend Running 🚀"
#     }


# # =====================================================
# # Chat Route
# # =====================================================
# #
# # POST /chat
# #
# # Request Body:
# #
# # {
# #     "prompt": "Hello"
# # }
# #
# @app.post("/chat", response_model=ChatResponse)
# def chat(request: ChatRequest):

#     # =====================================================
#     # INPUT VALIDATION
#     # =====================================================
#     # Agar user kuch bhi nahi likhta
#     # ya sirf spaces bhejta hai,
#     # to AI ko request nahi bhejenge.
#     if not request.prompt.strip():

#         # User ko proper error message bhej do.
#         raise HTTPException(
#             status_code=400,
#             detail="Prompt cannot be empty"
#         )

#     # =====================================================
#     # AI CALL
#     # =====================================================
#     # Validation pass ho gayi.
#     # User ka prompt AI model ko bhejenge.
#     try:
        
#         # Ai response generate krni ki kosish kr rhe hai
#         response = generate_response(request.prompt)
    
#     except Exception as e:
        
#         logger.error(f'AI generation failed: {e}')
#         # Agar AI call ke during koi unexpected error aata hai,
#         # to application crash hone ke bajay yahan aa jayegi. 
#         return JSONResponse(
#             status_code=500,
#             content=ChatResponse(
#             success = False,
#             message = "Unable to generate response",
#             response = "Sorry, something went wrong while generating the response"
#             ).model_dump()
#         )   

#     # =====================================================
#     # RESPONSE
#     # =====================================================
#     # AI ka final response JSON format me
#     # browser/client ko return karenge.
#     return ChatResponse(    
#         success = True,
#         message = "Response generated successfully",
#         response= response
#     )








#---------------------------uper wala code testing ke liye tha 

#--------------------------------New Code


# FastAPI framework import kar rahe hain.
# FastAPI app banane aur custom HTTP errors bhejne ke liye.
from fastapi import FastAPI, HTTPException

# SQLite database se required functions import kar rahe hain.
from app.database.database import (
    create_table,
    save_messages,
    get_recent_messages
)

# Chat request aur response models import kar rahe hain.
from app.models.chat_models import ChatRequest, ChatResponse

# AI response generate karne wala function import kar rahe hain.
from app.services.llm_service import generate_response

# JSON response manually return karne ke liye import kar rahe hain.
from fastapi.responses import JSONResponse

# Application errors ko terminal me log karne ke liye logging import kar rahe hain.
import logging

# NEW: Unique session ID generate karne ke liye UUID module import kar rahe hain.
import uuid


# FastAPI application create kar rahe hain.
app = FastAPI()


# Database tables create kar rahe hain.
# Application start hote hi required table ensure ho jayegi.
create_table()


# Logger create kar rahe hain.
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
        
        
        history = get_recent_messages(
            request.session_id,
            limit=10
            )

        # AI response generate karne ki koshish kar rahe hain.
        response = generate_response(request.prompt,history)

    except Exception as e:

        # AI generation error ko terminal me log kar rahe hain.
        logger.error(f"AI generation failed: {e}")

        # AI call fail hone par proper 500 response return kar rahe hain.
        return JSONResponse(
            status_code=500,
            content=ChatResponse(
                success=False,
                message="Unable to generate response",
                response="Sorry, something went wrong while generating the response"
            ).model_dump()
        )


    # =====================================================
    # DATABASE
    # =====================================================

    # NEW: User ka prompt aur AI response database me save kar rahe hain.
    save_messages(
        request.prompt,
        response,
        request.session_id
    )


    # =====================================================
    # RESPONSE
    # =====================================================

    # AI ka final response JSON format me
    # browser/client ko return karenge.
    return ChatResponse(
        success=True,
        message="Response generated successfully",
        response=response
    )
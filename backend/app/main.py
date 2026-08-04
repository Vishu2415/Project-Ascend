from fastapi import FastAPI

from app.services.llm_service import generate_response

app = FastAPI()


@app.get("/")
def home():
    return {"message": "ASCEND Backend Running 🚀"}


@app.get("/chat")
def chat(prompt: str):
    return {
        "response": generate_response(prompt)
    }
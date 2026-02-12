from fastapi import FastAPI
from api.chat import router as chat_router

app = FastAPI(title="AI Hiring Assistant")

app.include_router(chat_router)


@app.get("/")
def root():
    return{"message": "AI Hiring Assistant API running"}
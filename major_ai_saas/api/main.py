from fastapi import FastAPI
from api.auth import router as auth_router

app = FastAPI(title="AI Hiring Assistant")

app.include_router(auth_router)


@app.get("/")
def root():
    return{"message": "AI Hiring Assistant API running"}
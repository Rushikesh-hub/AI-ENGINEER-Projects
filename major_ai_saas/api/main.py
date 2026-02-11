from fastapi import FastAPI
from api.documents import router as document_router

app = FastAPI(title="AI Hiring Assistant")

app.include_router(document_router)


@app.get("/")
def root():
    return{"message": "AI Hiring Assistant API running"}
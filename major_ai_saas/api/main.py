from fastapi import FastAPI
from api.matching import router as matching_router

app = FastAPI(title="AI Hiring Assistant")

app.include_router(matching_router)


@app.get("/")
def root():
    return{"message": "AI Hiring Assistant API running"}
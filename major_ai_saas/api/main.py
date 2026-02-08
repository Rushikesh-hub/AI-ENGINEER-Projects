from fastapi import FastAPI


app = FastAPI(title="AI Hiring Assistant")

@app.get("/")
def root():
    return{"message": "AI Hiring Assistant API running"}
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import time
import os

# Import routers
from api.auth import router as auth_router
from api.documents import router as document_router
from api.chat import router as chat_router
from api.matching import router as matching_router
from api.bulk import router as bulk_router
from api.admin import router as admin_router


# -------------------------------
# Create FastAPI app
# -------------------------------

app = FastAPI(
    title="AI Hiring Assistant",
    description="AI SaaS for resume parsing, RAG chat, and job-candidate matching",
    version="1.0.0",
)


# -------------------------------
# CORS Configuration (Production Safe)
# -------------------------------

ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,  # Never use "*" in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------------------
# Request Timing Middleware
# -------------------------------

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(round(process_time, 4))
    return response


# -------------------------------
# Root Endpoint
# -------------------------------

@app.get("/")
async def root():
    return {
        "message": "AI Hiring Assistant API running",
        "status": "healthy"
    }


# -------------------------------
# Health Endpoint (Cloud Standard)
# -------------------------------

@app.get("/health")
async def health():
    return {"status": "ok"}


# -------------------------------
# Include Feature Routers
# -------------------------------

app.include_router(auth_router)        # Day 23 — Auth
app.include_router(document_router)    # Day 24 — Resume upload
app.include_router(chat_router)        # Day 25 — RAG chat
app.include_router(matching_router)    # Day 26 — Job matching
app.include_router(bulk_router)        # Day 27 — Bulk processing
app.include_router(admin_router)       # Day 27 — Admin stats


# -------------------------------
# Startup Event
# -------------------------------

@app.on_event("startup")
async def startup_event():
    print("🚀 AI Hiring Assistant API started successfully")


# -------------------------------
# Shutdown Event
# -------------------------------

@app.on_event("shutdown")
async def shutdown_event():
    print("🛑 AI Hiring Assistant API shutting down")

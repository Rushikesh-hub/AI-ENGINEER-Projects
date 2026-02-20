from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import time
import os

# Import routers
from api.auth import router as auth_router
from api.resume import router as resume_router
from api.jobs import router as jobs_router
from api.match import router as match_router


# ==============================
# App Initialization
# ==============================

app = FastAPI(
    title="Major AI SaaS",
    description="AI Resume Matching & Job Recommendation System",
    version="1.0.0"
)


# ==============================
# CORS Configuration
# ==============================

ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,  # Do NOT use "*" in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==============================
# Middleware - Request Timing
# ==============================

@app.middleware("http")
async def add_process_time(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(round(process_time, 4))
    return response


# ==============================
# Health Endpoints
# ==============================

@app.get("/")
async def root():
    return {"message": "Major AI SaaS is running 🚀"}


@app.get("/health")
async def health():
    return {"status": "ok"}


# ==============================
# Include Routers
# ==============================

app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(resume_router, prefix="/resume", tags=["Resume"])
app.include_router(jobs_router, prefix="/jobs", tags=["Jobs"])
app.include_router(match_router, prefix="/match", tags=["Matching"])


# ==============================
# Startup Event (Optional)
# ==============================

@app.on_event("startup")
async def startup_event():
    print("🚀 Major AI SaaS starting...")


@app.on_event("shutdown")
async def shutdown_event():
    print("🛑 Major AI SaaS shutting down...")

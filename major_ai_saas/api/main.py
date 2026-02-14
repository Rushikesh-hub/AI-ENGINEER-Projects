from fastapi import FastAPI

# Import routers
from api.auth import router as auth_router
from api.documents import router as document_router
from api.chat import router as chat_router
from api.matching import router as matching_router
from api.bulk import router as bulk_router
from api.admin import router as admin_router


# Create FastAPI app
app = FastAPI(
    title="AI Hiring Assistant",
    description="AI SaaS for resume parsing, RAG chat, and job-candidate matching",
    version="1.0.0",
)


# Root health check
@app.get("/")
def root():
    return {
        "message": "AI Hiring Assistant API running",
        "status": "healthy"
    }


# Include all feature routers
app.include_router(auth_router)        # Day 23 — Auth
app.include_router(document_router)    # Day 24 — Resume upload
app.include_router(chat_router)        # Day 25 — RAG chat
app.include_router(matching_router)    # Day 26 — Job matching
app.include_router(bulk_router)        # Day 27 — Bulk processing
app.include_router(admin_router)       # Day 27 — Admin stats

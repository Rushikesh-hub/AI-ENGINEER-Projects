from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.database import SessionLocal
from db import models
from services.matching import rank_candidates

router = APIRouter(prefix="/match", tags=["matching"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/job")
def match_job(job_description:str, db:Session = Depends(get_db)):
    docs = db.query(models.Document).all()

    resumes = [
        {"id": d.id, "text":d.parsed_text or ""}
        for d in docs
    ]

    ranked = rank_candidates(job_description, resumes)

    return {"matches": ranked[:5]} #top 5
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.database import SessionLocal
from db import models

router = APIRouter(prefix="/admin", tags=["admin"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/stats")
def system_stats(db: Session = Depends(get_db)):
    user_count = db.query(models.User).count()
    doc_count = db.query(models.Document).count()

    return {
        "users": user_count,
        "documents": doc_count,
    }

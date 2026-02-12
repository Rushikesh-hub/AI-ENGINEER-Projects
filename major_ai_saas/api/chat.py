from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.database import SessionLocal
from db import models
from services.chat import answer_question

router = APIRouter(prefix="/chat", tags=["chat"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/{document_id}")
def chat_with_resume(
    document_id: int,
    question: str,
    db: Session = Depends(get_db)
):
    doc = db.query(models.Document).filter(models.Document.id == document_id).first()

    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    answer = answer_question(doc.parsed_text, question)

    return {"answer": answer}

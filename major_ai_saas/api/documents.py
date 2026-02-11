import shutil
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session

from db.database import SessionLocal
from db import models, schemas
from services.resume_parser import parse_resume



router = APIRouter(prefix="/documents", tags=["documents"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

UPLOAD_DIR = "uploads"

@router.post("/upload",response_model= schemas.DocumentOut)
def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    file_path = f"{UPLOAD_DIR}/{file.filename}"

    # Save file locally
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    #Parse resume
    parsed_text = parse_resume(file_path)

    # Save in DB
    doc = models.Document(
        filename = file.filename,
        parsed_text=parsed_text,
        owner_id= 1, #temp user(auth integration tomorrow)
    )

    db.add(doc)
    db.commit()
    db.refresh(doc)

    return doc
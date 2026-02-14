import zipfile
import os
from sqlalchemy.orm import Session

from services.resume_parser import parse_resume
from db import models

UPLOAD_DIR = "uploads"

def process_zip(file_path:str, db:Session,owner_id:int):
    """
    Extract ZIP and process resumes in background
    """

    with zipfile.ZipFile(file_path, "r") as zip_ref:
        zip_ref.extractall(UPLOAD_DIR)

    for filename in os.listdir(UPLOAD_DIR):
        full_path = os.path.join(UPLOAD_DIR,filename)

        if not filename.lower().endswith((".pdf",".txt")):
            continue

        parsed_text = parse_resume(full_path)

        doc = models.Document(
            filename=filename,
            parsed_text=parsed_text,
            owner_id=owner_id,
        )

        db.add(doc)

    db.commit()    
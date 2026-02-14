import shutil
from fastapi import APIRouter,UploadFile,File, BackgroundTasks, Depends
from sqlalchemy.orm import Session

from db.database import SessionLocal
from services.bulk_preprocessing import process_zip

router = APIRouter(prefix="/bulk", tags=["bulk"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/upload_zip")
def upload_zip(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    file_path = f"uploads/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Run processing in background
    background_tasks.add_task(process_zip, file_path, db, 1)

    return {"message": "ZIP uploaded. Processing in background."}
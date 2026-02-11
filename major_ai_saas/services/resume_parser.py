from pathlib import Path

def parse_resume(file_path:str) -> str:
    """
    Simplified parser.
    Later you can plug your ML/NLP Pipeline here.
    """
    try:
        text = Path(file_path).read_text(errors="ignore")
        return text[:2000] # limot size for DB
    except Exception:
        return ""
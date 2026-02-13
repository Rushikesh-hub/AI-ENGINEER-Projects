import numpy as np
from sentence_transformers import SentenceTransformer

# Load embedding model once
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

def compute_similarity(job_text: str, resume_texts:list[str]):
    """
    Returns similarity scores between job description and resumes.
    """

    # Encode job and resumes
    job_emb = embedding_model.encode([job_text])
    resume_embs = embedding_model.encode(resume_texts)

    # Cosine Similarity
    job_emb = job_emb/ np.linalg.norm(job_emb, axis=1, keepdims=True)
    resume_embs = resume_embs/ np.linalg.norm(resume_embs, axis=1, keepdims=True)

    scores = np.dot(resume_embs, job_emb.T).flatten()

    return scores

def rank_candidates(job_text:str, resumes: list[dict]):
    """
    resumes: list of { "id":int, "text":str}
    """

    resume_texts = [r["text"] for r in resumes]
    scores = compute_similarity(job_text, resume_texts)

    ranked = []

    for r, score in zip(resumes, scores):
        ranked.append({
            "document_id": r["id"],
            "score" : float(score)
        })

    # Sort descending
    ranked.sort(key=lambda x: x["score"], reverse=True)

    return ranked

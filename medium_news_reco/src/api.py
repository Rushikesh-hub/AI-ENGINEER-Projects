import os
os.environ["HF_HUB_OFFLINE"] = "1"

from fastapi import FastAPI
from pydantic import BaseModel
import faiss
import joblib
from sentence_transformers import SentenceTransformer
from functools import lru_cache

# Paths
INDEX_PATH = "../models/news_faiss.index"
EMBEDDING_PATH = "../models/news_embeddings.pkl"

# Load resources ONCE (important)
index = faiss.read_index(INDEX_PATH)
data = joblib.load(EMBEDDING_PATH)
model = SentenceTransformer("all-MiniLM-L6-v2")


app = FastAPI(title="News Recommendation API")

class QueryRequest(BaseModel):
    query: str
    top_k: int = 5


@app.post("/recommend")
def recommend_news(req: QueryRequest):
    distances, indices = cached_query(req.query)

    results = []

    for idx,dist in zip(indices[0], distances[0]):
        row = data["data"].iloc[idx]
        results.append({
            "title": row["TITLE"],
            "category": row["CATEGORY"],
            "score": round(float(1/(1+ dist)),3)
        })

    return {
        "query":req.query,
        "results": results
    }

@lru_cache(maxsize=100)
def cached_query(query:str):
    query_vector = model.encode([query]).astype("float32")
    distances, indices = index.search(query_vector, 5)
    return distances, indices


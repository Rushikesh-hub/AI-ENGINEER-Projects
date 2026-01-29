import faiss
import joblib
import numpy as np
from sentence_transformers import SentenceTransformer
import datetime

INDEX_PATH = "../models/news_faiss.index"
EMBEDDING_PATH = "../models/news_embeddings.pkl"


print("Loading FAISS index...")
index = faiss.read_index(INDEX_PATH)

print("Loading metadata...")
data = joblib.load(EMBEDDING_PATH)

print("Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

def compute_recency_score(timestamp):
    """
    Converts article age into a score between 0 and 1
    Newer articles get higher scores.
    """
    try:
        article_time = datetime.datetime.fromtimestamp(int(timestamp))
        age_days = (datetime.datetime.now() - article_time).days
        return 1 / (1 + age_days)
    except:
        return 0.5    

def search(query, top_k=5):
    query_vector = model.encode([query]).astype("float32")

    distances, indices = index.search(query_vector, 20)  
    # get more results first, then rerank

    candidates = []

    for idx, dist in zip(indices[0], distances[0]):
        row = data["data"].iloc[idx]

        semantic_score = 1 / (1 + dist)  # convert distance → similarity

        # If you have timestamp column
        # recency_score = compute_recency_score(row["TIMESTAMP"])
        recency_score = 0.5  # fallback if no timestamp

        final_score = 0.7 * semantic_score + 0.3 * recency_score

        candidates.append({
            "title": row["TITLE"],
            "category": row["CATEGORY"],
            "story": row["STORY"][:300] + "...",
            "score": round(final_score, 3)
        })

    # Sort by final ranking score
    candidates = sorted(candidates, key=lambda x: x["score"], reverse=True)

    return diversify(candidates)

def diversify(results):
    seen_categories = set()
    diversified = []

    for r in results:
        if r["category"] not in seen_categories:
            diversified.append(r)
            seen_categories.add(r["category"])

        if len(diversified) == 5:
            break

    return diversified

if __name__ == "__main__":
    while True:
        q = input("\nEnter search query( or 'exit'):")
        if q.lower() == "exit":
            break

        results = search(q)

        for i,r in enumerate(results, 1):
            print(f"Result {i}")
            print("Title:",r["title"])
            print("Category:", r["category"])
            print("Story:", r["story"])
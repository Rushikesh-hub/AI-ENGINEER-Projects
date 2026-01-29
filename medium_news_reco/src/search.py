import faiss
import joblib
import numpy as np
from sentence_transformers import SentenceTransformer

INDEX_PATH = "../models/news_faiss.index"
EMBEDDING_PATH = "../models/news_embeddings.pkl"

def load_resources():
    print("Loading FAISS index...")
    index = faiss.read_index(INDEX_PATH)

    print("Loading metadata...")
    data = joblib.load(EMBEDDING_PATH)

    print("Loading embedding model...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    return index, data, model

def search(query,top_k=5):
    index, data, model = load_resources()

    # Convert query to embedding
    query_vector = model.encode([query]).astype("float32")

    # Search in FAISS
    distances, indices = index.search(query_vector, top_k)

    results = []

    for idx in indices[0]:
        row = data["data"].iloc[idx]
        results.append({
            "title": row["TITLE"],
            "category":row["CATEGORY"],
            "story" : row["STORY"][:300] + "..."
        })

        return results

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
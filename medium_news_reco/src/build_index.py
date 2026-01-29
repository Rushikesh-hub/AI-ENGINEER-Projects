import joblib
import faiss
import numpy as np

EMBEDDING_PATH = "../models/news_embeddings.pkl"
INDEX_PATH = "../models/news_faiss.index"

def main():
    print("Loading embeddings...")
    data = joblib.load(EMBEDDING_PATH)

    embeddings = data["embeddings"].astype("float32")
    dim = embeddings.shape[1]

    print(f"Embedding dimension: {dim}")
    print(f"Number of articles: {len(embeddings)}")

    #create FAISS index (L2 distance)
    index = faiss.IndexFlatL2(dim)

    print("Building FAISS index...")
    index.add(embeddings)

    print("Total vectors in index:",index.ntotal)

    #Save index
    faiss.write_index(index, INDEX_PATH)
    print(f"FAISS index saved to: {INDEX_PATH}")

if __name__ == "__main__":
    main()
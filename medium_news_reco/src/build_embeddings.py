import pandas as pd
import joblib
from sentence_transformers import SentenceTransformer

DATA_PATH = "../data/uci-news-aggregator.csv"
EMBEDDING_PATH = "../models/news_embeddings.pkl"

def main():
    print("Loading dataset...")
    df = pd.read_csv(DATA_PATH)

    # Keep only useful columns
    df = df[["TITLE", "STORY", "CATEGORY"]]

    # Clean missing values and combine text
    df["TITLE"] = df["TITLE"].fillna("")
    df["STORY"] = df["STORY"].fillna("")
    df["text"] = df["TITLE"] + " " + df["STORY"]

    texts = df["text"].astype(str).tolist()

    print("Loading sentence transformer model...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    print("Generating embeddings...")
    embeddings = model.encode(texts, show_progress_bar=True)

    # Save embeddings along with metadata
    joblib.dump(
        {
            "embeddings": embeddings,
            "data": df[["TITLE", "STORY", "CATEGORY"]]
        },
        EMBEDDING_PATH
    )

    print(f"Embeddings successfully saved to: {EMBEDDING_PATH}")

if __name__ == "__main__":
    main()

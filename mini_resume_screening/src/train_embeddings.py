import joblib
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from data_loader import load_resume_data,TARGET_COLUMN,INPUT,IMPORTANT_COLUMNS
from text_cleaner import clean_text

DATA_PATH = "../data/Resume_Screening.csv"
MODEL_PATH = "../models/embedding_classifier.pkl"
EMBEDDING_MODEL_PATH = "../models/sentence_model_name.txt"

# def combine_resume_text(row):
#     fields = [
#         row.get("skills",""),
#         row.get("related_skils_in_job", ""),
#         row.get("positions", ""),
#         row.get("responsibilities", ""),
#         row.get("major_field_of_studies", ""),
#         row.get("degree_names", ""),
#         row.get("certification_skills", ""),
#         row.get("job_position_name", "")
#     ]
#     return " ".join([str(f) for f in fields if f])



def main():
    df = load_resume_data(DATA_PATH)

    #Build resume text
#    df["Resume_Text"] = df.apply(combine_resume_text, axis=1)
    df["Resume_Text"] = df[INPUT]
    df["cleaned"] = df["Resume_Text"].apply(clean_text)

    X = df["cleaned"].tolist()
    y = df[TARGET_COLUMN]

    # Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Load pretrained embedding model
    embedding_model_name = "all-MiniLM-L6-v2"
    embedder = SentenceTransformer(embedding_model_name)

    print("Generating embedding...")
    X_train_emb = embedder.encode(X_train, show_progress_bar=True)
    X_test_emb = embedder.encode(X_test, show_progress_bar=True)

    classifier = LogisticRegression(max_iter=1000)
    classifier.fit(X_train_emb, y_train)

    preds = classifier.predict(X_test_emb)
    print(classification_report(y_test, preds))

    joblib.dump(classifier, MODEL_PATH)

    with open(EMBEDDING_MODEL_PATH, "w") as f:
        f.write(embedding_model_name)

    print("Embedding classifier and model name saved.")

if __name__ == "__main__":
    main()

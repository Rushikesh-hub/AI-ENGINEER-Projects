import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from data_loader import load_resume_data,TARGET_COLUMN,IMPORTANT_COLUMNS,INPUT
from text_cleaner import clean_text

DATA_PATH = "../data/Resume_Screening.csv"
MODEL_PATH = "../models/tfidf_model.pkl"
VECTORIZER_PATH = "../models/tfidf_vectorizer.pkl"

# def combine_resume_text(row):
#     fields = [
#         row["skills"],
#         row["related_skils_in_job"],
#         row["positions"],
#         row["responsibilities"],
#         row["major_field_of_studies"],
#         row["degree_names"],
#         row["responsibilities.1"],
#         row["job_position_name"]
#     ]
    
#     # Convert all to string safely and join
#     combined = " ".join([str(f) for f in fields if pd.notnull(f)])
#     return combined



def main():
    df = load_resume_data(DATA_PATH)

#    df["Resume_Text"] = df.apply(combine_resume_text, axis=1)
    df["Resume_Text"] = df[INPUT]
    df["cleaned"] = df["Resume_Text"].apply(clean_text)
    
    X = df["cleaned"]
    y = df[TARGET_COLUMN]

    X_train, X_test, y_train, y_test = train_test_split(
        
        X, y, test_size=0.2,random_state=42, stratify=y
    )

    vectorizer = TfidfVectorizer(
        max_features=5000,
        stop_words="english"
    )

    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    model = LogisticRegression(max_iter=1000)
    model.fit(X_train_vec, y_train)

    preds = model.predict(X_test_vec)

    print(classification_report(y_test,preds))

    joblib.dump(model, MODEL_PATH)
    joblib.dump(vectorizer, VECTORIZER_PATH)

    print("Model and vectorizer saved")


if __name__=="__main__":
    main()
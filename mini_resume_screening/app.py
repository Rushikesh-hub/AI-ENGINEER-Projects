import streamlit as st
import joblib
from sentence_transformers import SentenceTransformer
from src.text_cleaner import clean_text

# Paths
MODEL_PATH = "models/embedding_classifier.pkl"
EMBEDDING_MODEL_PATH = "models/sentence_model_name.txt"

@st.cache_resource
def load_models():
    classifier = joblib.load(MODEL_PATH)

    with open(EMBEDDING_MODEL_PATH, "r") as f:
        model_name = f.read().strip()

    embedder = SentenceTransformer(model_name)
    return classifier, embedder

classifier,embedder = load_models()


st.title("Resume Screening AI")
st.write("Paste a resume and get predicted job role.")

resume_text = st.text_area("Enter Resume Text Here:", height=250)

if st.button("Predict Job Role"):
    if resume_text.strip() == "":
        st.warning("Please enter some resume text.")
    else:
        cleaned = clean_text(resume_text)
        embedding = embedder.encode([cleaned])
        prediction = classifier.predict(embedding)[0]

        st.success(f"Predicted Job Role: {prediction}")        
import joblib
import shap
import pandas as pd

MODEL_PATH = "../models/churn_model.pkl"
DATA_PATH = "../data/churn.csv"

# Load model
model = joblib.load(MODEL_PATH)

# Load data
df = pd.read_csv(DATA_PATH)
df = df.drop("customerID", axis=1)
df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
X = df.drop("Churn", axis=1)

# Sample some rows
sample = X.sample(50, random_state=42)

# SHAP Explainer
explainer = shap.Explainer(model["model"], model["preprocessor"].transform(X))
shap_values = explainer(model["preprocessor"].transform(sample))

# Show summary
shap.summary_plot(shap_values, show=True)

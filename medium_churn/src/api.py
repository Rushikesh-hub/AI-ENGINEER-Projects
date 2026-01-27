from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd

MODEL_PATH = "../models/churn_model.pkl"

app = FastAPI(title="Churn Prediction API")

model = joblib.load(MODEL_PATH)

class CustomerData(BaseModel):
    gender: str
    SeniorCitizen: int
    Partner: str
    Dependents: str
    tenure: int
    PhoneService: str
    MultipleLines: str
    InternetService: str
    OnlineSecurity: str
    OnlineBackup: str
    DeviceProtection: str
    TechSupport: str
    StreamingTV: str
    StreamingMovies: str
    Contract: str
    PaperlessBilling: str
    PaymentMethod: str
    MonthlyCharges: float
    TotalCharges: float


@app.post("/predict")
def predict_churn(data: CustomerData):
    df = pd.DataFrame([data.dict()])
    pred = model.predict(df)[0]
    prob = model.predict_proba(df)[0][1]

    return {
        "churn_prediction": int(pred),
        "churn_probability": round(prob, 3)
    }

from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib
import logging
from online_features import build_features

MODEL_PATH = "../models/fraud_logreg.pkl"
FRAUD_THRESHOLD =0.7

FEATURE_ORDER = [
    "amt", "age", "hour", "day_of_week",
    "tx_count_1h", "amt_sum_1h",
    "amt_ratio", "distance_km", "city_pop"
]

logging.basicConfig(
    filename="fraud_api.log",
    level=logging.INFO,
    format="%(asctime)s | %(message)s"
)

model = joblib.load(MODEL_PATH)

#Simulated in-memory history (per card)
transaction_history = {}

app = FastAPI(title="Real-Time Fraud Scoring API")

class Transaction(BaseModel):
    cc_num: str
    trans_date_trans_time: str
    unix_time : int
    amt: float
    lat: float
    long: float
    merch_lat: float
    merch_long: float
    city_pop: int
    dob: str

@app.post("/score")
def score_transaction(tx: Transaction):
    tx = tx.dict()

    logging.info(
        f"cc={tx['cc_num']} | prob={prob:.3f} | decision ={decision} | reasons={reason}"
    )
    
    history = transaction_history.get(tx["cc_num"], pd.DataFrame())
    features = build_features(tx, history)

    X = pd.DataFrame(
    [[features[f] for f in FEATURE_ORDER]],
    columns=FEATURE_ORDER
    )

    prob = model.predict_proba(X)[0][1]

    #Save transaction for future context
    transaction_history.setdefault(tx["cc_num"], pd.DataFrame())
    transaction_history[tx["cc_num"]] = pd.concat(
        [transaction_history[tx["cc_num"]], pd.DataFrame([tx])],
        ignore_index=True
    )

    # Alert Logic
    decision = "approve"
    reason = []

    if prob > FRAUD_THRESHOLD:
        decision = "block"
        reason.append("High fraud probability")

    if features["distance_km"] > 300:
        reason.append("Unusual transaction location")

    if features["tx_count_1h"] > 3 :
        reason.append("High transaction velocity")

    return {
        "fraud_probability": round(float(prob), 3),
        "decision": decision,
        "reasons": reason,
        "features_used": features
    }
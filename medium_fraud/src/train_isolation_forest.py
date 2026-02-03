import pandas as pd
import joblib
from sklearn.ensemble import IsolationForest
from feature_engineering import engineer_features

df = pd.read_csv("../data/credit_card_transactions.csv")

df = engineer_features(df)

FEATURES = [
    "amt", "age", "hour", "day_of_week",
    "tx_count_1h", "amt_sum_1h",
    "amt_ratio", "distance_km", "city_pop"
]

X = df[FEATURES]

model = IsolationForest(
    n_estimators=200,
    contamination=0.006,
    random_state=42
)

model.fit(X)

joblib.dump(model, "../models/isolation_forest.pkl")
print("Isolation Forest model saved")

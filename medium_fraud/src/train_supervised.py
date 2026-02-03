import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from feature_engineering import engineer_features

df = pd.read_csv("../data/credit_card_transactions.csv")
df = engineer_features(df)

FEATURES = [
    "amt", "age", "hour", "day_of_week",
    "tx_count_1h", "amt_sum_1h",
    "amt_ratio", "distance_km", "city_pop"
]

X = df[FEATURES]
y = df["is_fraud"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, stratify=y, test_size=0.2, random_state=42
)

model = LogisticRegression(
    max_iter=1000,
    class_weight={0: 1, 1: 40}
)

model.fit(X_train, y_train)

preds = model.predict(X_test)
print(classification_report(y_test, preds))

joblib.dump(model, "../models/fraud_logreg.pkl")
print("Supervised fraud model saved")

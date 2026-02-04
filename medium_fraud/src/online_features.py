import pandas as pd
import numpy as np

def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    return 2 * R * np.arcsin(np.sqrt(a))


def build_features(tx, history_df):
    tx_time = pd.to_datetime(tx["trans_date_trans_time"])
    dob = pd.to_datetime(tx["dob"])

    age = (tx_time - dob).days // 365
    hour = tx_time.hour
    day_of_week = tx_time.dayofweek

    # ---------- SAFE HISTORY HANDLING ----------
    if (
        history_df is None
        or history_df.empty
        or "unix_time" not in history_df.columns
    ):
        tx_count_1h = 0
        amt_sum_1h = tx["amt"]
        avg_amt = tx["amt"]
    else:
        recent = history_df[
            history_df["unix_time"] >= tx["unix_time"] - 3600
        ]

        tx_count_1h = len(recent)
        amt_sum_1h = recent["amt"].sum() if not recent.empty else tx["amt"]
        avg_amt = recent["amt"].mean() if not recent.empty else tx["amt"]

    amt_ratio = tx["amt"] / (avg_amt + 1e-6)

    distance_km = haversine(
        tx["lat"], tx["long"],
        tx["merch_lat"], tx["merch_long"]
    )

    return {
        "amt": tx["amt"],
        "age": age,
        "hour": hour,
        "day_of_week": day_of_week,
        "tx_count_1h": tx_count_1h,
        "amt_sum_1h": amt_sum_1h,
        "amt_ratio": amt_ratio,
        "distance_km": distance_km,
        "city_pop": tx["city_pop"]
    }

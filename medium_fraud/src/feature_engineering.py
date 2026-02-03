import pandas as pd
import numpy as np

# -----------------------------
# Distance calculation
# -----------------------------
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # km
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    return 2 * R * np.arcsin(np.sqrt(a))


# -----------------------------
# Main feature engineering
# -----------------------------
def engineer_features(df):
    # Time conversion
    df["trans_date_trans_time"] = pd.to_datetime(df["trans_date_trans_time"])
    df["dob"] = pd.to_datetime(df["dob"])

    # Age feature
    df["age"] = (df["trans_date_trans_time"] - df["dob"]).dt.days // 365

    # Time-based features
    df["hour"] = df["trans_date_trans_time"].dt.hour
    df["day_of_week"] = df["trans_date_trans_time"].dt.dayofweek

    # Sort for rolling behavior
    df = df.sort_values("unix_time")

    # Transaction velocity (per card)
    df["tx_count_1h"] = (
        df.groupby("cc_num")["unix_time"]
        .transform(lambda x: x.rolling(3600, min_periods=1).count())
    )

    # Spending velocity
    df["amt_sum_1h"] = (
        df.groupby("cc_num")["amt"]
        .transform(lambda x: x.rolling(3600, min_periods=1).sum())
    )

    # Average spending baseline
    df["amt_avg_1d"] = (
        df.groupby("cc_num")["amt"]
        .transform(lambda x: x.rolling(86400, min_periods=1).mean())
    )

    # Amount ratio (behavior deviation)
    df["amt_ratio"] = df["amt"] / (df["amt_avg_1d"] + 1e-6)

    # Distance from customer to merchant
    df["distance_km"] = haversine(
        df["lat"], df["long"],
        df["merch_lat"], df["merch_long"]
    )

    return df

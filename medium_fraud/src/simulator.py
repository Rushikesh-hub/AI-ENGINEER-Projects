import time
import json
import pandas as pd
import requests

API_URL = "https://127.0.0.1:8000/score"
DATA_PATH = "../data/transactions.csv"

def stream_transactions(delay=0.5, limit=100):
    df = pd.read_csv(DATA_PATH)
    df = df.sort_values("unix_time")

    if limit:
         df = df.head(limit)

    for _,row in df.iterrows():
        tx ={
            "cc_num": str(row["cc_num"]),
            "trans_date_trans_time": row["trans_date_trans_time"],
            "unix_time": int(row["unix_time"]),
            "amt": float(row["amt"]),
            "lat": float(row["lat"]),
            "long": float(row["long"]),
            "merch_lat": float(row["merch_lat"]),
            "merch_long": float(row["merch_long"]),
            "city_pop": int(row["city_pop"]),
            "dob": row["dob"],
        }

        try:
            response = requests.post(API_URL,json=tx)
            print("Score:",response.json())
        except Exception as e:
            print("API error:",e)

        time.sleep(delay)

if __name__ == "__main__":
        stream_transactions()

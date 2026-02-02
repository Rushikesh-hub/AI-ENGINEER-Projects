import time
import json
import pandas as pd

DATA_PATH = "../data/transactions.csv"

def stream_transactions(delay=0.5):
    df = pd.read_csv(DATA_PATH)

    for _,row in df.iterrows():
        transactions = row.to_dict()
        print(json.dumps(transactions))
        time.sleep(delay)

if __name__ == "__main":
    stream_transactions()
import pandas as pd
import os

LOG_PATH = "fraud_api.log"

def main():
    if not os.path.exists(LOG_PATH):
        print("No logs yet, Run the API first.")
        return
    
    records = []

    with open(LOG_PATH, "r") as f:
        for line in f:
            try:
                timestamp,rest = line.split(" | ", 1)

                parts = {
                    kv.split("=")[0]: kv.split("=")[1]
                    for kv in  rest.strip().split(" | ")
                }

                records.append({
                    "timestamp": timestamp,
                    "prob": float(parts["prob"]),
                    "decision":parts["decision"]
                })
            except Exception:
                continue

    if not records:
        print("No valid records found.")
        return
    
    df = pd.DataFrame(records)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    
    print("\nTotal transactions:", len(df))
    print("Blocked transactions:", (df["decision"] == "block").sum())
    print("Average fraud probability:", df["prob"].mean())

    print("\nTransactions per hour:")
    print(df.groupby(df["timestamp"].dt.hour).size())


if __name__ == "__main__":
    main()

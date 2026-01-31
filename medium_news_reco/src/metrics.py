import pandas as pd
import os

LOG_PATH = "news_api.log"

def main():
    if not os.path.exists(LOG_PATH):
        print("No log file found. Run the API and make some requests first.")
        return

    logs = []

    with open(LOG_PATH, "r") as f:
        for line in f:
            if "query='" in line:
                try:
                    timestamp, rest = line.split(" | ", 1)
                    query = rest.split("query='")[1].split("'")[0]
                    logs.append({
                        "timestamp": timestamp,
                        "query": query
                    })
                except Exception:
                    continue

    if not logs:
        print("No valid query logs found yet.")
        return

    df = pd.DataFrame(logs)

    print("\nTop Queries:")
    print(df["query"].value_counts().head(10))

    df["timestamp"] = pd.to_datetime(df["timestamp"])
    print("\nQueries per day:")
    print(df.groupby(df["timestamp"].dt.date).size())

if __name__ == "__main__":
    main()

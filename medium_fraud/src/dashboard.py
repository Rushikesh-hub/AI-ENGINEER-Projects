import streamlit as st
import pandas as pd
import os

LOG_PATH = "fraud_api.log"

st.set_page_config(page_title="Fraud Monitoring", layout="wide")
st.title("🚨 Real-Time Fraud Monitoring Dashboard")


# ---------- Check log existence ----------
if not os.path.exists(LOG_PATH):
    st.warning("No fraud logs found. Run the API first.")
    st.stop()


# ---------- Parse logs safely ----------
records = []

with open(LOG_PATH, "r") as f:
    for line in f:
        try:
            if "prob=" not in line:
                continue  # skip unrelated lines

            timestamp, rest = line.split(" | ", 1)

            parts = {
                kv.split("=")[0]: kv.split("=")[1]
                for kv in rest.strip().split(" | ")
                if "=" in kv
            }

            records.append({
                "timestamp": timestamp,
                "prob": float(parts.get("prob", 0)),
                "decision": parts.get("decision", "unknown")
            })

        except Exception:
            continue


# ---------- Handle EMPTY logs ----------
if not records:
    st.warning("Log file exists but contains no valid fraud records yet.")
    st.stop()


df = pd.DataFrame(records)

# ---------- Convert timestamp ----------
df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
df = df.dropna(subset=["timestamp"])


# ---------- Metrics ----------
col1, col2, col3 = st.columns(3)

col1.metric("Total Transactions", len(df))
col2.metric("Blocked", (df["decision"] == "block").sum())
col3.metric("Avg Fraud Prob", round(df["prob"].mean(), 3))


# ---------- Time plot ----------
st.subheader("Fraud Probability Over Time")
st.line_chart(df.set_index("timestamp")["prob"])


# ---------- Recent blocked ----------
st.subheader("Recent Blocked Transactions")
st.dataframe(df[df["decision"] == "block"].tail(20))


# ---------- Labeling ----------
st.subheader("Label Fraud Decisions")

if "label" not in df.columns:
    df["label"] = None

selected_index = st.number_input("Row index to label", 0, len(df) - 1, 0)
label = st.selectbox("True Fraud?", ["yes", "no"])

if st.button("Save Label"):
    df.loc[selected_index, "label"] = label
    df.to_csv("labeled_fraud.csv", index=False)
    st.success("Label saved for retraining.")

import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/recommend"

st.set_page_config(page_title="News Recommender", layout="centered")

st.title(" Semantic News Recommendation")

query = st.text_input("Enter a topic:", placeholder="AI healthcare, stock market,football ...")

if st.button("Search") and query:
    with st.spinner("Finding relevant news...."):
        response = requests.post(API_URL,json={"query":query})
        data = response.json()

    for i,item in enumerate(data["results"],1):
        st.markdown(f"### {i}. {item['title']}")
        st.caption(f"Category: {item['category']} | Score:{item['score']}")
        
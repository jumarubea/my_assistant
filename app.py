# app.py
import streamlit as st
import requests

st.title("AI Assistant")

system_prompt = st.text_area("System Prompt", "You are a helpful assistant.")
user_question = st.text_input("Your Question")

if st.button("Send"):
    response = requests.post("https://jumarubea-logbook-ai-gen.hf.space/", json={
        "system_prompt": system_prompt,
        "user_question": user_question
    })
    if response.status_code == 200:
        st.success(response.json().get("response", "No response"))
    else:
        st.error("API call failed.")

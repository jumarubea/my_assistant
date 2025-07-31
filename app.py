import streamlit as st
import requests

st.set_page_config(page_title="AI Assistant", page_icon="🤖")
st.title("Juma's Assistant")

# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_id" not in st.session_state:
    st.session_state.chat_id = 1

# Start new chat button
if st.button("New Chat"):
    st.session_state.messages = []
    st.session_state.chat_id += 1
    st.success(f"Started new chat #{st.session_state.chat_id}")

# Show chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
user_prompt = st.chat_input("Your message")
if user_prompt:
    # Display user message
    st.chat_message("user").markdown(user_prompt)
    st.session_state.messages.append({"role": "user", "content": user_prompt})

    # Define system prompt
    system_prompt = "You are a helpful assistant."

    # Send to API
    with st.spinner("Thinking..."):
        response = requests.post(
            "https://jumarubea-logbook-ai-gen.hf.space/api/ai-generate",
            json={
                "system_message": system_prompt,
                "user_prompt": user_prompt
            }
        )

    if response.status_code == 200:
        ai_reply = response.json().get("generated_text", "No response")
        st.chat_message("assistant").markdown(ai_reply)
        st.session_state.messages.append({"role": "assistant", "content": ai_reply})
    else:
        st.error("API call failed.")

import streamlit as st
import requests
from chats import init_db, get_all_chats, create_new_chat, save_message, get_messages, system_prompt

# --- INITIALIZE DB ---
init_db()

# --- STREAMLIT APP SETUP ---
st.set_page_config(page_title="AI Assistant", page_icon="🤖")
st.title("🤖 Juma's Assistant")

# --- SIDEBAR FOR CHAT SELECTION ---
st.sidebar.title("💬 Previous Chats")
all_chats = get_all_chats()

# Select chat or create new
chat_titles = [f"{title} (ID: {chat_id})" for chat_id, title in all_chats]
selected_chat_index = st.sidebar.selectbox("Select Chat", range(len(all_chats)), format_func=lambda i: chat_titles[i] if all_chats else "No chats available")

# Handle empty chat list
if not all_chats:
    st.warning("No chats available. Please start a new chat.")
    selected_chat_id = None
else:
    selected_chat_id = all_chats[selected_chat_index][0]

if st.sidebar.button("🆕 Start New Chat"):
    selected_chat_id = create_new_chat()
    st.rerun()  # Rerun to refresh the chat list and select the new chat

if selected_chat_id is None:
    st.warning("Please start a new chat or select one from the sidebar.")
    st.stop()

# --- LOAD CHAT HISTORY ---
messages = get_messages(selected_chat_id)
for role, content in messages:
    with st.chat_message(role):
        st.markdown(content)

# --- CHAT INPUT AND RESPONSE ---
user_input = st.chat_input("Type your message...")
if user_input:
    # Show user input
    st.chat_message("user").markdown(user_input)
    save_message(selected_chat_id, "user", user_input)

    # Send request to backend
    with st.spinner("Thinking..."):
        response = requests.post(
            "https://jumarubea-logbook-ai-gen.hf.space/api/ai-generate",
            json={
                "system_message": system_prompt(),
                "user_prompt": user_input
            }
        )

    if response.status_code == 200:
        reply = response.json().get("generated_text", "No response")
        st.chat_message("assistant").markdown(reply)
        save_message(selected_chat_id, "assistant", reply)
    else:
        st.error("API call failed.")
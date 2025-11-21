import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv

# 1. Load API Key
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
    except (FileNotFoundError, KeyError):
        st.error("API Key not found! Please set it in your .env or Streamlit Secrets.")
        st.stop()

genai.configure(api_key=api_key)

# 2. Configure Page Settings
st.set_page_config(page_title="Gemini Chat", page_icon="🤖")
st.title("🤖 Gemini 2.5 Chatbot")

# 3. Initialize Chat Session (This runs once when the app starts)
if "chat_session" not in st.session_state:
    model = genai.GenerativeModel("gemini-2.5-flash")
    st.session_state.chat_session = model.start_chat(history=[])

# 4. Display Chat History
# We loop through the history to show previous messages on the screen
for message in st.session_state.chat_session.history:
    role = "user" if message.role == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

# 5. Handle User Input
user_input = st.chat_input("Type your message here...")

if user_input:
    # Display the user's message immediately
    st.chat_message("user").markdown(user_input)

    # Send to Gemini and get response
    try:
        response = st.session_state.chat_session.send_message(user_input)
        
        # Display Gemini's response
        with st.chat_message("assistant"):
            st.markdown(response.text)
            
    except Exception as e:
        st.error(f"An error occurred: {e}")
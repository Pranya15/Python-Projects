import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/api/analyze"

st.set_page_config(page_title="Cricket AI Analyst", page_icon="🏏", layout="wide")

st.title("🏏 Cricket AI Analyst Assistant")
st.markdown("Ask me anything about cricket! My multi-agent system will research, analyze stats, write a report, and fact-check it before showing you the result.")
st.markdown("*(Note: Please ensure you have added your API keys to the `.env` file and started the FastAPI server.)*")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Enter your cricket question (e.g. 'Compare Virat Kohli and Steve Smith's Test centuries')"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.spinner("Agents are researching, analyzing, drafting, and fact-checking..."):
        try:
            response = requests.post(API_URL, json={"query": prompt})
            if response.status_code == 200:
                result = response.json().get("result", "No result returned.")
            else:
                result = f"Error from backend: {response.status_code} - {response.text}"
        except Exception as e:
            result = f"Failed to connect to backend. Is FastAPI running? Error: {str(e)}"
    
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(result)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": result})

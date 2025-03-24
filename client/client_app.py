"""
# Llama 2 Chatbot Client

## How to run:
1. Make sure the API server is running: `uvicorn app:app --reload` (in the apis directory)
2. Run this client: `streamlit run client_app.py`
"""

import streamlit as st
import requests
import json

# Configure the page
st.set_page_config(
    page_title="Llama 2 Chatbot Client",
    page_icon="🦙",
    layout="centered"
)

# App title and description
st.title("🦙 Llama 2 Chatbot Client")
st.subheader("Connecting to the LangServe API")

# API URL configuration
API_URL = st.sidebar.text_input("API URL", value="http://localhost:8000/llama/invoke")
st.sidebar.info("Make sure the API server is running before using this client.")

# Initialize chat session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Function to call the API
def call_chatbot_api(prompt):
    try:
        payload = {
            "input": prompt
        }
        response = requests.post(API_URL, json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            return f"Error: API returned status code {response.status_code}"
    except Exception as e:
        return f"Error connecting to API: {str(e)}"

# Chat input
if prompt := st.chat_input("Ask me anything..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get response from API
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        with st.spinner("Calling API..."):
            response = call_chatbot_api(prompt)
            
            # Check if response is a string (error) or a dict (success)
            if isinstance(response, str):
                message_placeholder.error(response)
                assistant_response = response
            else:
                # Extract the response from the API output
                assistant_response = response
                message_placeholder.markdown(assistant_response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})

# Instructions footer
st.markdown("---")
st.markdown("### How to run this client")
st.code("streamlit run client_app.py")
st.markdown("Make sure the API server is running: `uvicorn app:app --reload` (in the apis directory)") 
"""
Streamlit client application for interacting with the Llama 2 chatbot API.

This module provides a Streamlit web interface to interact with the Llama 2 chatbot API.
"""

import streamlit as st
import requests
import logging
import json
from typing import Dict, Any, Union, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ChatbotClient:
    """
    Client for interacting with the Llama 2 chatbot API.
    """
    
    def __init__(self, api_url: str = "http://localhost:8000/llama/invoke"):
        """
        Initialize the chatbot client.
        
        Args:
            api_url: The URL of the chatbot API. Defaults to "http://localhost:8000/llama/invoke".
        """
        self.api_url = api_url
    
    def send_message(self, message: str) -> Union[str, Dict[str, Any]]:
        """
        Send a message to the chatbot API and get a response.
        
        Args:
            message: The message to send to the chatbot.
            
        Returns:
            The response from the chatbot API, either as a string (error) or as a dictionary (success).
        """
        try:
            payload = {"input": message}
            response = requests.post(self.api_url, json=payload)
            
            if response.status_code == 200:
                return response.json()
            else:
                return f"Error: API returned status code {response.status_code}"
        except Exception as e:
            logger.error(f"Error connecting to API: {str(e)}")
            return f"Error connecting to API: {str(e)}"

def initialize_page():
    """Initialize Streamlit page configuration."""
    st.set_page_config(
        page_title="Llama 2 Chatbot Client",
        page_icon="🦙",
        layout="centered"
    )
    
    # App title and description
    st.title("🦙 Llama 2 Chatbot Client")
    st.subheader("Connecting to the LangServe API")

def initialize_session_state():
    """Initialize the session state for chat history and API connection."""
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Initialize API URL
    if "api_url" not in st.session_state:
        st.session_state.api_url = "http://localhost:8000/llama/invoke"
    
    # Initialize client
    if "client" not in st.session_state or st.session_state.api_url != st.session_state.current_api_url:
        st.session_state.current_api_url = st.session_state.api_url
        st.session_state.client = ChatbotClient(st.session_state.api_url)
        logger.info(f"ChatbotClient initialized with API URL: {st.session_state.api_url}")

def setup_sidebar():
    """Set up the sidebar with API configuration."""
    with st.sidebar:
        st.header("API Configuration")
        api_url = st.text_input("API URL", value=st.session_state.api_url)
        
        if api_url != st.session_state.api_url:
            st.session_state.api_url = api_url
            initialize_session_state()
        
        st.info("Make sure the API server is running before using this client.")
        
        if st.button("Test Connection"):
            try:
                test_url = "/".join(st.session_state.api_url.split("/")[:-1])
                response = requests.get(test_url)
                if response.status_code == 200:
                    st.success("API connection successful!")
                else:
                    st.error(f"API connection failed with status code {response.status_code}")
            except Exception as e:
                st.error(f"API connection failed: {str(e)}")

def display_chat_history():
    """Display the chat history."""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def handle_user_input():
    """Handle user input and generate responses."""
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
                response = st.session_state.client.send_message(prompt)
                
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

def display_instructions():
    """Display usage instructions."""
    st.markdown("---")
    st.markdown("### How to run this client")
    st.code("python -m src.modules.client.streamlit_client")
    st.markdown("Make sure the API server is running: `python -m src.modules.api.api_server`")

def main():
    """Main function to run the Streamlit client."""
    initialize_page()
    initialize_session_state()
    setup_sidebar()
    display_chat_history()
    handle_user_input()
    display_instructions()

if __name__ == "__main__":
    main() 
"""
Streamlit application for direct interaction with the Llama 2 model.

This module provides a Streamlit web interface to interact with the Llama 2 model.
"""

import streamlit as st
import logging
import subprocess
import sys
import os
from src.config.environment_config import load_environment

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_environment()

def check_ollama_installed():
    """Check if Ollama is installed and available in PATH."""
    try:
        if sys.platform.startswith('win'):
            # Windows
            result = subprocess.run(['where', 'ollama'], 
                                   stdout=subprocess.PIPE, 
                                   stderr=subprocess.PIPE,
                                   text=True,
                                   check=False)
        else:
            # Linux/Mac
            result = subprocess.run(['which', 'ollama'], 
                                   stdout=subprocess.PIPE, 
                                   stderr=subprocess.PIPE,
                                   text=True,
                                   check=False)
        
        return result.returncode == 0
    except Exception as e:
        logger.error(f"Error checking Ollama installation: {str(e)}")
        return False

def initialize_page():
    """Initialize Streamlit page configuration."""
    st.set_page_config(
        page_title="Llama 2 Chatbot",
        page_icon="🦙",
        layout="centered"
    )
    
    # App title and description
    st.title("🦙 Llama 2 Chatbot")
    st.subheader("A simple chatbot using Langchain and Ollama")

def initialize_session_state():
    """Initialize the session state for chat history."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "llm_service" not in st.session_state:
        # Check if Ollama is installed
        if check_ollama_installed():
            try:
                from src.modules.llm.ollama_service import OllamaService
                st.session_state.llm_service = OllamaService()
                st.session_state.using_ollama = True
                logger.info("OllamaService initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize OllamaService: {str(e)}")
                st.error(f"Failed to initialize Ollama. Falling back to alternative model: {str(e)}")
                initialize_fallback_service()
        else:
            st.warning("⚠️ Ollama is not installed or not in your PATH. Falling back to an alternative model.")
            initialize_fallback_service()

def initialize_fallback_service():
    """Initialize a fallback service when Ollama is not available."""
    try:
        from src.modules.llm.huggingface_service import HuggingFaceService
        st.session_state.llm_service = HuggingFaceService()
        st.session_state.using_ollama = False
        logger.info("HuggingFaceService initialized as fallback")
        
        # Add installation instructions
        with st.expander("💡 How to install Ollama"):
            st.markdown("""
            ### Installing Ollama for better performance
            
            Ollama allows you to run powerful language models locally on your machine.
            
            1. Download Ollama from the [official website](https://ollama.ai/download)
            2. Install the application
            3. After installation, run this command in your terminal: `ollama run llama2`
            4. Restart this application
            
            If you're on Windows, you can run our setup script: `.\setup_windows.ps1`
            """)
    except Exception as e:
        logger.error(f"Failed to initialize fallback service: {str(e)}")
        st.error(f"Failed to initialize any language model service: {str(e)}")

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
        
        # Generate and display response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            
            # Generate response
            with st.spinner("Thinking..."):
                try:
                    if "llm_service" in st.session_state:
                        response = st.session_state.llm_service.generate_response(prompt)
                        message_placeholder.markdown(response)
                        
                        # Add assistant response to chat history
                        st.session_state.messages.append({"role": "assistant", "content": response})
                    else:
                        error_msg = "No language model service available. Please check the logs."
                        message_placeholder.error(error_msg)
                        logger.error(error_msg)
                        st.session_state.messages.append({"role": "assistant", "content": error_msg})
                except Exception as e:
                    error_msg = f"Error generating response: {str(e)}"
                    message_placeholder.error(error_msg)
                    logger.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})

def display_instructions():
    """Display usage instructions."""
    st.markdown("---")
    
    # Display different instructions based on which service is being used
    if st.session_state.get("using_ollama", False):
        st.markdown("### How to run this chatbot")
        st.code("python -m src.modules.llm.streamlit_app")
        st.markdown("Make sure Ollama is running with Llama 2 loaded (`ollama run llama2`)")
    else:
        st.markdown("### Using fallback model")
        st.markdown("You're currently using a smaller fallback model. For better results, install Ollama.")
        st.code("python -m src.modules.llm.streamlit_app")

def main():
    """Main function to run the Streamlit app."""
    initialize_page()
    initialize_session_state()
    display_chat_history()
    handle_user_input()
    display_instructions()

if __name__ == "__main__":
    main() 
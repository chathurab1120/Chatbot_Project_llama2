"""
# Llama 2 Chatbot with Langchain and Ollama

## Setup Instructions:
1. Download and install Ollama from the official website: https://ollama.ai/
2. Install and run the Llama 2 model using the command: `ollama run llama2`
3. Install the required dependencies: `pip install -r requirements.txt`
4. Run this Streamlit app: `streamlit run local_llama.py`
"""

import os
import streamlit as st
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms.ollama import Ollama
from langchain.schema.output_parser import StrOutputParser
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set page configuration
st.set_page_config(
    page_title="Llama 2 Chatbot",
    page_icon="🦙",
    layout="centered"
)

# App title and description
st.title("🦙 Llama 2 Chatbot")
st.subheader("A simple chatbot using Langchain and Ollama")

# Initialize chat model
@st.cache_resource
def get_llm():
    return Ollama(model="llama2")

# Initialize chat session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask me anything..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Create a Langchain chat template
    chat_template = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful, friendly AI assistant. Be concise and clear in your responses."),
        ("human", "{input}")
    ])
    
    # Build the chat chain
    llm = get_llm()
    chain = chat_template | llm | StrOutputParser()
    
    # Process the response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        # Generate response
        with st.spinner("Thinking..."):
            response = chain.invoke({"input": prompt})
            message_placeholder.markdown(response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

# Instructions footer
st.markdown("---")
st.markdown("### How to run this chatbot")
st.code("streamlit run local_llama.py")
st.markdown("Make sure Ollama is running with Llama 2 loaded (`ollama run llama2`)") 
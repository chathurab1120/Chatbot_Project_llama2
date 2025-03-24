import streamlit as st 
import subprocess 

# Set page configuration
st.set_page_config(
    page_title="LlamaChat AI Assistant",
    page_icon="🦙",
    layout="centered"
)

# Custom CSS for better appearance
st.markdown("""
<style>
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    .chat-header {
        text-align: center;
        margin-bottom: 30px;
    }
    .chat-header h1 {
        color: #FF4B4B;
        font-size: 2.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Attractive header with emoji
st.markdown("<div class='chat-header'><h1>🦙 LlamaChat AI Assistant</h1></div>", unsafe_allow_html=True)
st.markdown("*Powered by Llama 2 - Your local AI assistant*")
st.markdown("---")
 
if "messages" not in st.session_state: 
    st.session_state.messages = [] 
 
# Display chat messages 
for message in st.session_state.messages: 
    with st.chat_message(message["role"]): 
        st.markdown(message["content"]) 
 
# User input 
prompt = st.chat_input("Ask me anything...") 
if prompt: 
    # Add user message to chat history 
    st.session_state.messages.append({"role": "user", "content": prompt}) 
    # Display user message in chat message container 
    with st.chat_message("user"): 
        st.markdown(prompt) 
 
    # Display assistant response in chat message container 
    with st.chat_message("assistant"): 
        message_placeholder = st.empty() 
        message_placeholder.markdown("Thinking...") 
 
        try: 
            # Call Ollama directly 
            model = "tinyllama" 
            cmd = ["ollama", "run", model, prompt] 
            result = subprocess.run(cmd, capture_output=True, text=True) 
            response = result.stdout.strip() 
 
            # Update response 
            message_placeholder.markdown(response) 
            # Add assistant response to chat history 
            st.session_state.messages.append({"role": "assistant", "content": response}) 
        except Exception as e: 
            message_placeholder.markdown(f"Error: {str(e)}") 

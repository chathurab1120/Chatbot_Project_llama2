import streamlit as st 
import subprocess 
 
st.title("Minimal Ollama Chatbot") 
 
if "messages" not in st.session_state: 
    st.session_state.messages = [] 
 
# Display chat messages 
for message in st.session_state.messages: 
    with st.chat_message(message["role"]): 
        st.markdown(message["content"]) 
 
# User input 
prompt = st.chat_input("Message TinyLlama...") 
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

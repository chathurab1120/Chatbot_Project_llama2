@echo on
echo ========================================
echo LlamaChat AI Assistant - Launcher
echo ========================================
echo.

:: Direct path to Python
set PYTHON_CMD="C:\ProgramData\miniconda3\python.exe"
set MODEL_NAME=tinyllama

:: Create a permanent .env file
echo Creating .env file with TinyLlama configuration...
echo OLLAMA_MODEL=%MODEL_NAME% > .env
type .env

:: Create Streamlit config directory and theme file
echo.
echo Setting up dark mode theme...
mkdir .streamlit 2>nul
echo [theme] > .streamlit\config.toml
echo primaryColor = "#FF4B4B" >> .streamlit\config.toml
echo backgroundColor = "#0E1117" >> .streamlit\config.toml
echo secondaryBackgroundColor = "#262730" >> .streamlit\config.toml
echo textColor = "#FAFAFA" >> .streamlit\config.toml
echo font = "sans-serif" >> .streamlit\config.toml
echo base = "dark" >> .streamlit\config.toml

:: Check if Ollama is running without trying to start it
echo.
echo Checking if Ollama service is already running...
curl -s http://localhost:11434/api/tags >nul 2>&1
if %errorlevel% equ 0 (
    echo Great! Ollama is already running.
) else (
    echo WARNING: Ollama service doesn't seem to be running.
    echo Please open a Command Prompt and run 'ollama serve' before continuing.
    echo.
    echo Press any key when Ollama is running...
    pause >nul
)

:: Create a very simple chatbot that we know should work
echo.
echo Creating LlamaChat AI Assistant...
mkdir chatbot_simple 2>nul

:: Create the enhanced Ollama chatbot with dark mode
echo import streamlit as st > chatbot_simple\minimal_chat.py
echo import subprocess >> chatbot_simple\minimal_chat.py
echo. >> chatbot_simple\minimal_chat.py
echo # Set page configuration >> chatbot_simple\minimal_chat.py
echo st.set_page_config( >> chatbot_simple\minimal_chat.py
echo     page_title="LlamaChat AI Assistant", >> chatbot_simple\minimal_chat.py
echo     page_icon="🦙", >> chatbot_simple\minimal_chat.py
echo     layout="centered" >> chatbot_simple\minimal_chat.py
echo ) >> chatbot_simple\minimal_chat.py
echo. >> chatbot_simple\minimal_chat.py
echo # Custom CSS for better appearance >> chatbot_simple\minimal_chat.py
echo st.markdown(""" >> chatbot_simple\minimal_chat.py
echo ^<style^> >> chatbot_simple\minimal_chat.py
echo     .stApp { >> chatbot_simple\minimal_chat.py
echo         max-width: 1200px; >> chatbot_simple\minimal_chat.py
echo         margin: 0 auto; >> chatbot_simple\minimal_chat.py
echo     } >> chatbot_simple\minimal_chat.py
echo     .chat-header { >> chatbot_simple\minimal_chat.py
echo         text-align: center; >> chatbot_simple\minimal_chat.py
echo         margin-bottom: 30px; >> chatbot_simple\minimal_chat.py
echo     } >> chatbot_simple\minimal_chat.py
echo     .chat-header h1 { >> chatbot_simple\minimal_chat.py
echo         color: #FF4B4B; >> chatbot_simple\minimal_chat.py
echo         font-size: 2.5rem; >> chatbot_simple\minimal_chat.py
echo     } >> chatbot_simple\minimal_chat.py
echo ^</style^> >> chatbot_simple\minimal_chat.py
echo """, unsafe_allow_html=True) >> chatbot_simple\minimal_chat.py
echo. >> chatbot_simple\minimal_chat.py
echo # Attractive header with emoji >> chatbot_simple\minimal_chat.py
echo st.markdown("^<div class='chat-header'^>^<h1^>🦙 LlamaChat AI Assistant^</h1^>^</div^>", unsafe_allow_html=True) >> chatbot_simple\minimal_chat.py
echo st.markdown("*Powered by Llama 2 - Your local AI assistant*") >> chatbot_simple\minimal_chat.py
echo st.markdown("---") >> chatbot_simple\minimal_chat.py
echo. >> chatbot_simple\minimal_chat.py
echo if "messages" not in st.session_state: >> chatbot_simple\minimal_chat.py
echo     st.session_state.messages = [] >> chatbot_simple\minimal_chat.py
echo. >> chatbot_simple\minimal_chat.py
echo # Display chat messages >> chatbot_simple\minimal_chat.py
echo for message in st.session_state.messages: >> chatbot_simple\minimal_chat.py
echo     with st.chat_message(message["role"]): >> chatbot_simple\minimal_chat.py
echo         st.markdown(message["content"]) >> chatbot_simple\minimal_chat.py
echo. >> chatbot_simple\minimal_chat.py
echo # User input >> chatbot_simple\minimal_chat.py
echo prompt = st.chat_input("Ask me anything...") >> chatbot_simple\minimal_chat.py
echo if prompt: >> chatbot_simple\minimal_chat.py
echo     # Add user message to chat history >> chatbot_simple\minimal_chat.py
echo     st.session_state.messages.append({"role": "user", "content": prompt}) >> chatbot_simple\minimal_chat.py
echo     # Display user message in chat message container >> chatbot_simple\minimal_chat.py
echo     with st.chat_message("user"): >> chatbot_simple\minimal_chat.py
echo         st.markdown(prompt) >> chatbot_simple\minimal_chat.py
echo. >> chatbot_simple\minimal_chat.py
echo     # Display assistant response in chat message container >> chatbot_simple\minimal_chat.py
echo     with st.chat_message("assistant"): >> chatbot_simple\minimal_chat.py
echo         message_placeholder = st.empty() >> chatbot_simple\minimal_chat.py
echo         message_placeholder.markdown("Thinking...") >> chatbot_simple\minimal_chat.py
echo. >> chatbot_simple\minimal_chat.py
echo         try: >> chatbot_simple\minimal_chat.py
echo             # Call Ollama directly >> chatbot_simple\minimal_chat.py
echo             model = "tinyllama" >> chatbot_simple\minimal_chat.py
echo             cmd = ["ollama", "run", model, prompt] >> chatbot_simple\minimal_chat.py
echo             result = subprocess.run(cmd, capture_output=True, text=True) >> chatbot_simple\minimal_chat.py
echo             response = result.stdout.strip() >> chatbot_simple\minimal_chat.py
echo. >> chatbot_simple\minimal_chat.py
echo             # Update response >> chatbot_simple\minimal_chat.py
echo             message_placeholder.markdown(response) >> chatbot_simple\minimal_chat.py
echo             # Add assistant response to chat history >> chatbot_simple\minimal_chat.py
echo             st.session_state.messages.append({"role": "assistant", "content": response}) >> chatbot_simple\minimal_chat.py
echo         except Exception as e: >> chatbot_simple\minimal_chat.py
echo             message_placeholder.markdown(f"Error: {str(e)}") >> chatbot_simple\minimal_chat.py

echo.
echo ========================================
echo Starting LlamaChat AI Assistant and opening browser...
echo ========================================
echo.

:: Start the Streamlit server in a new window
start "LlamaChat AI Assistant" cmd /c "cd chatbot_simple && %PYTHON_CMD% -m streamlit run minimal_chat.py"

:: Wait for Streamlit to start
echo Waiting for Streamlit to initialize...
timeout /t 5 /nobreak > nul

:: Now explicitly open the browser
echo.
echo OPENING BROWSER NOW...
echo.
start "" "http://localhost:8501"

echo.
echo ========================================
echo Browser should now be opening to: http://localhost:8501
echo ========================================
echo.
echo If the browser doesn't open automatically, please:
echo 1. Manually open your browser
echo 2. Navigate to: http://localhost:8501
echo.
echo The Streamlit server is running in a separate window.
echo DO NOT close that window while using the chatbot.
echo.
echo Press any key to exit this window...
pause > nul 
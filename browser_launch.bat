@echo on
echo ========================================
echo Streamlit Chatbot with Browser Launch
echo ========================================
echo.

:: Direct path to Python
set PYTHON_CMD="C:\ProgramData\miniconda3\python.exe"
set MODEL_NAME=tinyllama

:: Create a permanent .env file
echo Creating .env file with TinyLlama configuration...
echo OLLAMA_MODEL=%MODEL_NAME% > .env
type .env

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
echo Creating a minimal chatbot...
mkdir chatbot_simple 2>nul

:: Create the simplest possible Ollama chatbot
echo import streamlit as st > chatbot_simple\minimal_chat.py
echo import subprocess >> chatbot_simple\minimal_chat.py
echo. >> chatbot_simple\minimal_chat.py
echo st.title("Minimal Ollama Chatbot") >> chatbot_simple\minimal_chat.py
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
echo prompt = st.chat_input("Message TinyLlama...") >> chatbot_simple\minimal_chat.py
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
echo Starting Streamlit and opening browser...
echo ========================================
echo.

:: Start the Streamlit server in a new window
start "Streamlit Server" cmd /c "cd chatbot_simple && %PYTHON_CMD% -m streamlit run minimal_chat.py"

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
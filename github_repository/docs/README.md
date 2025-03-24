# Llama 2 Chatbot with Langchain, FastAPI, and Streamlit

An end-to-end open-source chatbot project that leverages Langchain, local Llama 2 model via Ollama, FastAPI with LangServe, and Streamlit.

## Project Overview

This project demonstrates how to build a complete chatbot application using fully open-source components, without requiring any API keys or cloud services. The chatbot is powered by the Llama 2 model running locally through Ollama and is accessible through both a direct Streamlit interface and a FastAPI service.

## Technologies Used

- **Langchain**: Framework for developing applications powered by language models
- **Ollama**: Tool for running large language models locally
- **Llama 2**: Open-source large language model by Meta
- **FastAPI**: Modern, fast web framework for building APIs
- **LangServe**: Langchain's solution for deploying chains as REST APIs
- **Streamlit**: Framework for creating web applications for data science and machine learning

## Project Structure

```
├── chatbot_basic/          # Basic chatbot implementation
│   ├── local_llama.py      # Streamlit app for direct interaction
│   ├── .env                # Environment variables
│   └── requirements.txt    # Dependencies
│
├── apis/                   # API implementation
│   ├── app.py              # FastAPI app with LangServe
│   └── server_requirements.txt  # Server dependencies
│
├── client/                 # Client application
│   ├── client_app.py       # Streamlit app connecting to the API
│   └── client_requirements.txt  # Client dependencies
│
└── docs/                   # Documentation
    └── README.md           # This file
```

## Installation and Setup

### Prerequisites

1. Python 3.10 or higher
2. Ollama (for running Llama 2 locally)

### Step 1: Install Ollama and Llama 2

1. Download and install Ollama from the [official website](https://ollama.ai/).
2. Run the following command to download and install the Llama 2 model:

```bash
ollama run llama2
```

You can exit the Ollama CLI after it's loaded the model by typing `exit` or pressing Ctrl+C.

### Step 2: Set Up the Basic Chatbot

1. Navigate to the `chatbot_basic` directory:

```bash
cd chatbot_basic
```

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Run the chatbot:

```bash
streamlit run local_llama.py
```

This will open a browser window with the chatbot interface.

### Step 3: Set Up the API Server

1. Navigate to the `apis` directory:

```bash
cd apis
```

2. Install the required dependencies:

```bash
pip install -r server_requirements.txt
```

3. Start the API server:

```bash
uvicorn app:app --reload
```

4. Access the API documentation at `http://localhost:8000/docs`.

### Step 4: Set Up the Client Application

1. Navigate to the `client` directory:

```bash
cd client
```

2. Install the required dependencies:

```bash
pip install -r client_requirements.txt
```

3. Run the client application:

```bash
streamlit run client_app.py
```

This will open a browser window with the client interface.

## Usage

### Using the Basic Chatbot

1. Ensure Ollama is running with the Llama 2 model.
2. Run `streamlit run local_llama.py` in the `chatbot_basic` directory.
3. Type your messages in the input box at the bottom of the page.

### Using the API

The API exposes several endpoints:

- `GET /`: Status endpoint
- `POST /llama/invoke`: Main endpoint for chatbot interactions
- `GET /docs`: Interactive API documentation

Example API request:

```bash
curl -X 'POST' \
  'http://localhost:8000/llama/invoke' \
  -H 'Content-Type: application/json' \
  -d '{"input": "Tell me a joke about programming"}'
```

### Using the Client Application

1. Ensure the API server is running.
2. Run `streamlit run client_app.py` in the `client` directory.
3. Type your messages in the input box at the bottom of the page.

## Publishing to GitHub

To publish this project to GitHub:

1. Create a new repository on GitHub.
2. Initialize Git in the project directory:

```bash
git init
```

3. Add the files to the repository:

```bash
git add .
```

4. Commit the files:

```bash
git commit -m "Initial commit"
```

5. Link the local repository to the remote repository:

```bash
git remote add origin <YOUR_GITHUB_REPO_URL>
```

6. Push the files to GitHub:

```bash
git push -u origin main
```

## Future Enhancements

This project is designed to be modular for easy future upgrades, such as:

- Adding PDF reading capabilities
- Implementing vector databases for knowledge retrieval
- Supporting multiple LLM options
- Adding memory for longer conversations
- Enhancing the UI with additional features

## License

This project is available under the MIT License.

## Acknowledgements

- Langchain for the LLM application framework
- Meta for releasing Llama 2 as an open-source model
- Ollama for making local LLM deployment accessible 
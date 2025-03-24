# Llama 2 Chatbot with Langchain, FastAPI, and Streamlit

An end-to-end open-source chatbot project that leverages Langchain, local Llama 2 model via Ollama, FastAPI with LangServe, and Streamlit.

![LlamaChat AI Assistant](https://img.shields.io/badge/LlamaChat-AI%20Assistant-yellow)
![Langchain](https://img.shields.io/badge/Langchain-Framework-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-API-green)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-red)

## Project Overview

This project demonstrates how to build a complete chatbot application using fully open-source components, without requiring any API keys or cloud services. The LlamaChat AI Assistant is powered by the Llama 2 model running locally through Ollama and is accessible through both a direct Streamlit interface and a FastAPI service.

## Technologies Used

- **Langchain**: Framework for developing applications powered by language models
- **Ollama**: Tool for running large language models locally
- **Llama 2**: Open-source large language model by Meta
- **FastAPI**: Modern, fast web framework for building APIs
- **LangServe**: Langchain's solution for deploying chains as REST APIs
- **Streamlit**: Framework for creating web applications for data science and machine learning

## Quick Start

### Easy Start (Windows)
Simply run the batch file:
```
browser_launch.bat
```
This will check dependencies, create a minimal chatbot, start the Streamlit server, and automatically open your browser to the chatbot interface.

### Advanced Setup

1. Install Ollama and download the Llama 2 model:
   ```bash
   ollama run llama2
   ```
   *Don't have Ollama? Run `setup_windows.ps1` on Windows for an easy installation, or the chatbot will automatically fall back to a smaller HuggingFace model.*

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Streamlit app for direct LLM interaction:
   ```bash
   python -m src.modules.llm.streamlit_app
   ```

4. Run the API server:
   ```bash
   python -m src.modules.api.api_server
   ```

5. Run the Streamlit client that connects to the API:
   ```bash
   python -m src.modules.client.streamlit_client
   ```

## Project Structure

```
├── src/                     # Source code
│   ├── modules/             # Core modules
│   │   ├── llm/             # LLM integration with Ollama
│   │   │   ├── ollama_service.py  # Ollama service
│   │   │   └── streamlit_app.py   # Direct LLM interaction UI
│   │   ├── api/             # API implementation
│   │   │   ├── api_service.py     # FastAPI service
│   │   │   └── api_server.py      # API server runner
│   │   └── client/          # Client application
│   │       └── streamlit_client.py # Client connecting to API
│   └── config/              # Configuration
│       └── environment_config.py   # Environment variable management
│
├── tests/                   # Tests
│   ├── unit/                # Unit tests
│   │   ├── test_ollama_service.py  # Tests for Ollama service
│   │   ├── test_api_service.py     # Tests for API service
│   │   └── test_chatbot_client.py  # Tests for client
│   └── integration/         # Integration tests
│       └── test_api_integration.py # API integration tests
│
├── .env                     # Environment variables
└── requirements.txt         # Project dependencies
```

## Running Tests

Run the tests using pytest:

```bash
pytest
```

## Development Environments

The application supports three environments:
- **Development**: Local development environment
- **Test**: Testing environment
- **Production**: Production environment

## License

This project is available under the MIT License.

## Acknowledgements

- Langchain for the LLM application framework
- Meta for releasing Llama 2 as an open-source model
- Ollama for making local LLM deployment accessible

## Troubleshooting

### Common Issues

1. **"Ollama is not recognized as a command"**
   - Solution: The application will automatically fall back to a smaller model
   - For better results, install Ollama from [ollama.ai/download](https://ollama.ai/download)
   - On Windows, you can run `setup_windows.ps1` for assisted installation

2. **Slow Responses**
   - The first responses may be slow as the model loads into memory
   - Using the fallback model will be faster but may provide less accurate responses

3. **Out of Memory Errors with Ollama**
   - Llama 2 requires significant RAM. If you encounter memory issues, the application will fall back to a smaller model
   - Consider trying Ollama with a smaller model like `ollama run tinyllama` 
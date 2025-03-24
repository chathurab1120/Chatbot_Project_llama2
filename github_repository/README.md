# Llama 2 Chatbot with Langchain, FastAPI, and Streamlit

An end-to-end open-source chatbot project that leverages Langchain, local Llama 2 model via Ollama, FastAPI with LangServe, and Streamlit.

![Llama 2 Chatbot](https://img.shields.io/badge/Llama%202-Chatbot-yellow)
![Langchain](https://img.shields.io/badge/Langchain-Framework-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-API-green)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-red)

## Project Overview

This project demonstrates how to build a complete chatbot application using fully open-source components, without requiring any API keys or cloud services. The chatbot is powered by the Llama 2 model running locally through Ollama and is accessible through both a direct Streamlit interface and a FastAPI service.

## Technologies Used

- **Langchain**: Framework for developing applications powered by language models
- **Ollama**: Tool for running large language models locally
- **Llama 2**: Open-source large language model by Meta
- **FastAPI**: Modern, fast web framework for building APIs
- **LangServe**: Langchain's solution for deploying chains as REST APIs
- **Streamlit**: Framework for creating web applications for data science and machine learning

## Quick Start

1. Install Ollama and download the Llama 2 model:
   ```bash
   ollama run llama2
   ```

2. Set up and run the basic chatbot:
   ```bash
   cd chatbot_basic
   pip install -r requirements.txt
   streamlit run local_llama.py
   ```

3. Set up and run the API server:
   ```bash
   cd apis
   pip install -r server_requirements.txt
   uvicorn app:app --reload
   ```

4. Set up and run the client application:
   ```bash
   cd client
   pip install -r client_requirements.txt
   streamlit run client_app.py
   ```

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
    └── README.md           # Detailed documentation
```

## Detailed Documentation

For detailed documentation, installation instructions, and usage examples, please refer to the [docs/README.md](docs/README.md) file.

## License

This project is available under the MIT License.

## Acknowledgements

- Langchain for the LLM application framework
- Meta for releasing Llama 2 as an open-source model
- Ollama for making local LLM deployment accessible 
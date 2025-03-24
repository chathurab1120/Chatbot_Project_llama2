"""
Environment configuration for the Llama 2 Chatbot application.

This module handles loading and managing environment variables from .env files.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Constants
ENV_FILE_PATH = Path(__file__).parent.parent.parent / ".env"

# Environment variable names
LANGCHAIN_TRACING_V2 = "LANGCHAIN_TRACING_V2"
LANGCHAIN_PROJECT = "LANGCHAIN_PROJECT"

def load_environment():
    """
    Load environment variables from .env file.
    
    Returns:
        bool: True if environment variables were loaded successfully, False otherwise.
    """
    if ENV_FILE_PATH.exists():
        load_dotenv(dotenv_path=ENV_FILE_PATH)
        return True
    return False

def get_langchain_tracing():
    """
    Get the value of LANGCHAIN_TRACING_V2 environment variable.
    
    Returns:
        str: The value of LANGCHAIN_TRACING_V2 environment variable, or None if not set.
    """
    return os.getenv(LANGCHAIN_TRACING_V2)

def get_langchain_project():
    """
    Get the value of LANGCHAIN_PROJECT environment variable.
    
    Returns:
        str: The value of LANGCHAIN_PROJECT environment variable, or None if not set.
    """
    return os.getenv(LANGCHAIN_PROJECT)

# Load environment variables when module is imported
load_environment() 
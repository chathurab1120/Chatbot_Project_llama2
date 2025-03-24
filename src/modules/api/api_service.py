"""
API service for exposing the Llama 2 chatbot via FastAPI and LangServe.

This module provides a FastAPI application that exposes the Llama 2 chatbot as a REST API.
"""

import logging
import subprocess
import sys
from fastapi import FastAPI, HTTPException
from langserve import add_routes
from fastapi.middleware.cors import CORSMiddleware

# Configure logging
logger = logging.getLogger(__name__)

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

class ApiService:
    """
    Service for exposing the Llama 2 chatbot via FastAPI and LangServe.
    """
    
    def __init__(self):
        """Initialize the API service."""
        self.app = FastAPI(
            title="Llama 2 Chatbot API",
            description="API for a Llama 2 chatbot using LangChain and Ollama (or fallback service)",
            version="1.0.0",
        )
        self.using_ollama = False
        self._configure_cors()
        self._setup_routes()
    
    def _configure_cors(self):
        """Configure CORS middleware."""
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],  # Allows all origins
            allow_credentials=True,
            allow_methods=["*"],  # Allows all methods
            allow_headers=["*"],  # Allows all headers
        )
    
    def _setup_routes(self):
        """Set up API routes."""
        try:
            # Initialize LLM service based on availability
            if check_ollama_installed():
                try:
                    # Try to use Ollama
                    from src.modules.llm.ollama_service import OllamaService
                    llm_service = OllamaService()
                    self.using_ollama = True
                    logger.info("Using Ollama service for API")
                except Exception as e:
                    logger.warning(f"Failed to initialize Ollama service: {str(e)}. Falling back to alternative service.")
                    from src.modules.llm.huggingface_service import HuggingFaceService
                    llm_service = HuggingFaceService()
                    logger.info("Using HuggingFace service as fallback for API")
            else:
                # Use fallback service
                logger.warning("Ollama not found in PATH. Using fallback service.")
                from src.modules.llm.huggingface_service import HuggingFaceService
                llm_service = HuggingFaceService()
                logger.info("Using HuggingFace service as fallback for API")
            
            # Add LangServe routes for the chain
            add_routes(
                self.app,
                llm_service.get_chain(),
                path="/llama",
                enable_feedback=True,
            )
            
            # Add a health check endpoint
            @self.app.get("/")
            async def health_check():
                return {
                    "status": "online",
                    "using_ollama": self.using_ollama,
                    "message": "Llama 2 Chatbot API is running. Visit /docs for the API documentation."
                }
                
            logger.info("API routes set up successfully")
        except Exception as e:
            logger.error(f"Failed to set up API routes: {str(e)}")
            raise
    
    def get_app(self):
        """
        Get the FastAPI application.
        
        Returns:
            The FastAPI application instance.
        """
        return self.app 
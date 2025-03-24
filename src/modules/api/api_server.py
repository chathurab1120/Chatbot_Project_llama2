"""
API server runner for the Llama 2 chatbot.

This module provides a script to run the FastAPI server with Uvicorn.
"""

import logging
import uvicorn
from src.modules.api.api_service import ApiService
from src.config.environment_config import load_environment

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_environment()

def run_server(host: str = "0.0.0.0", port: int = 8000, reload: bool = True):
    """
    Run the FastAPI server with Uvicorn.
    
    Args:
        host: The host to bind to. Defaults to "0.0.0.0".
        port: The port to bind to. Defaults to 8000.
        reload: Whether to reload the server on code changes. Defaults to True.
    """
    try:
        # Initialize the API service
        api_service = ApiService()
        
        # Get the FastAPI app
        app = api_service.get_app()
        
        # Run the app with Uvicorn
        logger.info(f"Starting API server on {host}:{port}")
        uvicorn.run(app, host=host, port=port, reload=reload)
    except Exception as e:
        logger.error(f"Failed to start API server: {str(e)}")
        raise

def main():
    """Main function to run the API server."""
    run_server()

if __name__ == "__main__":
    main() 
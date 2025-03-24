"""
Integration tests for the API and LLM components.

This module contains integration tests between the API service and LLM service.
"""

import unittest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from src.modules.api.api_service import ApiService
from src.modules.llm.ollama_service import OllamaService

class TestApiLlmIntegration(unittest.TestCase):
    """
    Integration tests between the API service and LLM service.
    
    These tests verify that the API correctly interacts with the LLM service
    when processing requests.
    """
    
    @patch('src.modules.llm.ollama_service.Ollama')
    def test_llama_endpoint_integration(self, mock_ollama):
        """Test that the /llama endpoint correctly integrates with the LLM service."""
        # Arrange
        # Mock the Ollama LLM to return a specific response
        mock_llm = MagicMock()
        mock_chain = MagicMock()
        mock_chain.invoke.return_value = "This is a test response"
        
        # Set up the mocked OllamaService
        with patch('src.modules.api.api_service.OllamaService', autospec=True) as mock_service:
            mock_instance = mock_service.return_value
            mock_instance.get_chain.return_value = mock_chain
            
            # Create the API service
            api_service = ApiService()
            client = TestClient(api_service.get_app())
            
            # Act
            response = client.post(
                "/llama/invoke",
                json={"input": "Hello, world!"}
            )
            
            # Assert
            self.assertEqual(response.status_code, 200)
            # Confirm that results are present in the response
            # The exact format will depend on LangServe's response structure

    @patch('src.modules.api.api_service.OllamaService')
    def test_api_error_handling(self, mock_ollama_service):
        """Test that the API correctly handles errors from the LLM service."""
        # Arrange
        # Make the chain raise an exception when invoked
        mock_chain = MagicMock()
        mock_chain.invoke.side_effect = Exception("LLM error")
        
        mock_instance = mock_ollama_service.return_value
        mock_instance.get_chain.return_value = mock_chain
        
        # Create the API service
        api_service = ApiService()
        client = TestClient(api_service.get_app())
        
        # Act
        response = client.post(
            "/llama/invoke",
            json={"input": "This will cause an error"}
        )
        
        # Assert
        # LangServe typically returns 500 or similar for chain errors
        # This may need to be adjusted based on actual error handling
        self.assertGreaterEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main() 
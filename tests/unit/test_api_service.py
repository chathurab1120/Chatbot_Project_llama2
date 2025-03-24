"""
Unit tests for the API service.

This module contains tests for the ApiService class.
"""

import unittest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from src.modules.api.api_service import ApiService

class TestApiService(unittest.TestCase):
    """
    Test cases for the ApiService class.
    """
    
    @patch('src.modules.api.api_service.OllamaService')
    def test_initialization(self, mock_ollama_service):
        """Test that ApiService initializes correctly."""
        # Arrange
        mock_ollama_instance = MagicMock()
        mock_ollama_service.return_value = mock_ollama_instance
        mock_ollama_instance.get_chain.return_value = MagicMock()
        
        # Act
        service = ApiService()
        
        # Assert
        self.assertIsNotNone(service.app)
        mock_ollama_service.assert_called_once()
        mock_ollama_instance.get_chain.assert_called_once()
    
    @patch('src.modules.api.api_service.OllamaService')
    def test_get_app(self, mock_ollama_service):
        """Test that get_app returns the FastAPI app."""
        # Arrange
        mock_ollama_instance = MagicMock()
        mock_ollama_service.return_value = mock_ollama_instance
        mock_ollama_instance.get_chain.return_value = MagicMock()
        
        service = ApiService()
        
        # Act
        app = service.get_app()
        
        # Assert
        self.assertEqual(app, service.app)
    
    @patch('src.modules.api.api_service.OllamaService')
    def test_health_check_endpoint(self, mock_ollama_service):
        """Test that the health check endpoint returns the correct response."""
        # Arrange
        mock_ollama_instance = MagicMock()
        mock_ollama_service.return_value = mock_ollama_instance
        mock_ollama_instance.get_chain.return_value = MagicMock()
        
        service = ApiService()
        client = TestClient(service.get_app())
        
        # Act
        response = client.get("/")
        
        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "online")

if __name__ == '__main__':
    unittest.main() 
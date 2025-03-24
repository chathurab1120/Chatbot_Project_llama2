"""
Unit tests for the ChatbotClient class.

This module contains tests for the ChatbotClient class used in the Streamlit client.
"""

import unittest
from unittest.mock import patch, MagicMock
from src.modules.client.streamlit_client import ChatbotClient

class TestChatbotClient(unittest.TestCase):
    """
    Test cases for the ChatbotClient class.
    """
    
    def test_initialization(self):
        """Test that ChatbotClient initializes correctly with default and custom URLs."""
        # Test with default URL
        client = ChatbotClient()
        self.assertEqual(client.api_url, "http://localhost:8000/llama/invoke")
        
        # Test with custom URL
        custom_url = "http://example.com/api"
        client = ChatbotClient(custom_url)
        self.assertEqual(client.api_url, custom_url)
    
    @patch('src.modules.client.streamlit_client.requests.post')
    def test_send_message_success(self, mock_post):
        """Test that send_message correctly sends requests and handles successful responses."""
        # Arrange
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"output": "Test response"}
        mock_post.return_value = mock_response
        
        client = ChatbotClient()
        
        # Act
        response = client.send_message("Test message")
        
        # Assert
        mock_post.assert_called_once_with(
            "http://localhost:8000/llama/invoke", 
            json={"input": "Test message"}
        )
        self.assertEqual(response, {"output": "Test response"})
    
    @patch('src.modules.client.streamlit_client.requests.post')
    def test_send_message_error_status(self, mock_post):
        """Test that send_message correctly handles error status codes."""
        # Arrange
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_post.return_value = mock_response
        
        client = ChatbotClient()
        
        # Act
        response = client.send_message("Test message")
        
        # Assert
        self.assertTrue(isinstance(response, str))
        self.assertIn("Error", response)
        self.assertIn("500", response)
    
    @patch('src.modules.client.streamlit_client.requests.post')
    def test_send_message_exception(self, mock_post):
        """Test that send_message correctly handles exceptions during the API call."""
        # Arrange
        mock_post.side_effect = Exception("Connection error")
        
        client = ChatbotClient()
        
        # Act
        response = client.send_message("Test message")
        
        # Assert
        self.assertTrue(isinstance(response, str))
        self.assertIn("Error connecting to API", response)
        self.assertIn("Connection error", response)

if __name__ == '__main__':
    unittest.main() 
"""
Unit tests for the Ollama service.

This module contains tests for the OllamaService class.
"""

import unittest
from unittest.mock import patch, MagicMock
from src.modules.llm.ollama_service import OllamaService

class TestOllamaService(unittest.TestCase):
    """
    Test cases for the OllamaService class.
    """
    
    @patch('src.modules.llm.ollama_service.Ollama')
    @patch('src.modules.llm.ollama_service.ChatPromptTemplate')
    @patch('src.modules.llm.ollama_service.StrOutputParser')
    def test_initialization(self, mock_str_output_parser, mock_chat_template, mock_ollama):
        """Test that OllamaService initializes correctly."""
        # Arrange
        mock_ollama_instance = MagicMock()
        mock_ollama.return_value = mock_ollama_instance
        
        # Act
        service = OllamaService()
        
        # Assert
        mock_ollama.assert_called_once_with(model="llama2")
        self.assertEqual(service.model_name, "llama2")
        self.assertEqual(service.llm, mock_ollama_instance)
    
    @patch('src.modules.llm.ollama_service.Ollama')
    def test_generate_response(self, mock_ollama):
        """Test that generate_response calls the chain with the correct input."""
        # Arrange
        mock_chain = MagicMock()
        mock_chain.invoke.return_value = "Test response"
        
        mock_ollama_instance = MagicMock()
        mock_ollama.return_value = mock_ollama_instance
        
        service = OllamaService()
        service.chain = mock_chain
        
        # Act
        response = service.generate_response("Test input")
        
        # Assert
        mock_chain.invoke.assert_called_once_with({"input": "Test input"})
        self.assertEqual(response, "Test response")
    
    @patch('src.modules.llm.ollama_service.Ollama')
    def test_get_chain(self, mock_ollama):
        """Test that get_chain returns the chain."""
        # Arrange
        mock_chain = MagicMock()
        
        mock_ollama_instance = MagicMock()
        mock_ollama.return_value = mock_ollama_instance
        
        service = OllamaService()
        service.chain = mock_chain
        
        # Act
        chain = service.get_chain()
        
        # Assert
        self.assertEqual(chain, mock_chain)

if __name__ == '__main__':
    unittest.main() 
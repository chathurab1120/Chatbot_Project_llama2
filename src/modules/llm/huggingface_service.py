"""
HuggingFace service for interacting with open-source models.

This module provides a fallback when Ollama is not available.
"""

import logging
from typing import Dict, Any, Optional
import os

from langchain.prompts import ChatPromptTemplate
from langchain_community.llms import HuggingFaceEndpoint
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import Runnable

# Configure logging
logger = logging.getLogger(__name__)

class HuggingFaceService:
    """
    Service for interacting with HuggingFace models as a fallback for Ollama.
    """

    def __init__(self, model_name: str = "google/flan-t5-small"):
        """
        Initialize the HuggingFace service.
        
        Args:
            model_name: The name of the model to use. Defaults to "google/flan-t5-small".
        """
        self.model_name = model_name
        self.llm = None
        self.chain = None
        self._initialize_llm()
        self._build_chain()
    
    def _initialize_llm(self) -> None:
        """
        Initialize the HuggingFace model.
        """
        try:
            # Use smaller local model by default
            self.llm = HuggingFaceEndpoint(
                repo_id=self.model_name,
                temperature=0.7,
                max_length=512
            )
            logger.info(f"Successfully initialized HuggingFace with model {self.model_name}")
        except Exception as e:
            logger.error(f"Failed to initialize HuggingFace: {str(e)}")
            raise
    
    def _build_chain(self) -> None:
        """
        Build the language model chain with chat prompt template.
        """
        # Create a chat template
        chat_template = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful, friendly AI assistant. Be concise and clear in your responses."),
            ("human", "{input}")
        ])
        
        # Build the chain
        self.chain = chat_template | self.llm | StrOutputParser()
        
    def generate_response(self, user_input: str) -> str:
        """
        Generate a response to the user input.
        
        Args:
            user_input: The user's input message.
            
        Returns:
            The generated response from the model.
        """
        try:
            return self.chain.invoke({"input": user_input})
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return f"Sorry, I encountered an error: {str(e)}"
    
    def get_chain(self) -> Runnable:
        """
        Get the language model chain.
        
        Returns:
            The language model chain.
        """
        return self.chain 
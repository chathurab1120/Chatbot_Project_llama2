"""
# Llama 2 Chatbot API with FastAPI and LangServe

## How to run:
1. Make sure Ollama is running with Llama 2 model: `ollama run llama2`
2. Start the API server: `uvicorn app:app --reload`
3. Access the Swagger UI at http://localhost:8000/docs
"""

from fastapi import FastAPI
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms.ollama import Ollama
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import Runnable
from langserve import add_routes

# Create a FastAPI app
app = FastAPI(
    title="Chatbot API",
    description="API for a Llama 2 chatbot using LangChain and Ollama",
    version="1.0.0",
)

# Define the base chatbot chain
def create_chain() -> Runnable:
    # Initialize the Ollama model
    llm = Ollama(model="llama2")
    
    # Create a chat template
    chat_template = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful, friendly AI assistant. Be concise and clear in your responses."),
        ("human", "{input}")
    ])
    
    # Create and return the chain
    chain = chat_template | llm | StrOutputParser()
    return chain

# Add LangServe routes for the chain
add_routes(
    app,
    create_chain(),
    path="/llama",
    enable_feedback=True,
)

# Add a simple status endpoint
@app.get("/")
async def root():
    return {
        "status": "online",
        "message": "Llama 2 Chatbot API is running. Visit /docs for the API documentation."
    }

# Run the app with Uvicorn if executed directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True) 
from typing import List
from langchain.schema import Document
from mistralai.client import MistralClient
from app.core.config import settings
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self):
        if not settings.MISTRAL_API_KEY:
            raise ValueError("MISTRAL_API_KEY is not set in environment variables")
        
        logger.info("Initializing Mistral AI client with API key")
        self.client = MistralClient(api_key=settings.MISTRAL_API_KEY)
        self.model = "mistral-tiny"  # Using the free model as specified in docs

    def _create_prompt(self, query: str, context: List[Document]) -> str:
        """Create a prompt for the LLM using the query and context."""
        context_text = "\n\n".join([doc.page_content for doc in context])
        
        prompt = f"""You are a helpful AI assistant. Use the following context to answer the question.
        If the context doesn't contain relevant information, say so.

        Context:
        {context_text}

        Question: {query}

        Answer:"""
        return prompt

    def _detect_intent(self, query: str) -> bool:
        """Detect if the query requires knowledge base search."""
        # Simple intent detection
        greetings = {"hello", "hi", "hey", "good morning", "good afternoon", "good evening"}
        query_lower = query.lower().strip()
        
        # Check if it's a greeting
        if query_lower in greetings:
            return False
            
        # Check if it's a question
        if not any(query_lower.startswith(q) for q in ["what", "how", "why", "when", "where", "who", "which"]):
            return False
            
        return True

    def generate_response(self, query: str, context: List[Document]) -> str:
        """Generate a response using the Mistral AI model."""
        if not self._detect_intent(query):
            return "Hello! I'm here to help you with questions about the documents in our knowledge base. What would you like to know?"

        prompt = self._create_prompt(query, context)
        
        messages = [
            {"role": "user", "content": prompt}
        ]
        
        try:
            logger.info(f"Sending request to Mistral AI with model: {self.model}")
            chat_response = self.client.chat(
                model=self.model,
                messages=messages
            )
            return chat_response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error in Mistral AI API call: {str(e)}")
            if "401" in str(e):
                return "Error: Invalid or missing Mistral AI API key. Please check your .env file."
            return f"I apologize, but I encountered an error while processing your request: {str(e)}" 
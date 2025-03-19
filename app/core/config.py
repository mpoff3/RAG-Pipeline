from pydantic_settings import BaseSettings
from pathlib import Path
import os
from dotenv import load_dotenv
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class Settings(BaseSettings):
    # API Configuration
    API_V1_STR: str = "/api"
    PROJECT_NAME: str = "RAG Pipeline"
    
    # Mistral AI Configuration
    MISTRAL_API_KEY: str = os.getenv("MISTRAL_API_KEY", "")
    
    # File Storage
    UPLOAD_DIR: Path = Path("uploads")
    VECTOR_STORE_DIR: Path = Path("vector_store")
    
    # Document Processing
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    
    # Search Configuration
    SEMANTIC_WEIGHT: float = 0.7
    KEYWORD_WEIGHT: float = 0.3
    
    # Model Configuration
    EMBEDDING_MODEL: str = "mistral-embed"
    
    class Config:
        case_sensitive = True

settings = Settings()

# Log environment variable status
if not settings.MISTRAL_API_KEY:
    logger.warning("MISTRAL_API_KEY is not set in environment variables")
else:
    logger.info("MISTRAL_API_KEY is set")

# Create necessary directories
settings.UPLOAD_DIR.mkdir(exist_ok=True)
settings.VECTOR_STORE_DIR.mkdir(exist_ok=True) 
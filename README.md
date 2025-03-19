# RAG Pipeline with Mistral AI

This project implements a Retrieval-Augmented Generation (RAG) pipeline using FastAPI and Mistral AI for processing and querying PDF documents.

## System Architecture

### Components Overview

1. **Data Ingestion Layer**
   - PDF file upload endpoint
   - Text extraction and chunking using LangChain
   - Document storage in FAISS vector store

2. **Query Processing Layer**
   - Hybrid search combining semantic and keyword matching
   - Context retrieval from vector store
   - Query processing with Mistral AI

3. **Generation Layer**
   - Response generation using Mistral AI
   - Context-aware answer generation

## Setup Instructions

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file with your Mistral AI API key:
   ```
   MISTRAL_API_KEY=your_api_key_here
   ```
5. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```
6. Access the API interface:
   ```bash
   # Open your browser and navigate to:
   http://localhost:8000/docs  # Interactive Swagger UI for testing and debugging
   http://localhost:8000/redoc # Alternative documentation view (read-only)
   ```

## Using the API Interface

1. **Upload PDF Documents**:
   - Navigate to http://localhost:8000/docs
   - Find the `/api/ingest` endpoint and click "Try it out"
   - Click "Choose File" to select one or more PDF files
   - Click "Execute" to upload and process the documents
   - Wait for the confirmation message showing processed files

2. **Query the Documents**:
   - In the Swagger UI, find the `/api/query` endpoint
   - Click "Try it out"
   - Enter your question in the request body:
     ```json
     {
       "query": "What information can I find in the uploaded documents?"
     }
     ```
   - Click "Execute" to send your query
   - View the AI-generated response in the response body


## API Endpoints

### 1. Document Ingestion
- **Endpoint**: `/api/ingest`
- **Method**: POST
- **Content-Type**: multipart/form-data
- **Description**: Upload one or more PDF files for processing
- **Response**: List of processed document filenames

### 2. Query Processing
- **Endpoint**: `/api/query`
- **Method**: POST
- **Content-Type**: application/json
- **Description**: Process user queries and return AI-generated responses
- **Request Body**:
  ```json
  {
    "query": "Your question here"
  }
  ```

## Technical Details

### Dependencies
- FastAPI: Web framework
- Uvicorn: ASGI server
- PyPDF2: PDF processing
- LangChain: Document processing and chunking
- LangChain Community: Additional LangChain components
- LangChain HuggingFace: HuggingFace integration
- FAISS: Vector storage
- Mistral AI: Language model and embeddings
- Sentence Transformers: Text embeddings
- Python-dotenv: Environment variable management
- Pydantic: Data validation
- Pydantic Settings: Configuration management
- python-dotenv: Environment variable management

### Document Processing
- Chunk size: 1000 tokens
- Chunk overlap: 200 tokens
- Embedding model: Mistral AI embeddings

### Search Strategy
- Hybrid search combining:
  - Semantic similarity (70% weight)
  - Keyword matching (30% weight)
- Vector storage using FAISS
- Context-aware response generation

### Project Structure
```
app/
├── api/            # API endpoints and route handlers
│   └── endpoints.py
├── core/           # Core configuration and settings
│   └── config.py
├── services/       # Business logic and core functionality
│   ├── document_processor.py
│   ├── vector_store.py
│   └── llm_service.py
├── main.py         # Application entry point
├── uploads/        # Temporary storage for uploaded files
└── vector_store/   # Storage for vector embeddings
```

### Directory Purposes

- **api/**: Contains FastAPI route handlers and endpoint definitions
- **core/**: Houses application configuration and settings
- **services/**: Implements core business logic and functionality
- **uploads/**: Temporary storage for uploaded PDF files
- **vector_store/**: Persistent storage for FAISS vector embeddings

## Performance Considerations
- Document chunking optimized for Mistral AI's context window
- Efficient vector storage with FAISS
- CORS enabled for frontend integration
- Proper error handling and logging
- Temporary file cleanup after processing 
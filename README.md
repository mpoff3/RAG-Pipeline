# RAG Demo with Mistral AI

This project implements a Retrieval-Augmented Generation (RAG) pipeline using FastAPI, Next.js, and Mistral AI for processing and querying PDF documents.

## System Architecture

### Components Overview

1. **Frontend Layer**
   - Next.js web application
   - TypeScript for type safety
   - Tailwind CSS for styling
   - Real-time document upload and chat interface

2. **Data Ingestion Layer**
   - PDF file upload endpoint
   - Text extraction and chunking using LangChain
   - Document storage in FAISS vector store

3. **Query Processing Layer**
   - Context retrieval from vector store
      - Hybrid search combining semantic and keyword matching

4. **Generation Layer**
   - Response generation using Mistral AI
      - Context-aware answer generation

## Setup Instructions

### Backend Setup

1. Clone the repository
2. In the root directory, create a virtual environment:
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
5. Run the backend:
   ```bash
   uvicorn app.main:app --reload
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Create a `.env.local` file (use `.env.local.example` as a template):
   ```
   NEXT_PUBLIC_BACKEND_URL=http://localhost:8000/api
   ```
4. Run the development server:
   ```bash
   npm run dev
   ```
5. Access the web application:
   ```bash
   # Open your browser and navigate to:
   http://localhost:3000
   ```

## Technical Details

### Dependencies
- FastAPI: Web framework
- Uvicorn: ASGI server
- PyPDF2: PDF processing
- LangChain: Document processing and chunking
- FAISS: Vector storage
- Mistral AI: Language model
- Sentence Transformers: Text embeddings (all-MiniLM-L6-v2)
- Python-dotenv: Environment variable management
- Pydantic: Data validation

### Document Processing
- Chunk size: 1000 tokens
- Chunk overlap: 200 tokens
- Embedding model: Sentence Transformers (all-MiniLM-L6-v2)

### Search Strategy
- Hybrid search combining:
  - Semantic similarity (70% weight)
  - Keyword matching (30% weight)

### Project Structure
```
.
├── app/            # Backend application
│   ├── api/        # API endpoints and route handlers
│   ├── core/       # Core configuration and settings
│   ├── services/   # Core functionality
│   ├── main.py     # Application entry point
│   ├── uploads/    # Temporary storage for uploaded files
│   └── vector_store/ # Storage for vector embeddings
│
├── frontend/       # Next.js frontend application
│   ├── app/        # Next.js App Router
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   └── globals.css
│   └── components/ # React components
│       ├── Upload.tsx
│       ├── Chat.tsx
│       └── DocumentList.tsx
│
└── README.md       # Project documentation
```

## Performance Considerations
- Efficient vector storage with FAISS
- Proper error handling and logging
- Temporary file cleanup after processing 
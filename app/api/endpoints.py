from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from typing import List
from pathlib import Path
import shutil
from app.core.config import settings
from app.services.document_processor import DocumentProcessor
from app.services.vector_store import VectorStore
from app.services.llm_service import LLMService
from pydantic import BaseModel

router = APIRouter()
document_processor = DocumentProcessor()
vector_store = VectorStore()
llm_service = LLMService()

class QueryRequest(BaseModel):
    query: str

@router.post("/ingest")
async def ingest_documents(files: List[UploadFile] = File(...)):
    """Ingest PDF documents into the system."""
    try:
        processed_files = []
        
        for file in files:
            if not file.filename.endswith('.pdf'):
                raise HTTPException(status_code=400, detail="Only PDF files are supported")
            
            # Save file temporarily
            file_path = settings.UPLOAD_DIR / file.filename
            with file_path.open("wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            # Process the document
            chunks = document_processor.process_document(file_path)
            vector_store.add_documents(chunks)
            
            processed_files.append(file.filename)
            
            # Clean up
            file_path.unlink()
        
        return JSONResponse({
            "message": "Documents processed successfully",
            "processed_files": processed_files
        })
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/query")
async def query_documents(request: QueryRequest):
    """Process a query and return an AI-generated response."""
    try:
        # Perform hybrid search
        search_results = vector_store.hybrid_search(request.query)
        
        # Extract documents from search results
        context = [doc for doc, _ in search_results]
        
        # Generate response using LLM
        response = llm_service.generate_response(request.query, context)
        
        return JSONResponse({
            "response": response,
            "context_used": len(context)
        })
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 
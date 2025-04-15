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
import faiss
import numpy as np

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

@router.get("/documents")
async def list_documents():
    """Get a list of all processed documents."""
    try:
        # Get unique document filenames from the vector store
        document_names = set()
        for doc in vector_store.documents:
            if hasattr(doc, 'metadata') and 'filename' in doc.metadata:
                document_names.add(doc.metadata['filename'])
        
        return JSONResponse({
            "documents": sorted(list(document_names))
        })
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/documents/{filename}")
async def delete_document(filename: str):
    """Delete a document from the vector store."""
    try:
        # Find and remove documents with matching filename
        original_length = len(vector_store.documents)
        vector_store.documents = [
            doc for doc in vector_store.documents 
            if not (hasattr(doc, 'metadata') and 
                   'filename' in doc.metadata and 
                   doc.metadata['filename'] == filename)
        ]
        
        # If any documents were removed, rebuild the index
        if len(vector_store.documents) < original_length:
            # Rebuild the FAISS index
            if vector_store.documents:
                embeddings = vector_store.embeddings.embed_documents(
                    [doc.page_content for doc in vector_store.documents]
                )
                vector_store.index = faiss.IndexFlatL2(len(embeddings[0]))
                vector_store.index.add(np.array(embeddings).astype('float32'))
            else:
                vector_store.index = None
            
            # Save the updated store
            vector_store.save_store()
            
            return JSONResponse({
                "message": f"Document {filename} deleted successfully"
            })
        
        raise HTTPException(status_code=404, detail=f"Document {filename} not found")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 
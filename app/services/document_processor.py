from pathlib import Path
from typing import List, Dict
import PyPDF2
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from app.core.config import settings

class DocumentProcessor:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )

    def extract_text_from_pdf(self, file_path: Path) -> str:
        """Extract text from a PDF file."""
        text = ""
        with open(file_path, "rb") as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        return text

    def process_document(self, file_path: Path) -> List[Document]:
        """Process a document and return chunks."""
        # Extract text from PDF
        text = self.extract_text_from_pdf(file_path)
        
        # Create a Document object
        doc = Document(
            page_content=text,
            metadata={
                "source": str(file_path),
                "filename": file_path.name
            }
        )
        
        # Split into chunks
        chunks = self.text_splitter.split_documents([doc])
        
        # Add chunk-specific metadata
        for i, chunk in enumerate(chunks):
            chunk.metadata["chunk_index"] = i
            chunk.metadata["total_chunks"] = len(chunks)
        
        return chunks

    def process_files(self, files: List[Path]) -> Dict[str, List[Document]]:
        """Process multiple files and return a dictionary of processed chunks."""
        processed_docs = {}
        for file_path in files:
            try:
                chunks = self.process_document(file_path)
                processed_docs[str(file_path)] = chunks
            except Exception as e:
                print(f"Error processing {file_path}: {str(e)}")
                continue
        return processed_docs 
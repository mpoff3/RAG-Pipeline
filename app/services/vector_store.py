from pathlib import Path
from typing import List, Dict, Tuple
import faiss
import numpy as np
from langchain.schema import Document
from langchain_huggingface import HuggingFaceEmbeddings
from app.core.config import settings
import pickle
import os

class VectorStore:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        self.index = None
        self.documents: List[Document] = []
        self.load_store()

    def load_store(self):
        """Load the vector store from disk if it exists."""
        index_path = settings.VECTOR_STORE_DIR / "faiss.index"
        docs_path = settings.VECTOR_STORE_DIR / "documents.pkl"
        
        if index_path.exists() and docs_path.exists():
            self.index = faiss.read_index(str(index_path))
            with open(docs_path, "rb") as f:
                self.documents = pickle.load(f)

    def save_store(self):
        """Save the vector store to disk."""
        if self.index is not None:
            faiss.write_index(self.index, str(settings.VECTOR_STORE_DIR / "faiss.index"))
            with open(settings.VECTOR_STORE_DIR / "documents.pkl", "wb") as f:
                pickle.dump(self.documents, f)

    def add_documents(self, documents: List[Document]):
        """Add documents to the vector store."""
        if not documents:
            return

        # Get embeddings for new documents
        embeddings = self.embeddings.embed_documents([doc.page_content for doc in documents])
        
        # Initialize or update FAISS index
        if self.index is None:
            self.index = faiss.IndexFlatL2(len(embeddings[0]))
        
        # Add embeddings to the index
        self.index.add(np.array(embeddings).astype('float32'))
        
        # Add documents to the list
        self.documents.extend(documents)
        
        # Save the updated store
        self.save_store()

    def similarity_search(
        self,
        query: str,
        k: int = 4,
        score_threshold: float = 0.5
    ) -> List[Tuple[Document, float]]:
        """Perform similarity search."""
        if not self.index or not self.documents:
            return []

        # Get query embedding
        query_embedding = self.embeddings.embed_query(query)
        
        # Search in FAISS
        distances, indices = self.index.search(
            np.array([query_embedding]).astype('float32'),
            k
        )
        
        # Convert distances to similarities (1 - normalized distance)
        max_distance = np.max(distances)
        similarities = 1 - (distances / max_distance)
        
        # Filter and combine results
        results = []
        for idx, similarity in zip(indices[0], similarities[0]):
            if similarity >= score_threshold:
                results.append((self.documents[idx], float(similarity)))
        
        return results

    def keyword_search(
        self,
        query: str,
        k: int = 4
    ) -> List[Tuple[Document, float]]:
        """Perform keyword-based search."""
        if not self.documents:
            return []

        # Simple keyword matching
        query_terms = set(query.lower().split())
        results = []
        
        for doc in self.documents:
            content_terms = set(doc.page_content.lower().split())
            overlap = len(query_terms.intersection(content_terms))
            if overlap > 0:
                # Simple scoring based on term overlap
                score = overlap / len(query_terms)
                results.append((doc, score))
        
        # Sort by score and take top k
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:k]

    def hybrid_search(
        self,
        query: str,
        k: int = 4
    ) -> List[Tuple[Document, float]]:
        """Perform hybrid search combining semantic and keyword search."""
        semantic_results = self.similarity_search(query, k=k)
        keyword_results = self.keyword_search(query, k=k)
        
        # Create a dictionary to store combined scores using document content as key
        combined_results = {}
        
        # Add semantic search results
        for doc, score in semantic_results:
            combined_results[doc.page_content] = (doc, score * settings.SEMANTIC_WEIGHT)
        
        # Add keyword search results
        for doc, score in keyword_results:
            if doc.page_content in combined_results:
                # Update existing document's score
                existing_doc, existing_score = combined_results[doc.page_content]
                combined_results[doc.page_content] = (existing_doc, existing_score + score * settings.KEYWORD_WEIGHT)
            else:
                # Add new document
                combined_results[doc.page_content] = (doc, score * settings.KEYWORD_WEIGHT)
        
        # Convert dictionary values to list and sort by score
        sorted_results = sorted(
            combined_results.values(),
            key=lambda x: x[1],
            reverse=True
        )
        
        return sorted_results[:k] 
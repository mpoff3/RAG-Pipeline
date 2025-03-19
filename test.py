import pickle
import faiss
import numpy as np

# Load the documents
# with open('vector_store/documents.pkl', 'rb') as f:
#     documents = pickle.load(f)

# Print each document's content and metadata
# for doc in documents:
#     print("Content:", doc.page_content)
#     print("Metadata:", doc.metadata)
#     print("---")

# Load the index
index = faiss.read_index('vector_store/faiss.index')

# Get number of vectors and dimensions
print(f"Number of vectors: {index.ntotal}")
print(f"Vector dimension: {index.d}")  # Should be 384 for all-MiniLM-L6-v2

# If you want to see the actual vectors:
if isinstance(index, faiss.IndexFlat):
    vectors = index.reconstruct_n(0, index.ntotal)
    print("First vector:", vectors[0])  # Shows the 384 dimensions of the first vector
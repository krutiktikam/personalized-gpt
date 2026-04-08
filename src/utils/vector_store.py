import chromadb
from chromadb.utils import embedding_functions
import os
from pathlib import Path
from src.utils.logger import logger

class VectorStore:
    def __init__(self, db_path="data/vector_db"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(path=self.db_path)
        
        # Use a lightweight embedding function
        self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )
        
        # Create or get collections
        self.doc_collection = self.client.get_or_create_collection(
            name="aura_docs",
            embedding_function=self.embedding_function
        )
        self.snippet_collection = self.client.get_or_create_collection(
            name="user_snippets",
            embedding_function=self.embedding_function
        )
        
        logger.info("✅ VectorStore initialized with ChromaDB.")

    def add_document(self, content, metadata=None, doc_id=None):
        """Adds a document (e.g., from docs/) to the collection."""
        if not doc_id:
            import hashlib
            doc_id = hashlib.mdsafe_hex(content.encode()).hexdigest()
            
        self.doc_collection.upsert(
            documents=[content],
            metadatas=[metadata] if metadata else [{}],
            ids=[doc_id]
        )

    def add_snippet(self, content, metadata=None, snippet_id=None):
        """Adds a code snippet or project idea to the user collection."""
        if not snippet_id:
            import uuid
            snippet_id = str(uuid.uuid4())
            
        self.snippet_collection.upsert(
            documents=[content],
            metadatas=[metadata] if metadata else [{}],
            ids=[snippet_id]
        )

    def query_docs(self, query_text, n_results=3):
        """Searches the documentation for relevant context."""
        results = self.doc_collection.query(
            query_texts=[query_text],
            n_results=n_results
        )
        return results['documents'][0] if results['documents'] else []

    def query_snippets(self, query_text, n_results=3):
        """Searches user snippets for relevant past ideas."""
        results = self.snippet_collection.query(
            query_texts=[query_text],
            n_results=n_results
        )
        return results['documents'][0] if results['documents'] else []

# Singleton instance
vector_store = VectorStore()

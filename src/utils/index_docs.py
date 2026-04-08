import os
from pathlib import Path
import sys

# Add project root to sys.path
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.utils.vector_store import vector_store
from src.utils.logger import logger

def index_docs():
    docs_dir = project_root / "docs"
    if not docs_dir.exists():
        logger.error(f"Docs directory {docs_dir} not found.")
        return

    logger.info(f"📚 Indexing documentation from {docs_dir}...")
    
    for doc_file in docs_dir.glob("*.md"):
        with open(doc_file, "r", encoding="utf-8") as f:
            content = f.read()
            # Simple chunking by paragraph for now
            chunks = [c.strip() for c in content.split("\n\n") if len(c.strip()) > 50]
            
            for i, chunk in enumerate(chunks):
                doc_id = f"{doc_file.name}_chunk_{i}"
                vector_store.add_document(
                    content=chunk,
                    metadata={"source": doc_file.name},
                    doc_id=doc_id
                )
                
    # Also index text files
    for doc_file in docs_dir.glob("*.txt"):
        with open(doc_file, "r", encoding="utf-8") as f:
            content = f.read()
            chunks = [c.strip() for c in content.split("\n\n") if len(c.strip()) > 50]
            for i, chunk in enumerate(chunks):
                doc_id = f"{doc_file.name}_chunk_{i}"
                vector_store.add_document(
                    content=chunk,
                    metadata={"source": doc_file.name},
                    doc_id=doc_id
                )

    logger.info("✅ Documentation indexing complete.")

if __name__ == "__main__":
    index_docs()

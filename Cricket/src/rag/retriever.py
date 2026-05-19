import os
from langchain_community.vectorstores import Chroma
import sys
from pathlib import Path

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from src.rag.embeddings import get_embeddings_model

CHROMA_PATH = "vector_db"
DATA_PATH = "data"


def has_local_documents() -> bool:
    data_dir = Path(DATA_PATH)
    if not data_dir.exists():
        return False
    return any(path.is_file() and path.suffix.lower() == ".pdf" for path in data_dir.rglob("*.pdf"))

def get_vector_db():
    """Get the Chroma vector database instance."""
    embeddings = get_embeddings_model()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)
    return db

def get_retriever():
    """Get the retriever interface for the vector DB."""
    db = get_vector_db()
    # Return a retriever that fetches the top 4 most similar chunks
    return db.as_retriever(search_kwargs={"k": 4})

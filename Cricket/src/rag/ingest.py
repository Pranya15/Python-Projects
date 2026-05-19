import os
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
import sys

# Add the root project directory to the path so we can import from src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from src.rag.embeddings import get_embeddings_model

CHROMA_PATH = "vector_db"
DATA_PATH = "data"

def load_documents():
    """Load PDFs from the data directory."""
    print(f"Loading PDFs from {DATA_PATH}...")
    # Make sure data directory exists
    if not os.path.exists(DATA_PATH):
        os.makedirs(DATA_PATH)
        
    loader = PyPDFDirectoryLoader(DATA_PATH)
    docs = loader.load()
    print(f"Loaded {len(docs)} pages.")
    return docs

def split_text(documents):
    """Split documents into smaller chunks."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Split {len(documents)} pages into {len(chunks)} chunks.")
    return chunks

def save_to_chroma(chunks):
    """Save chunks to the local Chroma database."""
    print("Saving chunks to ChromaDB...")
    embeddings = get_embeddings_model()
    
    db = Chroma.from_documents(
        chunks, embeddings, persist_directory=CHROMA_PATH
    )
    print(f"Saved {len(chunks)} chunks to {CHROMA_PATH}.")

def ingest_data():
    """Main ingestion pipeline."""
    docs = load_documents()
    if not docs:
        print("No documents found to ingest. Place PDFs in the 'data' folder.")
        return
    chunks = split_text(docs)
    save_to_chroma(chunks)

if __name__ == "__main__":
    ingest_data()

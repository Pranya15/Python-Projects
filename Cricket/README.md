# Cricket AI Analyst Assistant

A full-stack, multi-agent AI assistant built with LangGraph, LangChain, FastAPI, and Streamlit.

## Features
- **RAG Pipeline**: Ingests cricket PDFs and stores them in ChromaDB.
- **Multi-Agent Workflow**: Includes Research, Stats, Writer, and Fact-Checker agents working in a sequence.
- **FastAPI Backend**: Exposes the LangGraph workflow as a scalable REST API.
- **Streamlit Frontend**: A beautiful chat interface for the user.

## Setup Instructions

### 1. Environment Variables
Open the `.env` file and replace the placeholder text with your actual API key for either Google Gemini or OpenAI.

### 2. Ingest Data (RAG Pipeline)
1. Place any cricket-related PDF files inside the `data/` folder (e.g., cricket rulebook, Wikipedia exports, player stats).
2. Activate your virtual environment and run the ingest script to create the local ChromaDB vector database:
```bash
.\venv\Scripts\activate
python src/rag/ingest.py
```

### 3. Start the Backend (FastAPI)
In a new terminal window:
```bash
.\venv\Scripts\activate
python src/backend/main.py
```
The API will run on `http://127.0.0.1:8000`.

### 4. Start the Frontend (Streamlit)
In another new terminal window:
```bash
.\venv\Scripts\activate
streamlit run src/frontend/app.py
```
This will automatically open the beautiful chat UI in your browser!

## Mentorship Notes
This project covers:
1. Document chunking & embeddings (LangChain)
2. Vector search (ChromaDB)
3. Node/Edge routing and State management (LangGraph)
4. Client/Server separation (FastAPI + Streamlit)

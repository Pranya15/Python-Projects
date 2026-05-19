import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_openai import OpenAIEmbeddings

load_dotenv()

PLACEHOLDER_GOOGLE_KEY = "your_google_gemini_api_key_here"
PLACEHOLDER_OPENAI_KEY = "your_openai_api_key_here"
GOOGLE_EMBEDDING_MODEL = "models/gemini-embedding-001"


def _has_configured_key(env_var: str, placeholder: str) -> bool:
    value = os.getenv(env_var, "").strip()
    return bool(value) and value != placeholder

def get_embeddings_model():
    """Returns the configured embeddings model."""
    # Check for Google API key first, default to OpenAI if not present
    if _has_configured_key("GOOGLE_API_KEY", PLACEHOLDER_GOOGLE_KEY):
        return GoogleGenerativeAIEmbeddings(model=GOOGLE_EMBEDDING_MODEL)
    elif _has_configured_key("OPENAI_API_KEY", PLACEHOLDER_OPENAI_KEY):
        return OpenAIEmbeddings(model="text-embedding-3-small")
    else:
        # Fallback to Google if no key is properly configured yet (will error later if actually used without key)
        print("WARNING: No valid API key found in .env. Using Google Embeddings as default placeholder.")
        return GoogleGenerativeAIEmbeddings(model=GOOGLE_EMBEDDING_MODEL)

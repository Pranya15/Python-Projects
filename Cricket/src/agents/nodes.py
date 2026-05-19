import os
import sys
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI

from src.agents.state import AgentState
from src.rag.retriever import get_retriever, has_local_documents

load_dotenv()

PLACEHOLDER_GOOGLE_KEY = "your_google_gemini_api_key_here"
PLACEHOLDER_OPENAI_KEY = "your_openai_api_key_here"
GOOGLE_CHAT_MODEL = "gemini-2.0-flash"
USER_FACING_PROVIDER_ERROR = (
    "The AI provider request failed. Check your configured API key or billing for the active "
    "provider. If OpenAI quota is exhausted, add a valid Google Gemini key or restore OpenAI quota."
)


def _has_configured_key(env_var: str, placeholder: str) -> bool:
    value = os.getenv(env_var, "").strip()
    return bool(value) and value != placeholder


def get_llms():
    llms = []
    if _has_configured_key("GOOGLE_API_KEY", PLACEHOLDER_GOOGLE_KEY):
        llms.append(("google", ChatGoogleGenerativeAI(model=GOOGLE_CHAT_MODEL, temperature=0)))
    if _has_configured_key("OPENAI_API_KEY", PLACEHOLDER_OPENAI_KEY):
        llms.append(("openai", ChatOpenAI(model="gpt-3.5-turbo", temperature=0)))
    if llms:
        return llms
    return [("google", ChatGoogleGenerativeAI(model=GOOGLE_CHAT_MODEL, temperature=0))]


def _friendly_error_message(last_error: Exception) -> str:
    error_text = str(last_error)
    lowered = error_text.lower()
    if "resource_exhausted" in lowered or "quota exceeded" in lowered:
        return (
            "Google Gemini quota is exhausted for this project. Wait for quota reset or enable billing "
            "for the Google key in `.env`."
        )
    if "insufficient_quota" in lowered or "exceeded your current quota" in lowered:
        return (
            "OpenAI quota is exhausted for this project. Update billing for the OpenAI key in `.env` "
            "or use a valid Google Gemini key instead."
        )
    if "api key" in lowered or "authentication" in lowered or "permission" in lowered:
        return "The configured API key was rejected by the provider. Update the key in `.env`."
    return USER_FACING_PROVIDER_ERROR


def _summarize_provider_errors(provider_errors) -> str:
    normalized = []
    for provider_name, exc in provider_errors:
        message = _friendly_error_message(exc)
        normalized.append(f"{provider_name}: {message}")

    if not normalized:
        return USER_FACING_PROVIDER_ERROR

    unique_messages = []
    for item in normalized:
        if item not in unique_messages:
            unique_messages.append(item)

    if len(unique_messages) == 1:
        return unique_messages[0]

    return "All configured AI providers failed. " + " | ".join(unique_messages)


def invoke_with_fallback(messages):
    provider_errors = []
    for provider_name, llm in get_llms():
        try:
            response = llm.invoke(messages)
            return response.content
        except Exception as exc:
            print(f"LLM provider '{provider_name}' failed: {exc}", file=sys.stderr)
            provider_errors.append((provider_name, exc))
    if not provider_errors:
        raise RuntimeError(USER_FACING_PROVIDER_ERROR)
    raise RuntimeError(_summarize_provider_errors(provider_errors)) from provider_errors[-1][1]


def _trim_context(text: str, limit: int = 1800) -> str:
    cleaned = (text or "").strip()
    if len(cleaned) <= limit:
        return cleaned
    return cleaned[:limit].rsplit(" ", 1)[0] + "..."


def build_retrieval_only_response(query: str, research: str, stats: str = "") -> str:
    parts = [
        "AI drafting is temporarily unavailable because the configured model providers are out of quota.",
        f"Query: {query}",
    ]

    research_excerpt = _trim_context(research) if research else ""
    stats_excerpt = _trim_context(stats, 600) if stats and "Error:" not in stats else ""

    if research_excerpt:
        parts.append("Retrieved context:")
        parts.append(research_excerpt)
    else:
        parts.append("No retrieved cricket context was available in the local vector database.")

    if stats_excerpt:
        parts.append("Available stats context:")
        parts.append(stats_excerpt)

    parts.append("Restore quota or replace the API keys in `.env` to re-enable full drafted answers.")
    return "\n\n".join(parts)

def research_agent(state: AgentState) -> dict:
    """Retrieves general cricket knowledge from the vector DB."""
    query = state["query"]
    print("---RESEARCH AGENT---")
    
    try:
        if not has_local_documents():
            context = (
                "No local cricket documents are available. Add one or more PDF files to the `data/` "
                "folder and run `python src/rag/ingest.py` to enable retrieval."
            )
            return {"research_context": context, "current_agent": "research_agent"}
        retriever = get_retriever()
        docs = retriever.invoke(query)
        context = "\\n\\n".join([d.page_content for d in docs])
        if not context:
            context = "No relevant context found in the documents."
    except Exception as e:
        context = f"Error retrieving documents: {str(e)}"
        
    return {"research_context": context, "current_agent": "research_agent"}

def stats_agent(state: AgentState) -> dict:
    """Focuses on numerical data or uses a specific stats tool if available."""
    query = state["query"]
    print("---STATS AGENT---")
    
    system_msg = SystemMessage(content="You are a Cricket Statistician. Extract and highlight any numerical stats related to the query from your knowledge or state that stats are unavailable.")
    human_msg = HumanMessage(content=query)
    
    try:
        content = invoke_with_fallback([system_msg, human_msg])
    except Exception as e:
        content = f"Stats Error: {str(e)}"
        
    return {"stats_data": content, "current_agent": "stats_agent"}

def writer_agent(state: AgentState) -> dict:
    """Drafts the final response combining research and stats."""
    query = state["query"]
    research = state.get("research_context", "")
    stats = state.get("stats_data", "")
    print("---WRITER AGENT---")
    
    system_msg = SystemMessage(content=(
        "You are an expert Cricket Writer. Draft a comprehensive and engaging response "
        "to the user's query using the provided research context and statistical data. "
        "Make it read like a professional sports article or analysis."
    ))
    
    prompt = f"User Query: {query}\\n\\nResearch Context:\\n{research}\\n\\nStats Data:\\n{stats}"
    human_msg = HumanMessage(content=prompt)
    
    try:
        content = invoke_with_fallback([system_msg, human_msg])
    except Exception as e:
        content = build_retrieval_only_response(query, research, stats)
        
    return {"draft": content, "current_agent": "writer_agent"}

def fact_checker_agent(state: AgentState) -> dict:
    """Reviews the draft for factual accuracy against the context."""
    draft = state.get("draft", "")
    research = state.get("research_context", "")
    print("---FACT CHECKER AGENT---")
    
    system_msg = SystemMessage(content=(
        "You are a meticulous Cricket Fact Checker. Review the drafted article against "
        "the retrieved research context. Fix any hallucinations or inaccuracies. "
        "If the draft is accurate, return the draft as is. If not, return the corrected draft."
    ))
    
    prompt = f"Original Research Context:\\n{research}\\n\\nDrafted Article:\\n{draft}\\n\\nPlease output the final verified article."
    human_msg = HumanMessage(content=prompt)
    
    try:
        content = invoke_with_fallback([system_msg, human_msg])
    except Exception as e:
        content = draft  # Fallback to draft if error
        
    return {"final_output": content, "current_agent": "fact_checker_agent"}

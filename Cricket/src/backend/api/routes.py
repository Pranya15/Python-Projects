from fastapi import APIRouter, HTTPException
from src.backend.models.schemas import QueryRequest, QueryResponse
from src.agents.graph import run_workflow
import traceback

router = APIRouter()

@router.post("/analyze", response_model=QueryResponse)
async def analyze_query(request: QueryRequest):
    try:
        # Run the LangGraph workflow
        result = run_workflow(request.query)
        return QueryResponse(result=result)
    except Exception as e:
        print(f"Error in workflow: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))

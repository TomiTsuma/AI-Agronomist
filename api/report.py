from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.gemini_interface import executive_summary, recommendations_summary
from services.plots import createPlots
from services.retrieval import retrieve_context
from services.context_manager import search_context
from db.connection import get_data

router = APIRouter()

class ReportInput(BaseModel):
    results: list
    guides: list
    recommendations: list

class ReportOutput(BaseModel):
    executive_summary: str
    recommendations_summary: str
    visualizations: list

@router.post("/", response_model=ReportOutput)
async def ask(request: ReportInput):

    # try:
    executive_summary_result = executive_summary(request.results, request.guides)
    recommendations_summary_result = recommendations_summary(request.results, request.guides, request.recommendations)
    visualization_result = createPlots(request.results, request.guides)
    return ReportOutput(executive_summary=executive_summary_result,  recommendations_summary=recommendations_summary_result, visualizations=visualization_result)
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=str(e))
    


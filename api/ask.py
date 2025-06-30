from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.gemini_interface import ask_gemini
from services.retrieval import retrieve_context
from services.context_manager import search_context
from db.connection import get_data

router = APIRouter()

class AskRequest(BaseModel):
    client_name: str
    farm_name: str
    query: str

class AskResponse(BaseModel):
    response: dict
    context_used: list

@router.post("/", response_model=AskResponse)
async def ask(request: AskRequest):

    try:
        context_chunks = retrieve_context(request.client_name, request.farm_name)
        response = ask_gemini(request.query, context_chunks)
        return AskResponse(response=response, context_used=context_chunks)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/search-and-ask", response_model=AskResponse)
async def ask(request: AskRequest):

    try:
        sql_query = search_context(request.query)
        sql_query = sql_query.get("sql_query", None)
        if sql_query == None:
            raise HTTPException(status_code=500, detail="Could not generate a query use the /ask endpoint instead")
        context_chunks = get_data(sql_query).to_dict("records")
        response = ask_gemini(request.query, context_chunks)
        return AskResponse(response=response, context_used=context_chunks)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

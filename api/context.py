from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.context_manager import search_context

router = APIRouter()

class ContextEntry(BaseModel):
    query: str

@router.get("/search")
async def search(query: str):
    # try:
    results = search_context(query)
    return results
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=str(e))

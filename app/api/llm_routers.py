from fastapi import APIRouter, Query, HTTPException
from app.services.llm_services import generate_llm_output

router = APIRouter()

@router.get("/output/")
def get_llm_output(query: str = Query(..., description="Enter the query"),
                   results: str = Query(..., description="All the results")):
    try:
        return generate_llm_output(query, results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

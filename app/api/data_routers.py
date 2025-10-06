from fastapi import APIRouter, Query, HTTPException
import os
from app.services.pdf_services import process_folder
from app.services.weaviate_services import client

router = APIRouter()

@router.get("/list-preview/", response_model=str)
def list_pdf_preview(path: str = Query(..., description="Path to the local folder")):
    if not os.path.isdir(path):
        raise HTTPException(status_code=400, detail="Invalid folder path")
    try:
        return process_folder(path, client)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/search/")
def search_documents(query: str = Query(..., description="Your search query"), limit: int = 3):
    from app.services.weaviate_services import search_in_weaviate
    try:
        return search_in_weaviate(query, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

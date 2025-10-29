from fastapi import APIRouter, Query, HTTPException
import os
from app.services.data_services import process_folder
from app.services.weaviate_services import client, clear_weaviate_data
from app.services.article_services import process_article

router = APIRouter()
 
@router.get("/list-preview/", response_model=str)
def list_pdf_preview(path: str = Query(..., description="Path to the local folder")):
    if not os.path.isdir(path):
        raise HTTPException(status_code=400, detail="Invalid folder path")
    try:
        return process_folder(path, client)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# @router.get("/search/")
# def search_documents(query: str = Query(..., description="Your search query"), limit: int = 3):
#     from app.services.weaviate_services import search_in_weaviate
#     try:
#         return search_in_weaviate(query, limit)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


@router.get("/article-preview/", response_model=str)
def list_article_preview(url: str = Query(..., description="URL of the article to process")):
    """
    Accept an article URL and process it: extract content, split into chunks, embed, store in Weaviate.
    """
    if not url.startswith("http"):
        raise HTTPException(status_code=400, detail="Invalid URL provided.")

    try:
        return process_article(url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.delete("/clear-weaviate/", response_model=str)
def clear_weaviate():
    """
    Clear all data from the Weaviate 'Document' collection.
    """
    return clear_weaviate_data(client)

from fastapi import APIRouter, Query, HTTPException, File, UploadFile, Form
from typing import List, Optional, Union
from app.services.data_services import process_folder
from app.services.weaviate_services import client, clear_weaviate_data
from app.services.article_services import process_article
from app.services.process_files import handle_multiple_files
 
router = APIRouter()
 
@router.post("/list-preview/", response_model=str)
async def list_pdf_preview(files: Optional[Union[List[UploadFile], List[str]]] = None, urls: Optional[List[str]] = Form(None)):
    """
    Accept multiple local file paths and process them.
    Logic handled inside app/services/process_files.py
    """
    try:

        file_result = ""
        url_result = ""

        try:
            file_result = handle_multiple_files(files)
        except Exception:
            file_result = "No files uploaded."

        try:
            for url in urls:
                if not url.startswith("http"):
                    raise HTTPException(status_code=400, detail="Invalid URL provided.")

                clean_urls = []
                for url in urls:
                    clean_urls.extend([u.strip() for u in url.split(",") if u.strip()])

                for url in clean_urls:
                    if not url.startswith("http"):
                        raise HTTPException(status_code=400, detail=f"Invalid URL provided: {url}")
                    try:
                        res = process_article(url)
                        url_result += f"\n{res}"
                    except Exception as e:
                        url_result += f"\nError processing {url}: {str(e)}"

        except Exception:
            url_result = "No URLs provided."

        return f"url result is {url_result} and file result is {file_result}"
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
async def list_article_preview(url: str = Query(..., description="URL of the article to process")):
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
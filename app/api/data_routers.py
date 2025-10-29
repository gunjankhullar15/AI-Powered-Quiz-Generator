from fastapi import APIRouter, Query, HTTPException, UploadFile, File
import os
import shutil
from app.services.data_services import process_folder, clear_weaviate_data
from app.services.weaviate_services import client

router = APIRouter()

TEMP_DIR = "temp_files"

# Ensure temp folder exists
os.makedirs(TEMP_DIR, exist_ok=True)


@router.post("/upload-files/", response_model=str)
async def upload_files(files: list[UploadFile] = File(...)):
    """
    Accept multiple uploaded files (PDF, DOCX, TXT, PPTX),
    store them temporarily in the temp_files folder,
    and process them afterward.
    """
    if not files:
        raise HTTPException(status_code=400, detail="No files uploaded.")

    try:
        # 🧹 Clear old temp files before saving new ones
        for old_file in os.listdir(TEMP_DIR):
            old_path = os.path.join(TEMP_DIR, old_file)
            if os.path.isfile(old_path):
                os.remove(old_path)

        saved_paths = []

        # Save uploaded files to temp folder
        for file in files:
            temp_path = os.path.join(TEMP_DIR, file.filename)
            with open(temp_path, "wb") as f:
                shutil.copyfileobj(file.file, f)
            saved_paths.append(temp_path)

        # ✅ Now process the saved files from the temp folder
        result = process_folder(TEMP_DIR, client)

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during file upload: {e}")


@router.get("/search/")
def search_documents(query: str = Query(..., description="Your search query"), limit: int = 3):
    from app.services.weaviate_services import search_in_weaviate
    try:
        return search_in_weaviate(query, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

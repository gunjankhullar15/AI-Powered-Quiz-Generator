import os
import shutil
from fastapi import HTTPException, UploadFile
from app.services.data_services import process_folder
from app.services.weaviate_services import client


def handle_multiple_files(files: list[UploadFile]):
    """
    Accept multiple local file paths, copy them to a temp folder,
    then process them using existing process_folder logic.
    """

    temp_dir = os.path.join("app", "temp_uploads")
    os.makedirs(temp_dir, exist_ok=True)

    # Clear temp folder before using
    for f in os.listdir(temp_dir):
        file_path = os.path.join(temp_dir, f)
        try:
            os.remove(file_path)
        except Exception:
            pass

     # Save uploaded files into temp folder
    for file in files:
        file_path = os.path.join(temp_dir, file.filename)
        try:
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to save file {file.filename}: {e}")

    try:
        # Process all files from the temp folder
        result = process_folder(temp_dir, client)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Optional cleanup (delete temp files after processing)
        for f in os.listdir(temp_dir):
            try:
                os.remove(os.path.join(temp_dir, f))
            except Exception:
                pass
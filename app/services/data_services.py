import os
from app.utils.splitter import get_splitter
from app.services.weaviate_services import transformer


def process_folder(folder_path, client):
    """
    Process all supported files (PDF, DOCX, TXT, PPTX)
    from a local folder (e.g., temp_files/).
    """
    supported_ext = [".pdf", ".docx", ".txt", ".pptx"]
    doc_collection = client.collections.get("Document")

    # List all valid files from the folder
    all_files = [
        os.path.join(folder_path, f)
        for f in os.listdir(folder_path)
        if os.path.splitext(f)[1].lower() in supported_ext
    ]

    if not all_files:
        return "No supported files (PDF, DOCX, TXT, PPTX) found in folder."

    for file_path in all_files:
        filename = os.path.basename(file_path)
        ext = os.path.splitext(filename)[1].lower()
        print(f"📄 Processing file: {filename}")

        # Read file bytes
        with open(file_path, "rb") as f:
            file_bytes = f.read()

        # Split into chunks
        chunks = get_splitter(file_bytes, file_type=ext)
        text_chunks = [chunk.page_content for chunk in chunks]

        # Generate embeddings
        embeddings = transformer.encode(text_chunks).tolist()

        # Store in Weaviate
        for chunk, vector in zip(text_chunks, embeddings):
            doc_collection.data.insert(
                properties={"content": chunk, "filename": filename},
                vector=vector
            )

    return f"✅ Successfully processed {len(all_files)} files from '{folder_path}'."


def clear_weaviate_data(client):
    doc_collection = client.collections.get("Document")

    # 🧹 Delete all existing data before inserting new data
    try:
        
        # Delete all objects that have the 'content' property (i.e., all your docs)
        
        client.collections.delete("Document")
        print("🧹 Cleared all objects from the 'Document' class.")
    except Exception as e:
        print(f"⚠️ Failed to delete old data: {e}")
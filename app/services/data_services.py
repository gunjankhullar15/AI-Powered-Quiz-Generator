import os
from app.utils.splitter import get_splitter
from app.services.weaviate_services import transformer
from app.logs.logger_config import setup_logger
 
logger = setup_logger(__name__)
 
 
 
def process_folder(path: str, client):
    """Process PDF, DOCX, TXT, and PPTX files using LangChain loaders + splitters and store in Weaviate."""
    supported_ext = [".pdf", ".docx", ".txt", ".pptx"]
    files = os.listdir(path)
    supported_files = [f for f in files if os.path.splitext(f)[1].lower() in supported_ext]
 
    if not supported_files:
        logger.warning("No supported files found.")
        return "No supported files (PDF, DOCX, TXT, PPTX) found in the folder."
 
    doc_collection = client.collections.get("Document")
 
    for file in supported_files:
        file_path = os.path.join(path, file)
        ext = os.path.splitext(file)[1].lower()
 
        print(f"📄 Processing file: {file}")
 
        # Get document chunks using appropriate loader and splitter
        chunks = get_splitter(file_path)
 
        # Extract text content for embedding
        text_chunks = [chunk.page_content for chunk in chunks]
 
        # Generate embeddings
        logger.info(f"Generating embeddings for {len(text_chunks)} chunks...")
        embeddings = transformer.encode(text_chunks).tolist()
 
        # Store in Weaviate
        for chunk, vector in zip(text_chunks, embeddings):
            doc_collection.data.insert(
                properties={"content": chunk, "filename": file},
                vector=vector
            )
 
    return f"✅ Successfully processed {len(supported_files)} files (PDF, DOCX, TXT, PPTX)."
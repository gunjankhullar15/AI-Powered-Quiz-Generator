from langchain_community.document_loaders import (
    PyPDFLoader,
    Docx2txtLoader,
    TextLoader,
    UnstructuredPowerPointLoader,
)
from langchain.text_splitter import CharacterTextSplitter
from langchain.schema import Document
from app.logs.logger_config import setup_logger
logger = setup_logger(__name__)
 
def get_splitter(file_path: str = None, text: str = None):
    """Return documents and splitter based on file type — word-based chunks."""

    if text:
        logger.info("Splitting raw article text for article ingestion...")
        splitter = CharacterTextSplitter(
            separator=" ",       # Split by spaces (word-based)
            chunk_size=200,      # Number of words per chunk
            chunk_overlap=20,    # Overlap between chunks
            length_function=lambda t: len(t.split()),  # Count words
        )
        docs = [Document(page_content=text)]
        chunks = splitter.split_documents(docs)
        logger.info(f"Split article text into {len(chunks)} chunks")
        return chunks


    logger.info(f"Loading document: {file_path}")

    if file_path.endswith(".pdf"):
        loader = PyPDFLoader(file_path)
    elif file_path.endswith(".docx"):
        loader = Docx2txtLoader(file_path)
    elif file_path.endswith(".txt"):
        loader = TextLoader(file_path)
    elif file_path.endswith(".pptx"):
        loader = UnstructuredPowerPointLoader(file_path)
    else:
        logger.error(f"Unsupported file type: {file_path}")
        raise ValueError(f"Unsupported file type: {file_path}")
 
    # Load the document
    docs = loader.load()
    logger.info(f"Loaded {len(docs)} documents from {file_path}")
 
    # Splitter based on words (not characters)
    splitter = CharacterTextSplitter(
        separator=" ",       # Split by spaces (word-based)
        chunk_size=200,      # Number of words per chunk
        chunk_overlap=20,    # Overlap between chunks
        length_function=lambda text: len(text.split()),  # Count words
    )
 
    # Split into chunks
    chunks = splitter.split_documents(docs)
    logger.info(f"Split into {len(chunks)} chunks for {file_path}")
    return chunks

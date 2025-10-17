# from langchain_community.document_loaders import (
#     PyPDFLoader,
#     Docx2txtLoader,
#     TextLoader,
#     UnstructuredPowerPointLoader,
# )
# from langchain.text_splitter import CharacterTextSplitter
 
 
# def get_splitter(file_path: str):
#     """Return documents and splitter based on file type — word-based chunks."""
#     if file_path.endswith(".pdf"):
#         loader = PyPDFLoader(file_path)
#     elif file_path.endswith(".docx"):
#         loader = Docx2txtLoader(file_path)
#     elif file_path.endswith(".txt"):
#         loader = TextLoader(file_path)
#     elif file_path.endswith(".pptx"):
#         loader = UnstructuredPowerPointLoader(file_path)
#     else:
#         raise ValueError(f"Unsupported file type: {file_path}")
 
#     # Load the document
#     docs = loader.load()
 
#     # Splitter based on words (not characters)
#     splitter = CharacterTextSplitter(
#         separator=" ",       # Split by spaces (word-based)
#         chunk_size=200,      # Number of words per chunk
#         chunk_overlap=20,    # Overlap between chunks
#         length_function=lambda text: len(text.split()),  # Count words
#     )
 
#     # Split into chunks
#     chunks = splitter.split_documents(docs)
#     return chunks


from langchain_community.document_loaders import (
    PyPDFLoader,
    Docx2txtLoader,
    TextLoader,
    UnstructuredPowerPointLoader,
)
from langchain.text_splitter import CharacterTextSplitter
from langchain.schema import Document


def get_splitter(file_path: str = None, text: str = None):
    """
    Return chunks based on either a file path or raw text input.
    - If file_path is provided: loads and splits document file.
    - If text is provided: directly splits text content.
    """

    splitter = CharacterTextSplitter(
        separator=" ",        # Split by spaces (word-based)
        chunk_size=200,       # Number of words per chunk
        chunk_overlap=20,     # Overlap between chunks
        length_function=lambda text: len(text.split()),  # Count words
    )

    if file_path:
        # Handle document files
        if file_path.endswith(".pdf"):
            loader = PyPDFLoader(file_path)
        elif file_path.endswith(".docx"):
            loader = Docx2txtLoader(file_path)
        elif file_path.endswith(".txt"):
            loader = TextLoader(file_path)
        elif file_path.endswith(".pptx"):
            loader = UnstructuredPowerPointLoader(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_path}")

        docs = loader.load()
        chunks = splitter.split_documents(docs)

    elif text:
        # Handle raw text input (e.g., articles)
        doc = Document(page_content=text)
        chunks = splitter.split_documents([doc])

    else:
        raise ValueError("Either file_path or text must be provided.")

    return chunks

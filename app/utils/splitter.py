from langchain.text_splitter import RecursiveCharacterTextSplitter

def get_splitter():
    return RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

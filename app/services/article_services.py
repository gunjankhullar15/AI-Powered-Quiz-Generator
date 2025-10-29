import requests
from bs4 import BeautifulSoup
from app.utils.splitter import get_splitter
from app.services.weaviate_services import transformer, client
 
def process_article(url: str):
    """
    Fetch article from URL, split into chunks, embed, and store in Weaviate.
    Enhanced with browser User-Agent and improved error handling.
    """
    try:
        # -------------------
        # Fetch URL content
        # -------------------
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/122.0.0.0 Safari/537.36"
            ),
            "Accept-Language": "en-US,en;q=0.9",
        }
        response = requests.get(url,  headers=headers, timeout=10)
        response.raise_for_status()
        # if response.status_code != 200:
        #     return f"Failed to fetch URL: {url}"
       
        soup = BeautifulSoup(response.text, "html.parser")
        article_text = " ".join([p.get_text() for p in soup.find_all("p") if p.get_text().strip()])
 
        if not article_text.strip():
            return "No textual content found in the provided URL."
 
        # -------------------
        # Split into chunks
        # -------------------
        chunks = get_splitter(text=article_text)  # returns list of Document objects
 
        # Extract raw text from each chunk
        texts = [chunk.page_content for chunk in chunks]
 
        # -------------------
        # Embed and store in Weaviate
        # -------------------
        doc_collection = client.collections.get("Document")
        embeddings = transformer.encode(texts).tolist()
 
        for text, vector in zip(texts, embeddings):
            doc_collection.data.insert(
                properties={"content": text, "source_url": url},
                vector=vector
            )
 
        return f"Successfully processed article: {url} with {len(texts)} chunks."
 
 
    except Exception as e:
        return f"Error processing article: {str(e)}"
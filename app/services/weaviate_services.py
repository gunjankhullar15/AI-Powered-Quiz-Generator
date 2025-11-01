import weaviate
import weaviate.classes as wvc
from sentence_transformers import SentenceTransformer
 
# Load model once
transformer = SentenceTransformer('all-MiniLM-L6-v2')
 
#  Connect once
client = weaviate.connect_to_local()
 
#  Create collection if not exists
if not client.collections.exists("Document"):
    client.collections.create(
        name="Document",
        properties=[wvc.config.Property(name="content", data_type=wvc.config.DataType.TEXT)],
        vectorizer_config=wvc.config.Configure.Vectorizer.none()
    )
 
# Load model once
# transformer = SentenceTransformer('all-MiniLM-L6-v2')
 
 
# def search_in_weaviate(query: str, limit: int = 3):
#     doc_collection = client.collections.get("Document")
#     query_vector = transformer.encode(query).tolist()
 
#     results = doc_collection.query.near_vector(query_vector, limit=limit, return_properties=["content"])
#     matches = [obj.properties.get("content", "") for obj in results.objects]
#     return {"query": query, "results": matches}
 
#fetch all the data from weaviate
def search_in_weaviate(query: str, max_chunks: int = 3):
    """
    Perform semantic search in Weaviate using the topic as query.
    Fetches up to `max_chunks` (~300 words each) of related content.
    """
    doc_collection = client.collections.get("Document")
 
 
    # Skip empty query (fetch all)
    if not query:
        results = doc_collection.query.fetch_objects(limit=max_chunks, return_properties=["content"])
        return [{"content": obj.properties.get("content", "")} for obj in results.objects]
   
 
    query_vector = transformer.encode(query).tolist()
 
    # Perform similarity search
    results = doc_collection.query.near_vector(
        near_vector=query_vector,
        limit=max_chunks,
        return_properties=["content"],
        certainty=0.3
    )
 
    #  Return in a clean consistent format
    matches = [{"content": obj.properties.get("content", "")} for obj in results.objects]
    return matches
 
 
def clear_weaviate_data(client):
    #  Deleting all existing data
    try:
        client.collections.delete("Document")
        return " Cleared all objects from the 'Document' class."
    except Exception as e:
        return f" Failed to delete old data: {e}"
import weaviate
import weaviate.classes as wvc
from sentence_transformers import SentenceTransformer
 
# Load model once
transformer = SentenceTransformer('all-MiniLM-L6-v2')
 
# ✅ Connect once
client = weaviate.connect_to_local()
 
# ✅ Create collection if not exists
if not client.collections.exists("Document"):
    client.collections.create(
        name="Document",
        properties=[
            wvc.config.Property(name="content", data_type=wvc.config.DataType.TEXT),
            wvc.config.Property(name="source_url", data_type=wvc.config.DataType.TEXT),
            wvc.config.Property(name="filename", data_type=wvc.config.DataType.TEXT),
        ],
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
# def search_in_weaviate(query: str, max_chunks: int = 10):
#     """
#     Perform semantic search in Weaviate using the topic as query.
#     Fetches up to `max_chunks` (~300 words each) of related content.
#     """
#     doc_collection = client.collections.get("Document")
 
 
#     # Skip empty query (fetch all)
#     if not query:
#         results = doc_collection.query.fetch_objects(limit=max_chunks, return_properties=["content"])
#         return [{"content": obj.properties.get("content", "")} for obj in results.objects]
   
 
#     query_vector = transformer.encode(query).tolist()
 
#     # Perform similarity search
#     results = doc_collection.query.near_vector(
#         near_vector=query_vector,
#         limit=max_chunks,
#         return_properties=["content"],
#         certainty=0.3
#     )
 
#     # 🧩 Return in a clean consistent format
#     matches = [{"content": obj.properties.get("content", "")} for obj in results.objects]
#     return matches
 

def search_in_weaviate(query: str, max_chunks: int = 10):
    """
    Perform semantic search in Weaviate.
    Ensures balanced results from both articles and PDFs.
    """
    doc_collection = client.collections.get("Document")
    query_vector = transformer.encode(query).tolist()
    
    # Fetch more results to ensure diversity
    results = doc_collection.query.near_vector(
        near_vector=query_vector,
        limit=max_chunks * 3,
        return_properties=["content", "source_url", "filename"],
        certainty=0.3
    )
    
    # Group by source
    sources = {}
    for obj in results.objects:
        source = obj.properties.get("source_url") or obj.properties.get("filename", "unknown")
        if source not in sources:
            sources[source] = []
        sources[source].append({
            "content": obj.properties.get("content", ""),
            "source": source,
            "source_url": obj.properties.get("source_url"),
            "filename": obj.properties.get("filename")
        })
    
    # Balance results across sources (round-robin)
    balanced_results = []
    while len(balanced_results) < max_chunks and any(sources.values()):
        for source in list(sources.keys()):
            if sources[source]:
                balanced_results.append(sources[source].pop(0))
                if len(balanced_results) >= max_chunks:
                    break
    
    return balanced_results



# def clear_weaviate_data(client):
#     # 🧹 Deleting all existing data
#     try:

#         if "Document" not in client.collections.list_all():
#             return "⚠️ 'Document' collection does not exist."

#         # Access the collection
#         collection = client.collections.get("Document")

#         # Count how many objects exist
#         count_result = collection.aggregate.over_all()
#         total_objects = count_result.total_objects

#         if total_objects == 0:
#             return "No data found in 'Document' collection. Nothing to delete."
        
#         client.collections.delete("Document")
#         return "🧹 Cleared all objects from the 'Document' class."
#     except Exception as e:
#         return f"⚠️ Failed to delete old data: {e}"

# def clear_weaviate_data(client):
#     try:
#         collections = client.collections.list_all()
#         if "Document" not in collections:
#             return "'Document' collection does not exist."

#         collection = client.collections.get("Document")

#         try:
#             count_result = collection.aggregate.over_all()
#             total_objects = count_result.objects[0].total_count if count_result.objects else 0
#         except Exception:
#             total_objects = None

#         client.collections.delete("Document")

#         if total_objects:
#             return f"Cleared all {total_objects} objects from the 'Document' collection."
#         else:
#             return "Cleared all objects from the 'Document' collection."
#     except Exception as e:
#         return f"Failed to delete old data: {e}"


def clear_weaviate_data(client):
    try:
        
        collections = client.collections.list_all()
        total_objects = 0
        
        if "Document" in collections:
            collection = client.collections.get("Document")
            try:
                count_result = collection.aggregate.over_all()
                total_objects = count_result.objects[0].total_count if count_result.objects else 0
            except Exception:
                total_objects = 0
             
            
            client.collections.delete("Document")

        client.collections.create(
            name="Document",
            properties=[
                wvc.config.Property(name="content", data_type=wvc.config.DataType.TEXT),
                wvc.config.Property(name="source_url", data_type=wvc.config.DataType.TEXT),
                wvc.config.Property(name="filename", data_type=wvc.config.DataType.TEXT),
            ],
            vectorizer_config=wvc.config.Configure.Vectorizer.none()
        )

        if total_objects > 0:
            return f"Cleared {total_objects} objects and reset 'Document' schema."
        else:
            return "Reset 'Document' schema (was empty)."

    except Exception as e:
        return f"Failed to reset data: {e}"

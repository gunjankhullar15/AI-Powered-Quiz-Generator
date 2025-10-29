import weaviate
import weaviate.classes as wvc
from sentence_transformers import SentenceTransformer

# ✅ Connect once
client = weaviate.connect_to_local()

# ✅ Create collection if not exists
if not client.collections.exists("Document"):
    client.collections.create(
        name="Document",
        properties=[wvc.config.Property(name="content", data_type=wvc.config.DataType.TEXT)],
        vectorizer_config=wvc.config.Configure.Vectorizer.none()
    )

# Load model once
transformer = SentenceTransformer('all-MiniLM-L6-v2')

def search_in_weaviate(query: str, limit: int = 3):
    doc_collection = client.collections.get("Document")
    query_vector = transformer.encode(query).tolist()

    results = doc_collection.query.near_vector(query_vector, limit=limit, return_properties=["content"], certainty=0.6)
    matches = [obj.properties.get("content", "") for obj in results.objects]
    return {"query": query, "results": matches}

import chromadb
from services.Model_loader import get_model
from typing import List , Dict, Any
model = get_model()
client = chromadb.PersistentClient(path="./database/chroma_db")
collection = client.get_or_create_collection(name="rag_collection")



def extract_results(results: Dict[str, Any]) -> List[Dict[str, Any]]:
    ids = results.get("ids", [[]])[0]
    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    formatted_results = []

    for i in range(len(ids)):
        formatted_results.append({
            "id": ids[i],
            "document": documents[i] if i < len(documents) else None,
            "metadata": metadatas[i] if i < len(metadatas) else {},
            "distance": distances[i] if i < len(distances) else None
        })

    return formatted_results

def retrive_from_chroma(embedding: List[float]) -> Dict[str, Any] | str:

    if not embedding:
        raise ValueError("Embedding is required")
    
    results = collection.query(
        query_embeddings = [embedding],
        n_results = 8
    )
    if not results:
        print('No results from Chroma')
        return{
            "message": "No related content found"
        }
    # print('Results from Chroma: ',results)
    return extract_results(results)
    
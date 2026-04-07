from typing import List, Dict , Any
from chromadb.api import client
import chromadb

client = chromadb.PersistentClient(path="./database/chroma_db")
collection = client.get_or_create_collection(name="rag_collection", 
    metadata={ "description":"RAG Collection", "hnsw:space":"cosine"})


def get_existing_ids(ids: List) -> List:
    """
    Get the Existing Ids from chroma
    """

    try:
        existing_ids = collection.get(ids=ids)['ids']
        return existing_ids
    except Exception as e:
        print(f"Error getting existing ids: {e}")
        return []

def add_chunks_to_chroma(chunks: List[Dict[str, Any]]) ->  Dict[str,Any]:
    """
    Add chunks to Chroma DB
    """




    if not chunks:
        return{
            "status":"error",
            "message":"No chunks provided"
        }
    
    ids = [chunk['chunk_id'] for chunk in chunks]
    docs = [chunk['text'] for chunk in chunks]
    metadata = [chunk['metadata'] for chunk in chunks]
    embeddings = [chunk['embedding'] for chunk in chunks]


    existing_ids = get_existing_ids(ids)

    filtered_ids = []
    filtered_docs = []
    filtered_embeddings = []
    filtered_metadatas = []

    for idx , chunk_id in enumerate(ids):
        if chunk_id not in existing_ids:
            filtered_ids.append(chunk_id)
            filtered_docs.append(docs[idx])
            filtered_embeddings.append(embeddings[idx])
            filtered_metadatas.append(metadata[idx])

    if not filtered_ids:
        return{
            "status":"success",
            "message":"No new chunks to add, All ids in vector store",
            "inserted_count": 0
        }

    try:
        collection.add(
            ids = filtered_ids,
            metadatas = filtered_metadatas,
            embeddings = filtered_embeddings,
            documents= filtered_docs
        )
        return{
            "status":"success",
            "message":f"Successfully added {len(filtered_ids)} new chunks to Chroma DB",
            "inserted_count": len(filtered_ids)
        }
    except Exception as e:
        return{
            "status":"error",
            "message":f"Error adding chunks to Chroma DB: {e}"
        }






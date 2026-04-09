from typing import List
from chromadb.api import client
import chromadb

client = chromadb.PersistentClient(path="./database/chroma_db")
collection = client.get_or_create_collection(name="rag_collection", 
    metadata={ "description":"RAG Collection", "hnsw:space":"cosine"})


def get_collections() -> bool:
    """
    Get the statistics and contents of the RAG collection.
    """
    try:
        # Get count of items
        count = collection.count()
        print(f"Collection count: {count}")
        
        if count == 0:
            print("Collection is empty.")
            return False
        else:
            print("Collection has content")
            return True
    except Exception as e:
        print(f"Error getting collection info: {e}")
        return False


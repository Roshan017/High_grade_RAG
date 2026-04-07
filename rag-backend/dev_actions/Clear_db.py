import chromadb


try:
    client = chromadb.PersistentClient(path="./database/chroma_db")
    collection = client.get_or_create_collection(name="rag_collection")
    collection.delete(
        where={
            "user_id": "dev_user_001"
        }
    )
    print("✅ Database cleared successfully.")
except Exception as e:
    print(f"❌ Error clearing database: {e}")
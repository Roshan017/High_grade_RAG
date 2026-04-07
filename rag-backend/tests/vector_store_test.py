import chromadb


try:
    client = chromadb.PersistentClient(path="./database/chroma_db")
    collection = client.get_or_create_collection(name="rag_collection")
    count = collection.count()
    print(f"✅ Connection Successful!")
    print(f"📊 Total chunks in 'rag_collection': {count}")
except Exception as e:
    print(f"❌ Error connecting to Vector Store: {e}")

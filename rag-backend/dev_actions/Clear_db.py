import chromadb
import os
import json

def clear_db():
    try:
        client = chromadb.PersistentClient(path="./database/chroma_db")
        collection = client.get_or_create_collection(name="rag_collection")
        collection.delete(
            where={
                "user_id": "dev_user_001"
            }
        )
        print("✅ Database cleared successfully.")
        
        # Safely wipe the Ragas analytics data
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_json_path = os.path.join(base_dir, "llm", "ragas", "data.json")
        
        if os.path.exists(data_json_path):
            with open(data_json_path, "w", encoding="utf-8") as f:
                json.dump([], f)
            print("✅ Ragas evaluation data (data.json) cleared successfully.")
            
    except Exception as e:
        print(f"❌ Error clearing system: {e}")

if __name__ == "__main__":
    clear_db()
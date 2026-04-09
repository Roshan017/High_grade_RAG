import chromadb
import shutil
import os

def clear_db():
    print("Clearing Chroma DB...")
    db_path = "./database/chroma_db"
    
    try:
        # Connect to client to delete collection first (cleaner)
        client = chromadb.PersistentClient(path=db_path)
        collections = client.list_collections()
        for col in collections:
            print(f"Deleting collection: {col.name}")
            client.delete_collection(name=col.name)
            
        # Hard wipe the directory to be sure
        if os.path.exists(db_path):
            shutil.rmtree(db_path)
            os.makedirs(db_path)
            
        print("Database cleared successfully.")
    except Exception as e:
        print(f"Error clearing database: {e}")

if __name__ == "__main__":
    confirm = input("Are you sure you want to clear the database? (y/n): ")
    if confirm.lower() == 'y':
        clear_db()
    else:
        print("Operation cancelled.")

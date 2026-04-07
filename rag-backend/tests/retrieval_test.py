import os
import sys
import chromadb

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from services.Model_loader import get_model

model = get_model()
client = chromadb.PersistentClient(path="./database/chroma_db")
collection = client.get_or_create_collection(name="rag_collection")

query = "Who is Roshan P Mathew"

query_embedding = model.encode(query, normalize_embeddings=True).tolist()

results = collection.query(
    query_embeddings = [query_embedding],
    n_results = 3
)
if not results["ids"][0]:
    print("No results found.")
    sys.exit(0)
print("🔍 Search Results:\n")

for i in range(len(results["ids"][0])):
    print(f"Result {i+1}")
    print("ID:", results["ids"][0][i])
    print("Distance:", results["distances"][0][i])
    print("Metadata:", results["metadatas"][0][i])
    print("Text:", results["documents"][0][i])
    print("-" * 80)
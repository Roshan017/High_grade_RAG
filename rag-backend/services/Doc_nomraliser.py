from uuid import uuid4
from typing import Dict , List , Any

def Doc_Normalizer(docs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    This function is responsible for normalising the documents to the RAG system.
    """
    normalized_docs = []

    for idx , doc in enumerate(docs):
        normalized_docs.append(
            {
                "doc_id": f"doc_{idx+1}_{uuid4().hex[:6]}",
                "filename": doc.get("filename",'unknown'),
                "text": doc.get("content",""),
                "metadata": {
                    "file_type": doc.get("file_type", "unknown")
                }

            }
        )
    
    return normalized_docs
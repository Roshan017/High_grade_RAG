from uuid import uuid4
from typing import Dict, List, Any

def Doc_Normalizer(docs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    This function is responsible for normalising the documents to the RAG system.
    """
    normalized_docs = []

    for idx, doc in enumerate(docs):
        content = doc.get('content', " ")
        filename = doc.get("filename", 'unknown')
        file_type = doc.get("file_type", "unknown")
        doc_id = f"doc_{idx+1}_{uuid4().hex[:6]}"

        if isinstance(content, list):
            for page in content:
                normalized_docs.append({
                    "doc_id": doc_id,
                    "filename": filename,
                    "text": page.get('text', ""),
                    "metadata": {
                        "file_type": file_type,
                        "page_number": page.get('page_no', "unknown")
                    }
                })
        else:
            normalized_docs.append({
                "doc_id": doc_id,
                "filename": filename,
                "text": content,
                "metadata": {
                    "file_type": file_type,
                    "page_number": 1
                }
            })
    
    return normalized_docs
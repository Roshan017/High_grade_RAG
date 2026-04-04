from services.Embedder.BGE_Embedder import embed_texts
from typing import Dict, List, Any


def embed_chunks(chunks: List[Dict[str, Any]]) -> List[Dict[str,Any]]:
    """
    Takes chunk dictionaries, generates embeddings,
    and adds embedding vectors to each chunk.
    """

    if not chunks:
        return []

    
    texts = [chunk["text"].strip().replace("\n", " ") for chunk in chunks ]

    embeddings = embed_texts(texts)

    embedded_chunks = []

    for chunk, cleaned_text , embedding in zip(chunks, texts, embeddings):
        chunk['text'] = cleaned_text
        chunk['embedding'] = embedding

        if "metadata" not in chunk:
            chunk['metadata'] = {}
        
        chunk["metadata"]["chunk_length"] = len(cleaned_text)

        chunk["metadata"]["embedding_model"] = 'BAAI/bge-small-en-v1.5'

        embedded_chunks.append(chunk)

    return embedded_chunks

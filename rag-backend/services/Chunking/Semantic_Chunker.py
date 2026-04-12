import nltk
import numpy as np
from typing import List, Dict, Any
from sklearn.metrics.pairwise import cosine_similarity
from services.Model_loader import get_model


def Semantic_Chunker(
    Docs_list: List[Dict[str, Any]],
    similarity_threshold: float = 0.79,
    min_chunk_sentences: int = 3,
    max_chunk_sentences: int = 5
) -> List[Dict[str, Any]]:
    """
    Groups sentences into chunks based on semantic similarity using a rolling mean strategy.
    """

    model = get_model()
    all_chunks = []

    for doc in Docs_list:
        text = doc.get("text", "").strip()
        metadata = doc.get("metadata", {})
        filename = doc.get("filename", "unknown")
        doc_id = doc.get("doc_id", "unknown")

        sentences = nltk.sent_tokenize(text)
        if not sentences:
            continue

        if len(sentences) == 1:
            page_no = metadata.get('page_number', 'unknown')
            chunk_id = f"{doc_id}_p{page_no}_semantic_chunk_1"
            all_chunks.append({
                "chunk_id": chunk_id,
                "text": sentences[0],
                "metadata": {
                    **metadata,
                    "user_id":"dev_user_001",
                    "doc_id": doc_id,
                    "filename": filename,
                    "chunk_index": 1,
                    "chunking_type": "semantic",
                    "chunk_id": chunk_id,
                    "page_number": page_no,
                    "chunks_length": 1
                }
            })
            continue

        sentence_embeddings = model.encode(sentences, normalize_embeddings=True)

        doc_chunks = []
        current_chunk = [sentences[0]]
        current_embeddings = [sentence_embeddings[0]]

        for i in range(1, len(sentences)):
            next_sentence = sentences[i]
            next_embedding = sentence_embeddings[i]

            chunk_embedding_mean = np.mean(current_embeddings, axis=0).reshape(1, -1)
            next_sent_embedding = next_embedding.reshape(1, -1)

            sim = cosine_similarity(chunk_embedding_mean, next_sent_embedding)[0][0]

            if len(current_chunk) < min_chunk_sentences:
                current_chunk.append(next_sentence)
                current_embeddings.append(next_embedding)

            elif sim >= similarity_threshold and len(current_chunk) < max_chunk_sentences:
                current_chunk.append(next_sentence)
                current_embeddings.append(next_embedding)

            else:
                doc_chunks.append({
                    "text": " ".join(current_chunk),
                    "metadata_partial": {
                        "chunking_type": "semantic",
                        "chunks_in_this_doc": len(current_chunk) # Temp: not needed but for record
                    }
                })
                current_chunk = [next_sentence]
                current_embeddings = [next_embedding]

        # Add the final chunk if it exists
        if current_chunk:
            doc_chunks.append({
                "text": " ".join(current_chunk),
                "metadata_partial": {
                    "chunking_type": "semantic"
                }
            })

        total_doc_chunks = len(doc_chunks)
        
        for idx, chunk_data in enumerate(doc_chunks):
            page_no = metadata.get('page_number', 'unknown')
            chunk_id = f"{doc_id}_p{page_no}_semantic_chunk_{idx + 1}"
            all_chunks.append({
                "chunk_id": chunk_id,
                "text": chunk_data["text"],
                "metadata": {
                    **metadata,
                    "user_id": "dev_user_001",
                    "doc_id": doc_id,
                    "filename": filename,
                    "chunk_index": idx + 1,
                    "chunking_type": "semantic",
                    "chunk_id": chunk_id,
                    "page_number": page_no,
                    "total_chunks": total_doc_chunks
                }
            })

    print(f"✅ Semantic Chunking Complete: Generated {len(all_chunks)} chunks.")
    return all_chunks
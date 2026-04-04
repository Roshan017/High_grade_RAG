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
            all_chunks.append({
                "chunk_id": f"{doc_id}_semantic_chunk_1",
                "text": sentences[0],
                "metadata": {
                    **metadata,
                    "doc_id": doc_id,
                    "filename": filename,
                    "chunk_index": 1,
                    "chunking_type": "semantic",
                    "chunks_length": 1
                }
            })
            continue

        sentence_embeddings = model.encode(sentences, normalize_embeddings=True)

        current_chunk = [sentences[0]]
        current_embeddings = [sentence_embeddings[0]]
        chunk_idx = 1

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
                all_chunks.append({
                    "chunk_id": f"{doc_id}_semantic_chunk_{chunk_idx}",
                    "text": " ".join(current_chunk),
                    "metadata": {
                        **metadata,
                        "doc_id": doc_id,
                        "filename": filename,
                        "chunk_index": chunk_idx,
                        "chunking_type": "semantic",
                        "chunks_length": len(current_chunk)
                    }
                })

                chunk_idx += 1
                current_chunk = [next_sentence]
                current_embeddings = [next_embedding]

        # Add the final chunk if it exists
        if current_chunk:
            all_chunks.append({
                "chunk_id": f"{doc_id}_semantic_chunk_{chunk_idx}",
                "text": " ".join(current_chunk),
                "metadata": {
                    **metadata,
                    "doc_id": doc_id,
                    "filename": filename,
                    "chunk_index": chunk_idx,
                    "chunking_type": "semantic",
                    "chunks_length": len(current_chunk)
                }
            })

    print(f"✅ Semantic Chunking Complete: Generated {len(all_chunks)} chunks.")
    return all_chunks
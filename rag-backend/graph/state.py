from typing import TypedDict, List, Dict, Any, Optional


class Chunk_class(TypedDict, total=False):
    chunk_id: str
    text: str
    metadata: Dict[str, Any]
    embedding: Optional[List[float]]


class RetrievedChunk(TypedDict, total=False):
    chunk_id: str
    text: str
    metadata: Dict[str, Any]
    score: float

class Citation(TypedDict, total=False):
    chunk_id: str
    source: str
    text: str

class RAG_State(TypedDict, total=False):
    # Ingestion
    uploaded_files: List[str]
    raw_docs: List[Dict[str, Any]]
    user_id: str

    # Chunking
    chunking_strategy: str
    fixed_size_chunks: List[Chunk_class]
    semantic_segments: List[Chunk_class]

    # Embedding / Indexing
    embedded_fixed_chunks: List[Chunk_class]
    embedded_semantic_chunks: List[Chunk_class]
    
    indexing_complete: bool

    # Query
    query: str
    query_embedding: List[float]
    query_status: bool

    # Retrieval
    retrieved_chunks: List[RetrievedChunk]

    # Generation
    ids_to_metadata: Dict[str, Any]
    final_answer: str
    citations: List[Citation]

    # Status flags (optional)
    chunks_embedding_complete: bool
    query_embedding_complete: bool
    retrieved_chunks_complete: bool
    final_answer_complete: bool
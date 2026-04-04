from graph.state import RAG_State
from services.Embedder.Embedding_service import embed_chunks
def Embedder_node(state: RAG_State):

    fixed_chunks = state.get('fixed_size_chunks')
    semantic_chunks = state.get('semantic_segments')


    print(f"🧬 Vectorizing {len(fixed_chunks)} Fixed-size chunks...")
    fixed_chunk_embeddings = embed_chunks(fixed_chunks)

    print(f"🧬 Vectorizing {len(semantic_chunks)} Semantic chunks...")
    semantic_chunk_embeddings = embed_chunks(semantic_chunks)


    state['embedded_fixed_chunks'] = fixed_chunk_embeddings
    state['embedded_semantic_chunks'] = semantic_chunk_embeddings

    state['chunks_embedding_complete'] = True



    return {
        'embedded_fixed_chunks': fixed_chunk_embeddings,
        'embedded_semantic_chunks': semantic_chunk_embeddings,
        'chunks_embedding_complete': True
    }

from graph.state import RAG_State
from services.Doc_nomraliser import Doc_Normalizer
from services.Chunking.Fixed_Chunker import Fixed_Chunker
from services.Chunking.Semantic_Chunker import Semantic_Chunker
from services.File_writer import File_writer
def Chunking_node(state: RAG_State):
    """
    This node is responsible for chunking the documents to the RAG system.
    """
    raw_docs = state.get('raw_docs',[])
    total_content_length = sum(len(doc['content']) for doc in raw_docs)

   

    normalized_docs = Doc_Normalizer(raw_docs)

    # print("Chunking Node: ",normalized_docs)

    if total_content_length < 1000:
        chunk_size = 200
        overlap = 50
    else:
        chunk_size = 1000
        overlap = 200
    
    fixed_chunks = Fixed_Chunker(normalized_docs, chunk_size, overlap)

    semantic_chunks = Semantic_Chunker(normalized_docs)
    # print("Chunking Node: Fixed Chunks: ",fixed_chunks)

    File_writer(fixed_chunks,  "fixed")
    File_writer(semantic_chunks, "semantic")

    

    return {  
        'fixed_size_chunks': fixed_chunks,
        'semantic_segments': semantic_chunks,
        'chunking_strategy': 'fixed and semantic'
      }
    
    
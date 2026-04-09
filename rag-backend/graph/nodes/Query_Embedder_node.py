from graph.state import RAG_State
from services.Embedder.BGE_Embedder import embed_query




def Query_Embedder_node(state: RAG_State):

    query = state.get('query', "")

    if not query:
        raise ValueError("No query provided")
    try:
        # print('Embedding User Query: ', query)
        query_embedding = embed_query(query)
        # print(query_embedding)
    except Exception as e:
        raise ValueError(f"Error embedding query: {str(e)}")

    
    return {
        "query_status": True,
        "query_embedding": query_embedding
        }
from graph.state import RAG_State
from services.Vector_store.Retrive_from_chroma import retrive_from_chroma


def Retrieval_node(state: RAG_State):
    print('Retrieval_node Entered')
    query_embedding = state['query_embedding']
    if not query_embedding:
        raise ValueError("Query embedding is required")
    try:
        results = retrive_from_chroma(query_embedding)
        print('Results from Chroma: ',results)
    except Exception as e:
        print(str(e))
        return {
            "message": f"Error in retrieval: {str(e)}"
        }
    
    if not results:
        print('No results')
        return {
            "message": "No related content found"
        }
    print('Retrieval_node Exit')
    return {
        "retrieved_chunks": results,
        "retrieved_chunks_complete": True
    }
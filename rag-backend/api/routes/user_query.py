from api.middlewares.Get_user import get_current_user
from fastapi import APIRouter, HTTPException, Depends
from graph.graph import build_RAG_State_Graph
from graph.state import RAG_State
from models.user_model import User_Query
from langfuse import observe
from llm.ragas.logger import log_interaction
router = APIRouter()

rag_state_graph = build_RAG_State_Graph()

@router.post("/query")
@observe(name="user-query")
def query_endpoint(user_query: User_Query, user_id: str = Depends(get_current_user)):

    if not user_query.query:
        raise HTTPException(status_code=400, detail="No query provided")

    # Securely override any client-provided ID with the verified JWT user ID
    user_query.userid = user_id

    try:
        result = rag_state_graph.invoke({
            
            'query': user_query.query,
            'userid': user_query.userid
        })

        ans = result.get('final_answer')
        citations = result.get('citations')
        
        retrieved_list = result.get('chunk_to_llm', [])
        ret_chunks = [chunk.get("content", "") for chunk in retrieved_list if isinstance(chunk, dict)]
        print('Logger: ', len(ret_chunks), 'chunks logged')

        if not ans:
            ans = "No answer found"
            citations = "No citations found"
        log_interaction(user_query.query, ans, ret_chunks)

        return {
            "query": result.get('query'),
            "final_answer": ans,
            "citations": citations,
            "retrieved_chunks": ret_chunks
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
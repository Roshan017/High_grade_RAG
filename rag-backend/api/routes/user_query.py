from fastapi import APIRouter, HTTPException
from graph.graph import build_RAG_State_Graph
from graph.state import RAG_State
from models.user_model import User_Query

router = APIRouter()

rag_state_graph = build_RAG_State_Graph()

@router.post("/query")
def query_endpoint(user_query: User_Query):

    if not user_query.query:
        raise HTTPException(status_code=400, detail="No query provided")

    if not user_query.userid:
        user_query.userid = "dev_user_001"

    try:
        result = rag_state_graph.invoke({
            'query': user_query.query,
            'userid': user_query.userid
        })
        chunks = result.get('retrieved_chunks')
        query_status = result.get('query_status')
        query = result.get('query')
        return {
            "query": query,
            "query_status": query_status,
            "retrieved_chunks": chunks,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
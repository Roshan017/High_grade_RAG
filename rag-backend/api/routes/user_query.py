from fastapi import APIRouter, HTTPException
from graph.graph import build_RAG_State_Graph
from graph.state import RAG_State
from models.user_model import User_Query
from langfuse import observe

router = APIRouter()

rag_state_graph = build_RAG_State_Graph()

@router.post("/query")
@observe(name="user-query")
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

        ans = result.get('final_answer')

        if not ans:
            ans = "No answer found"

        return {
            "query": result.get('query'),
            "final_answer": ans
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
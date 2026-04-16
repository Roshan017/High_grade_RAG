from fastapi import APIRouter, HTTPException , UploadFile, File
from graph.graph import build_RAG_State_Graph
from graph.state import RAG_State
from models.doc_model import  Doc_Res_Model
from dev_actions.Clear_db import clear_db

router = APIRouter()

@router.post('/doc-upload', response_model = Doc_Res_Model)
async def doc_upload(file : UploadFile = File(...)):
    rag_graph = build_RAG_State_Graph()
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")

    allowed_extensions = ["pdf", "docx", "txt", "md"]
    file_ext = file.filename.split('.')[-1].lower()


    if file_ext not in allowed_extensions:
        raise HTTPException(status_code=400, detail="Invalid file type")

    file_bytes = await file.read()
    # print("Doc Upload API: ", file_bytes)
    
    result = rag_graph.invoke({
        "user_id": "dev_user_001",
        "uploaded_files": [file.filename],
        "raw_docs": [{"filename": file.filename, "content": file_bytes, "file_type": file_ext}]
    })

    return Doc_Res_Model(
        status="success",
        message="Document uploaded successfully",
        data=result
    )

@router.post('/cleardb')
def clear_full_db():
    try:
        clear_db()
        return {
            "message": "Database cleared successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
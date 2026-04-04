from fastapi import APIRouter, HTTPException , UploadFile, File
from graph.graph import build_RAG_State_Graph
from graph.state import RAG_State
from models.doc_model import  Doc_Res_Model

router = APIRouter()

rag_graph = build_RAG_State_Graph()

@router.post('/doc-upload', response_model = Doc_Res_Model)
async def doc_upload(file : UploadFile = File(...)):

    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")

    allowed_extensions = ["pdf", "docx", "txt", "md"]
    file_ext = file.filename.split('.')[-1].lower()


    if file_ext not in allowed_extensions:
        raise HTTPException(status_code=400, detail="Invalid file type")

    file_bytes = await file.read()
    # print("Doc Upload API: ", file_bytes)
    
    result = rag_graph.invoke({
        "uploaded_files": [file.filename],
        "raw_docs": [{"filename": file.filename, "content": file_bytes, "file_type": file_ext}]
    })

    return Doc_Res_Model(
        status="success",
        message="Document uploaded successfully",
        data=result
    )
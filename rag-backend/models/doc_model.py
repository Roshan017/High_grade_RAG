from fastapi import UploadFile
from pydantic import BaseModel
from typing import Dict, Any , Optional, Literal

class Doc_Req_Model(BaseModel):
    file: UploadFile
    file_name: str
    file_type: Literal["pdf","docx","txt","md"]

class Doc_Res_Model(BaseModel):
    status: str
    message: str
    data: Optional[Dict[str, Any]] = None
    
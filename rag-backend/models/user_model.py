from pydantic import BaseModel
from typing import Dict, Any , Optional, Literal

class User_Query(BaseModel):
    userid: str = 'dev_user_001'
    query: str
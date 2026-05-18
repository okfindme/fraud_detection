from pydantic import BaseModel , ConfigDict
from datetime import datetime 

class ApiKeyCreate(BaseModel):
    name :str

class ApiKeyResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id : int 
    name : str 
    is_active : bool
    created_at : datetime
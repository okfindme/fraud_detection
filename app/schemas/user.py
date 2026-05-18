from pydantic import BaseModel , Field , EmailStr , ConfigDict
from typing import Annotated
from datetime import datetime

class UserCreate(BaseModel):
    email : Annotated[EmailStr , Field(...,description="user email")]
    full_name : Annotated[str, Field(...,description="user name")]

class UserResponse(BaseModel):
    # it just says user may repond with otherthan dict in that case use attribute access.
    model_config = ConfigDict(from_attributes=True)

    id:Annotated[int , Field(...,description="id of user")]
    email:Annotated[EmailStr , Field(...,description="email of user")]
    full_name:Annotated[str , Field(...,description="full_name of user")]
    is_active:Annotated[bool , Field(...,description="checks if user is active")]
    created_at:Annotated[datetime , Field(...,description="time when user is created")]
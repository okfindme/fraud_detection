from pydantic import BaseModel , ConfigDict
from datetime import datetime

class PredictionCreate(BaseModel):
    amount:float
    merchant : str 
    card_type : str 

class PredictionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id : int 
    user_id : int 
    amount :float 
    merchant : str 
    fraud_score : float 
    is_fraud : bool 
    model_version : str 
    created_at : datetime
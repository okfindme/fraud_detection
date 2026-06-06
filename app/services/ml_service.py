# this is a stub ( gimmick function needs to connect the real model later
import random
_model_ready = True
def predict (features:dict)->dict:
    fraud_score =random.uniform(0,1)
    is_fraud = fraud_score >= 0.5
    model_version = "1.0"

    return {
        "fraud_score" : fraud_score,
        "is_fraud" : is_fraud,
        "model_version" : model_version
    }

def is_loaded() -> bool:
    return _model_ready
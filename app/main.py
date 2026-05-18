from contextlib import asynccontextmanager
from fastapi import FastAPI
import subprocess
from app.api.routes.users import router as users_router
from app.api.routes.predictions import router as predictions_router
from app.api.routes.api_keys import router as api_keys_router
@asynccontextmanager
async def lifespan(app: FastAPI):
    subprocess.run(["alembic", "upgrade", "head"], check=True)
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(users_router)
app.include_router(predictions_router)
app.include_router(api_keys_router)


"""
--> this was the sync code 

from app.db.base import Base
from app.db.session import SessionLocal , engine
from app.models.user import User
from app.models.prediction import Prediction
from app.models.audit_log import AuditLog
from app.models.api_key import ApiKey

#now this is done by the alembic , it manages the creation and sync it 
# This line is now not just redundant — it's dangerous. If it runs before a migration, it can create tables outside Alembic's tracking, causing the exact silent-empty-migration problem we discussed at the start.
#Base.metadata.create_all(engine)

session = SessionLocal()

try:
    #insert one user
    user = User(email="test2@example.com",full_name="Test User2")
    session.add(user)
    session.flush()
    # insert one prediction 
    prediction = Prediction(user_id=user.id, amount=33, merchant="Amazon", 
                        card_type="visa", fraud_score=0.33, is_fraud=False)
    session.add(prediction)
    session.flush()
    # insert one auditlog 
    auditlog = AuditLog(prediction_id=prediction.id, ip_address="192.168.1.1", 
                    endpoint="/api/v1/predict", status_code=200, latency_ms=45.3)
    session.add(auditlog)
    session.flush()
    session.commit()

    prediction = session.query(Prediction).first()
    print(prediction.owner.email)
    print(len(prediction.owner.predictions))

    
finally:
    session.close()"""
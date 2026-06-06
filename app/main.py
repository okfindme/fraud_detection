from contextlib import asynccontextmanager
from fastapi import FastAPI, Request , Depends
import subprocess
from app.api.routes.users import router as users_router
from app.api.routes.predictions import router as predictions_router
from app.api.routes.api_keys import router as api_keys_router
# ----------------->> imports for = exception handling and logging it <<---------------------
from app.core.logging import get_logger ,setup_logging
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
import time

# ----------------->> imports for = rate limiting  <<---------------------
from slowapi import  _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.core.limiter import limiter

# ----------------->> imports for = corsmiddleare  <<---------------------
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

# ------------------>> imports for health checkup <<-----------------------
from sqlalchemy import text
from app.db.session import AsyncSessionLocal
from app.services.ml_service import is_loaded
import datetime

@asynccontextmanager
async def lifespan(app: FastAPI):
    subprocess.run(["alembic", "upgrade", "head"], check=True)
    yield

setup_logging() # It configures structlog globally
logger = get_logger("fraud_api") 

app = FastAPI(lifespan=lifespan)


app.state.limiter = limiter # rate limit 

app.include_router(users_router)
app.include_router(predictions_router)
app.include_router(api_keys_router)

#  ----------------->> middleware <<---------------------

@app.middleware("http")
async def request_logging_middleware(request: Request, call_next):
    start_time = time.time()

    has_api_key = "X-API-Key" in request.headers
    bound_logger = logger.bind(
        method=request.method,
        path=request.url.path,
        has_api_key=has_api_key,
    )

    bound_logger.info("request_started")

    response = await call_next(request)

    latency_ms = round((time.time() - start_time) * 1000, 2)
    bound_logger.info(
        "request_finished",
        status_code=response.status_code,
        latency_ms=latency_ms,
    )

    return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]         # Allow all headers
    )


# ----------------->> health checkup <<--------------------
@app.get("/health")
async def health_check():  # no Depends
    async with AsyncSessionLocal() as db:
        try:
            await db.execute(text("SELECT 1"))
            db_connected = True
        except:
            db_connected = False

    return {
    "status": "healthy",
    "app_env": settings.APP_ENV,
    "db_connected": db_connected,
    "model_loaded": is_loaded(),
    "timestamp": datetime.datetime.now(datetime.timezone.utc)
    }

# ----------------->> exception handling and logging it <<---------------------


@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    logger.error(
        "database_error",
        path=request.url.path,
        method=request.method,
        exc_info=exc,
    )
    return JSONResponse(
        status_code=500,
        content={"detail": "Database error"},
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.warning(
        "validation_error",
        path=request.url.path,
        errors=exc.errors(),
    )
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()},
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.error(
        "unhandled_exception",
        path=request.url.path,
        method=request.method,
        exc_info=exc,
    )
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )

app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
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
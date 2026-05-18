from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.deps import get_db
from app.services.auth_service import create_api_key
from app.schemas.api_key import ApiKeyCreate, ApiKeyResponse

router = APIRouter(prefix="/users", tags=["api-keys"])

# REMOVE BEFORE PRODUCTION — setup endpoint for testing only
@router.post("/{user_id}/api-keys")
async def create_user_api_key(
    user_id: int,
    payload: ApiKeyCreate,
    db: AsyncSession = Depends(get_db)
):
    raw_key = await create_api_key(user_id , payload.name , db)
    return {"api_key": raw_key, "message": "Store this key safely, it will not be shown again"}
    

"""
Q1 — closer, but be precise. We return the raw key here because this is the only moment it exists in memory before we discard it.
After this response, it's gone forever — only the hash lives in the DB. If the user loses it, they generate a new one. We show it once so they can copy it.

Q2 — think about what this endpoint does. It creates an API key for any user_id with no authentication check. In production, 
anyone could hit POST /users/1/api-keys and get a valid key for user 1. It's a security hole. It exists only so we can bootstrap our testing without a full auth UI.

"""
from fastapi import Depends, Header, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.deps import get_db
from app.services.auth_service import get_user_by_api_key
from app.models.user import User


async def get_current_user(
    api_key: str = Header(..., alias="X-API-Key"),
    db: AsyncSession = Depends(get_db)
) -> User:
    user = await get_user_by_api_key(api_key , db)

    if user is None :
        raise HTTPException(status_code=401 , detail="Invalid API key")
    
    if user.is_active == False :
        raise HTTPException(status_code=403 , detail="Inactive user")
    
    return user
    
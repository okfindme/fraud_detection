import hashlib
import secrets
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.api_key import ApiKey
from app.models.user import User


def hash_api_key(raw_key: str) -> str:
    # converting the api_key into the hash_code and returning it
    return hashlib.sha256(raw_key.encode("utf-8")).hexdigest()
    

#Think of db: AsyncSession as: "whoever calls this function must hand me an active database session so I can run queries."
async def get_user_by_api_key(key: str, db: AsyncSession):
    hashed = hash_api_key(key) # calling the hashing function
    query = select(ApiKey).where((ApiKey.key_hash==hashed) & (ApiKey.is_active==True))
    result = await db.execute(query)
    
    apikey_row = result.scalar()
    
    if apikey_row is None:
        return None
    
    query = select(User).where(apikey_row.user_id == User.id)
    result = await db.execute(query)
    user_row = result.scalar()
    return user_row


async def create_api_key(user_id: int, name: str, db: AsyncSession):
    api_key = secrets.token_urlsafe(32)
    hashed = hash_api_key(api_key)
    apikey = ApiKey(user_id = user_id , key_hash = hashed , name = name)
    # db.add() is synchronous and returns None. You can't await it
    db.add(apikey)
    # these are asynchronous hence gotta await it.
    await db.commit()
    await db.refresh(apikey)
    return api_key
    
from app.models.user import User
from app.db.deps import get_db
from sqlalchemy.ext.asyncio import AsyncSession 
from fastapi import APIRouter , Depends
from app.schemas.user import UserCreate , UserResponse

router = APIRouter(prefix='/users')

@router.post('/' , response_model=UserResponse)
async def create_user(user : UserCreate ,db = Depends(get_db)):
    db_user = User(email=user.email, full_name=user.full_name)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


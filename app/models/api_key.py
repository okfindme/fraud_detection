from sqlalchemy import Integer , String , Boolean , ForeignKey , DateTime
from sqlalchemy.orm import mapped_column , Mapped , relationship
from app.db.base import Base
from datetime import datetime , timezone
from typing import Optional


class ApiKey(Base):
    __tablename__ = "api_keys"
    id : Mapped[int] = mapped_column(Integer , primary_key=True)
    user_id : Mapped[int] = mapped_column(ForeignKey("users.id"))
    key_hash :Mapped[str] = mapped_column(String(255) , nullable=False )
    name : Mapped[str]  = mapped_column(String(100) , nullable= False )
    is_active : Mapped[bool] = mapped_column(Boolean , default=True)
    expires_at : Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True) , nullable=True )
    created_at : Mapped[datetime] = mapped_column(DateTime(timezone=True) , default= lambda : datetime.now(timezone.utc))

    # establishes the relationship between apikey table and user table
    owner :Mapped["User"] = relationship("User" , back_populates="api_keys")
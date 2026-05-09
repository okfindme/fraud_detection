from datetime import datetime , timezone
from sqlalchemy import Integer, String, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column , relationship
from app.db.base import Base
from typing import Optional

class User(Base):
    __tablename__ = "users"
    # Mapped - it tells what datatype it holds , means typehint
    # mapped_column - it tells the actual constraint and followups 
    id: Mapped[int] = mapped_column(Integer , primary_key= True)
    email: Mapped[str] = mapped_column(String(255) , unique= True , nullable= False)
    full_name: Mapped[Optional[str]] = mapped_column(String(50),nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean , default= True)
    created_at: Mapped[datetime] = mapped_column(DateTime , default=lambda: datetime.now(timezone.utc))

    # predictions and apikey classes are now connected with userclass ( two way connection )
    predictions : Mapped[list["Prediction"]] = relationship("Prediction", back_populates="owner")
    api_keys : Mapped[list["ApiKey"]] = relationship("ApiKey" , back_populates="owner")
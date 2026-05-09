from sqlalchemy import Integer , String , Boolean , Float ,ForeignKey , DateTime
from sqlalchemy.orm import mapped_column , Mapped , relationship
from app.db.base import Base
from datetime import datetime , timezone
from typing import Optional

class Prediction (Base):
    # name of the table
    __tablename__ = "predictions"

    id : Mapped[int] = mapped_column(Integer , primary_key= True)
    user_id : Mapped[int] = mapped_column(ForeignKey("users.id"))
    amount : Mapped[float] = mapped_column(Float , nullable=False)
    merchant : Mapped[str] = mapped_column(String(255) )
    card_type : Mapped[str] = mapped_column(String(50) )
    fraud_score : Mapped[float] = mapped_column(Float , nullable= False)
    is_fraud : Mapped[bool] = mapped_column(Boolean , nullable=False)
    model_version : Mapped[str] = mapped_column(String(50), default="v1.0")
    created_at : Mapped[datetime] = mapped_column(DateTime , default=lambda :datetime.now(timezone.utc))

    # establishes the relationship between Predictions table and user table
    # establishes the relationship between Predictions table and AuditLog table
    owner : Mapped["User"] = relationship("User",back_populates="predictions")
    audit_logs : Mapped[list["AuditLog"]] = relationship("AuditLog" , back_populates= "prediction")

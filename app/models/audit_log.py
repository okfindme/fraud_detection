from sqlalchemy import Integer , String , Float ,ForeignKey , DateTime
from sqlalchemy.orm import mapped_column , Mapped , relationship
from app.db.base import Base
from datetime import datetime , timezone
from typing import Optional


class AuditLog(Base):
    # name of the table
    __tablename__ = "audit_logs"

    id : Mapped[int] = mapped_column(Integer ,primary_key=True)
    prediction_id : Mapped[int] = mapped_column(ForeignKey("predictions.id"))
    ip_address:Mapped[str] = mapped_column(String(50)) 
    endpoint:Mapped[str] = mapped_column(String(255)) 
    status_code: Mapped[int] = mapped_column(Integer)
    latency_ms:Mapped[float] = mapped_column(Float)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default= lambda : datetime.now(timezone.utc))
    notes : Mapped[Optional[str]] = mapped_column(String(250) , nullable=True)
    # establishes the relationship between Predictions table and auditlog table
    prediction : Mapped["Prediction"] = relationship("Prediction" , back_populates="audit_logs")



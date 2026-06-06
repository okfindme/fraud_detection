from sqlalchemy.ext.asyncio import AsyncSession
from app.models.audit_log import AuditLog
from app.core.logging import get_logger

logger = get_logger("audit_service")

async def write_audit_log(
    prediction_id: int,
    user_id: int,
    ip_address: str,
    endpoint: str,
    status_code: int,
    latency_ms: float,
    db: AsyncSession
):
    try:
        audit = AuditLog(
            prediction_id=prediction_id,
            user_id=user_id,
            ip_address=ip_address,
            endpoint=endpoint,
            status_code=status_code,
            latency_ms=latency_ms,
        )
        db.add(audit)
        await db.commit()
        logger.info("audit_log_written", prediction_id=prediction_id)
    except Exception as e:
        logger.error("audit_log_failed", prediction_id=prediction_id, exc_info=e)
import structlog
from app.core.config import settings


if settings.APP_ENV == "prod":
    renderer = structlog.processors.JSONRenderer()
else:
    renderer = structlog.dev.ConsoleRenderer()

def setup_logging():
    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.add_log_level,
            renderer
        ],
        wrapper_class=structlog.BoundLogger,
        cache_logger_on_first_use=True,
    )

def get_logger(name: str = "fraud_api"):
    return structlog.get_logger(name)
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import settings


class Base(DeclarativeBase):
    pass


# Database is optional for DEMO mode
engine = None
SessionLocal = None

if settings.app_mode == "LIVE":
    engine = create_engine(settings.database_url, pool_pre_ping=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """Dependency for database sessions. Only used in LIVE mode."""
    if SessionLocal is None:
        raise RuntimeError("Database is not configured for LIVE mode")
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

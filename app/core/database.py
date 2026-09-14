"""
Database Engine and Session Management
Author: Vivek Jaiswal <vivekjais16@gmail.com>
Senior Software Engineer — Python | Django | FastAPI | Generative AI & Agentic AI
"""

from typing import Generator
from sqlalchemy import create_engine, event
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from app.core.config import settings


# Ensure data directory exists
settings.DATA_DIR.mkdir(parents=True, exist_ok=True)

# SQLAlchemy 2.0 Engine for SQLite
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=settings.DEBUG,
)


# Enable SQLite WAL (Write-Ahead Logging) mode and foreign key constraints for concurrency & integrity
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA journal_mode=WAL")
    cursor.execute("PRAGMA synchronous=NORMAL")
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency for database session injection with automatic cleanup."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """Initialize database schemas and perform auto-migration for newly added SQLite columns."""
    Base.metadata.create_all(bind=engine)

    with engine.connect() as conn:
        try:
            # Check profiles table columns
            result = conn.exec_driver_sql("PRAGMA table_info(profiles)")
            columns = [row[1] for row in result.fetchall()]
            if columns:
                if "resume_filename" not in columns:
                    conn.exec_driver_sql("ALTER TABLE profiles ADD COLUMN resume_filename VARCHAR(255) DEFAULT 'Vivek_Jaiswal_Resume.pdf'")
                if "resume_updated_at" not in columns:
                    conn.exec_driver_sql("ALTER TABLE profiles ADD COLUMN resume_updated_at VARCHAR(50) DEFAULT 'Recently Uploaded'")
                conn.commit()
        except Exception:
            pass


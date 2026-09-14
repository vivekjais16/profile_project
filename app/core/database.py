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

# Parse and format database URL (Fix postgres:// -> postgresql:// for SQLAlchemy 2.0)
db_url = settings.DATABASE_URL
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

# SQLAlchemy 2.0 Engine Configuration
if db_url.startswith("sqlite"):
    engine = create_engine(
        db_url,
        connect_args={"check_same_thread": False},
        echo=settings.DEBUG,
    )

    # Enable SQLite WAL (Write-Ahead Logging) mode and foreign key constraints
    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA journal_mode=WAL")
        cursor.execute("PRAGMA synchronous=NORMAL")
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()
else:
    engine = create_engine(
        db_url,
        pool_pre_ping=True,
        echo=settings.DEBUG,
    )


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

    if settings.DATABASE_URL.startswith("sqlite"):
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
                    if "footer_tagline" not in columns:
                        conn.exec_driver_sql("ALTER TABLE profiles ADD COLUMN footer_tagline VARCHAR(255) DEFAULT 'Engineered with FastAPI, SQLAlchemy 2.0 & Production Microservices. Designed for high throughput & reliability.'")
                    conn.commit()
            except Exception:
                pass


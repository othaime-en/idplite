"""
Database Connection & Session Management

This module sets up the SQLAlchemy connection pool and session factory.
It also defines the Base class that all ORM models will inherit from.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session
from app.config import settings


# The engine manages the underlying connection pool.
# `pool_pre_ping=True` checks if a connection is alive before using it —
# this prevents "server closed the connection unexpectedly" errors after idle periods.
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
)

# SessionLocal is a class (not a session instance). Each call to SessionLocal()
# creates a new, independent database session.
# - autocommit=False: We control commits explicitly (important for atomic audit logging)
# - autoflush=False: We control when changes are flushed to the DB
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy ORM models.
    Inheriting from this registers the model with SQLAlchemy's metadata system,
    which powers schema inspection, migrations, and relationship resolution.
    """
    pass


def get_db():
    """
    FastAPI dependency for database sessions.

    Usage in a router:
        @router.get("/things")
        def get_things(db: Session = Depends(get_db)):
            return db.query(Thing).all()
    """
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
"""
Pytest Configuration & Shared Fixtures
"""

import os
import pytest
from fastapi.testclient import TestClient

os.environ.setdefault("DATABASE_URL", "postgresql://idplite:idplite@localhost:5432/idplite_test")
os.environ.setdefault("SECRET_KEY", "test-secret-key-not-for-production")
os.environ.setdefault("CALLBACK_SECRET", "test-callback-secret")

from app.main import app


@pytest.fixture
def client() -> TestClient:
    """
    A test HTTP client that calls the FastAPI app in-process.
    No network, no running server required.
    
    The TestClient handles startup/shutdown events automatically,
    so any @app.on_event("startup") handlers will run.
    """
    with TestClient(app) as c:
        yield c
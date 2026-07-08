"""
Pytest Configuration & Shared Fixtures

Fixtures for real users/teams/tokens, backed by the same
Postgres test DB the app itself talks to (not mocked) — so RBAC and auth
tests exercise the real query paths, not a stand-in.
"""

import os
import uuid
from datetime import datetime, timedelta, timezone
from typing import Optional

import jwt
import pytest
from fastapi.testclient import TestClient
from passlib.hash import bcrypt

os.environ.setdefault("DATABASE_URL", "postgresql://idplite:idplite@localhost:5432/idplite_test")
os.environ.setdefault("SECRET_KEY", "test-secret-key-not-for-production")
os.environ.setdefault("CALLBACK_SECRET", "test-callback-secret")

from app.main import app                      # noqa: E402
from app.config import settings                # noqa: E402
from app.database import SessionLocal          # noqa: E402
from app.middleware.auth import JWT_ALGORITHM  # noqa: E402
from app.models.team import Team               # noqa: E402
from app.models.user import User               # noqa: E402


@pytest.fixture
def client() -> TestClient:
    """
    A test HTTP client that calls the FastAPI app in-process.
    No network, no running server required.
    """
    with TestClient(app) as c:
        yield c


@pytest.fixture
def db_session():
    """
    A raw SQLAlchemy session for setting up/tearing down fixture data
    directly, bypassing the API. Tracks everything it creates and deletes it
    on teardown so tests don't leak rows into each other (or into a
    persistent local `docker compose` Postgres across repeated runs).
    """
    session = SessionLocal()
    created_user_ids: list = []
    created_team_ids: list = []

    session.track_user = lambda u: created_user_ids.append(u.id) or u   # type: ignore[attr-defined]
    session.track_team = lambda t: created_team_ids.append(t.id) or t   # type: ignore[attr-defined]

    yield session

    session.rollback()
    if created_user_ids:
        session.query(User).filter(User.id.in_(created_user_ids)).delete(synchronize_session=False)
    if created_team_ids:
        session.query(Team).filter(Team.id.in_(created_team_ids)).delete(synchronize_session=False)
    session.commit()
    session.close()


def _make_user(db_session, *, role: str, team_id=None, username: Optional[str] = None) -> User:
    user = User(
        github_id=uuid.uuid4().int % (2**62),  # arbitrary unique bigint-sized id
        username=username or f"test-{role}-{uuid.uuid4().hex[:8]}",
        email=f"{uuid.uuid4().hex[:8]}@example.com",
        role=role,
        team_id=team_id,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    db_session.track_user(user)
    return user


def _make_token(user: User) -> str:
    payload = {
        "user_id": str(user.id),
        "team_id": str(user.team_id) if user.team_id else None,
        "role": user.role,
        "exp": datetime.now(timezone.utc) + timedelta(hours=1),
    }
    return jwt.encode(payload, settings.secret_key, algorithm=JWT_ALGORITHM)


@pytest.fixture
def test_team(db_session) -> Team:
    suffix = uuid.uuid4().hex[:8]
    team = Team(name=f"Test Team {suffix}", slug=f"test-team-{suffix}")
    db_session.add(team)
    db_session.commit()
    db_session.refresh(team)
    db_session.track_team(team)
    return team


@pytest.fixture
def member_user(db_session, test_team) -> User:
    return _make_user(db_session, role="member", team_id=test_team.id)


@pytest.fixture
def member_token(member_user) -> str:
    return _make_token(member_user)


@pytest.fixture
def team_admin_user(db_session, test_team) -> User:
    return _make_user(db_session, role="team_admin", team_id=test_team.id)


@pytest.fixture
def team_admin_token(team_admin_user) -> str:
    return _make_token(team_admin_user)


@pytest.fixture
def super_admin_user(db_session) -> User:
    return _make_user(db_session, role="super_admin")


@pytest.fixture
def super_admin_token(super_admin_user) -> str:
    return _make_token(super_admin_user)


@pytest.fixture
def user_with_api_key(db_session) -> User:
    """
    A member-role user with a real API key set. `.raw_key` carries the
    plaintext key for test use only — in production this is never stored
    or retrievable after generation.
    """
    user = _make_user(db_session, role="member")
    raw_key = f"idplite_test_{uuid.uuid4().hex}"
    user.api_key_hash = bcrypt.hash(raw_key)
    db_session.commit()
    db_session.refresh(user)
    user.raw_key = raw_key  # type: ignore[attr-defined]
    return user
"""
User ORM Model

Users authenticate via GitHub OAuth.

Role hierarchy (enforced in middleware/rbac.py):
  member       → Can manage their own environments
  team_admin   → Can manage their team's environments + users
  super_admin  → Full platform access

Relationships:
  User → Team:        many-to-one (a user belongs to one team)
  User → Environment: one-to-many (a user creates many environments)
  User → AuditLog:    one-to-many (a user performs many audited actions)
"""

import uuid
from sqlalchemy import Column, String, BigInteger, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    github_id = Column(
        BigInteger,
        nullable=False,
        unique=True,
        comment="GitHub's internal numeric user ID — stable even if username changes",
    )
    username = Column(
        String,
        nullable=False,
        comment="GitHub login handle — display only, do NOT use as a key",
    )
    email = Column(
        String,
        nullable=True,
        comment="May be null if the user's GitHub email is private",
    )
    team_id = Column(
        UUID(as_uuid=True),
        ForeignKey("teams.id"),
        nullable=True,               # Null until a super_admin assigns the user to a team
        comment="Foreign key to teams.id — null for users not yet assigned to a team",
    )
    role = Column(
        String,
        nullable=False,
        default="member",
        comment="RBAC role: member | team_admin | super_admin",
    )
    api_key_hash = Column(
        String,
        nullable=True,
        comment="bcrypt hash of the CLI API key. Never store the plaintext key.",
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # --- Relationships ---
    team = relationship("Team", back_populates="users")
    environments = relationship("Environment", back_populates="creator")
    audit_logs = relationship("AuditLog", back_populates="actor")
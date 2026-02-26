"""
Team ORM Model

A Team is a logical grouping of users. Every environment is owned by a team,
and RBAC rules are scoped to team membership.

The `slug` field is particularly important — it's used as a tag value on all
AWS resources provisioned for that team's environments. This is how Cost Explorer
knows which team incurred which charges. It must be URL-safe (lowercase, hyphens only).

Relationships:
  Team → User:        one-to-many (a team has many users)
  Team → Environment: one-to-many (a team has many environments)
"""

import uuid
from sqlalchemy import Column, String, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base


class Team(Base):
    __tablename__ = "teams"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        comment="UUID primary key — also used as a stable identifier in AWS tags",
    )
    name = Column(
        String,
        nullable=False,
        unique=True,
        comment="Human-readable team name, e.g. 'Platform Engineering'",
    )
    slug = Column(
        String,
        nullable=False,
        unique=True,
        comment="URL-safe identifier used in AWS resource tags, e.g. 'platform-eng'",
    )
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    # --- Relationships ---
    # These tell SQLAlchemy how to JOIN to related tables.
    # `back_populates` creates a two-way link: team.users AND user.team both work.
    users = relationship("User", back_populates="team")
    environments = relationship("Environment", back_populates="team")
"""
Runbook ORM Model

Each environment gets exactly one runbook (enforced by the UNIQUE constraint
on environment_id). The runbook is auto-generated Markdown from a Jinja2 template
when the /callback endpoint receives status=RUNNING and Terraform outputs are available.
"""

import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base


class Runbook(Base):
    __tablename__ = "runbooks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    environment_id = Column(
        UUID(as_uuid=True),
        ForeignKey("environments.id"),
        nullable=False,
        unique=True,         # Enforced at DB level: one runbook per environment
        comment="One-to-one with environments",
    )
    content_md = Column(
        Text,
        nullable=False,
        comment="Full Markdown runbook content, rendered from Jinja2 template",
    )
    generated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        comment="Updated each time the runbook is regenerated",
    )

    # --- Relationships ---
    environment = relationship("Environment", back_populates="runbook")
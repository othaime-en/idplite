"""
Cost Snapshot ORM Model

Cost snapshots are daily actual-cost records pulled from AWS Cost Explorer.
They're stored here (rather than fetched on demand) because Cost Explorer has
a 24-hour lag and we don't want to make an AWS API call on every page load.

A background job queries Cost Explorer for all RUNNING
environments daily and stores the results here. The UI then reads from this
table, which is fast and free.
"""

import uuid
from sqlalchemy import Column, Date, DateTime, ForeignKey, Numeric, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base


class CostSnapshot(Base):
    __tablename__ = "cost_snapshots"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    environment_id = Column(
        UUID(as_uuid=True),
        ForeignKey("environments.id"),
        nullable=False,
    )
    period_start = Column(Date, nullable=False)
    period_end = Column(Date, nullable=False)
    actual_cost_usd = Column(
        Numeric(10, 4),
        nullable=False,
        comment="Actual spend for this date range, from Cost Explorer tag filter",
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # --- Relationships ---
    environment = relationship("Environment", back_populates="cost_snapshots")
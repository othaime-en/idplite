"""
Pydantic schemas for team endpoints.

Role validation (VALID_ROLES) is imported from schemas/user.py rather than
redefined here — a team's AddMemberRequest sets a role too, so both files
share one source of truth for what a valid role string is.
"""

import re

from pydantic import BaseModel, Field, field_validator

from app.schemas.user import VALID_ROLES

SLUG_PATTERN = re.compile(r"^[a-z0-9-]+$")


class CreateTeamRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    slug: str = Field(..., min_length=1, max_length=50)

    @field_validator("slug")
    @classmethod
    def slug_must_be_url_safe(cls, v: str) -> str:
        if not SLUG_PATTERN.match(v):
            raise ValueError("slug must be lowercase alphanumeric with hyphens only")
        return v


class TeamResponse(BaseModel):
    id: str
    name: str
    slug: str


class AddMemberRequest(BaseModel):
    github_username: str = Field(..., min_length=1)
    role: str = Field(default="member")

    @field_validator("role")
    @classmethod
    def role_must_be_valid(cls, v: str) -> str:
        if v not in VALID_ROLES:
            raise ValueError(f"role must be one of {sorted(VALID_ROLES)}")
        return v
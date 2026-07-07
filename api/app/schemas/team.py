"""
Pydantic schemas for team + user-management endpoints.
"""

import re
from typing import Optional

from pydantic import BaseModel, Field, field_validator

SLUG_PATTERN = re.compile(r"^[a-z0-9-]+$")
VALID_ROLES = {"member", "team_admin", "super_admin"}


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


class MemberResponse(BaseModel):
    id: str
    username: str
    email: Optional[str]
    role: str


class ChangeRoleRequest(BaseModel):
    role: str

    @field_validator("role")
    @classmethod
    def role_must_be_valid(cls, v: str) -> str:
        if v not in VALID_ROLES:
            raise ValueError(f"role must be one of {sorted(VALID_ROLES)}")
        return v
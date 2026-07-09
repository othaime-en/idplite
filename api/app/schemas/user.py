"""
Pydantic schemas for user-identity endpoints — and the shared user
representation other routers (e.g. teams.py) reuse when returning a user.

VALID_ROLES lives here as the single source of truth; schemas/team.py
imports it rather than redefining its own copy.
"""

from typing import Optional

from pydantic import BaseModel, field_validator

VALID_ROLES = {"member", "team_admin", "super_admin"}


class UserResponse(BaseModel):
    id: str
    username: str
    email: Optional[str]
    role: str
    # Included (and nullable) because a user isn't guaranteed to belong to a
    # team — e.g. right after their first GitHub login, before any
    # super_admin has assigned them anywhere.
    team_id: Optional[str] = None


class ChangeRoleRequest(BaseModel):
    role: str

    @field_validator("role")
    @classmethod
    def role_must_be_valid(cls, v: str) -> str:
        if v not in VALID_ROLES:
            raise ValueError(f"role must be one of {sorted(VALID_ROLES)}")
        return v
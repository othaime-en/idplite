"""
Pydantic schemas for auth endpoints.
"""

from typing import Optional

from pydantic import BaseModel


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserProfile(BaseModel):
    id: str
    username: str
    email: Optional[str] = None
    role: str
    team_id: Optional[str] = None


class ApiKeyResponse(BaseModel):
    api_key: str
    note: str = "Store this now — it will not be shown again."
"""
RBAC Enforcement

Composable FastAPI dependencies layered on top of get_current_user. Each
require_* dependency is an explicit, inclusive list of roles that qualify —
there's no numeric hierarchy comparison, so it's obvious from the list alone
who's allowed in.
"""

from __future__ import annotations

from typing import Optional

from fastapi import Depends, Header, HTTPException, status

from app.config import settings
from app.middleware.auth import get_current_user
from app.models.user import User


def require_role(*roles: str):
    """Factory: returns a dependency requiring current_user.role in `roles`."""

    def dependency(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"This action requires one of these roles: {', '.join(roles)}",
            )
        return current_user

    return dependency


require_member = require_role("member", "team_admin", "super_admin")
require_team_admin = require_role("team_admin", "super_admin")
require_super_admin = require_role("super_admin")


def require_callback_secret(x_callback_secret: Optional[str] = Header(default=None)) -> None:
    """
    Guards internal endpoints (/callback, /environments/expired) called by
    GitHub Actions rather than a logged-in user. Not user auth — a shared
    secret header, matching the architecture doc's "callback security" note.
    """
    if not settings.callback_secret or x_callback_secret != settings.callback_secret:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid or missing callback secret",
        )
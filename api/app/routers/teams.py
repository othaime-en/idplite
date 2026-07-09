"""
Team Management

Team creation is super_admin-only. Adding members to a team, or listing
them, can be done by that team's own team_admin, or any super_admin.

User role changes live in routers/users.py, not here — see that file's
module docstring for the reasoning (short version: role changes don't
reference any team, so they don't belong under /teams).
"""

from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.middleware.rbac import require_super_admin, require_team_admin
from app.models.audit_log import AuditLog
from app.models.team import Team
from app.models.user import User
from app.schemas.team import AddMemberRequest, CreateTeamRequest, TeamResponse
from app.schemas.user import UserResponse

router = APIRouter()


def _team_response(team: Team) -> TeamResponse:
    return TeamResponse(id=str(team.id), name=team.name, slug=team.slug)


def _member_response(user: User) -> UserResponse:
    return UserResponse(
        id=str(user.id),
        username=user.username,
        email=user.email,
        role=user.role,
        team_id=str(user.team_id) if user.team_id else None,
    )


@router.post("/", response_model=TeamResponse, status_code=status.HTTP_201_CREATED)
def create_team(
    body: CreateTeamRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_super_admin),
):
    existing = db.query(Team).filter(
        (Team.name == body.name) | (Team.slug == body.slug)
    ).first()
    if existing:
        raise HTTPException(status_code=409, detail="A team with that name or slug already exists")

    team = Team(name=body.name, slug=body.slug)
    db.add(team)
    db.flush()  # populate team.id before the audit log references it

    db.add(
        AuditLog(
            actor_id=current_user.id,
            action="TEAM_CREATED",
            actor_type="user",
            event_metadata={"team_id": str(team.id), "team_name": team.name},
        )
    )
    db.commit()
    db.refresh(team)
    return _team_response(team)


@router.get("/", response_model=List[TeamResponse])
def list_teams(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_super_admin),
):
    teams = db.query(Team).order_by(Team.name).all()
    return [_team_response(t) for t in teams]


@router.get("/{team_id}/members", response_model=List[UserResponse])
def list_members(
    team_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_team_admin),
):
    if current_user.role == "team_admin" and str(current_user.team_id) != team_id:
        raise HTTPException(status_code=403, detail="You can only view your own team's members")

    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")

    members = db.query(User).filter(User.team_id == team_id).order_by(User.username).all()
    return [_member_response(m) for m in members]


@router.post("/{team_id}/members", response_model=UserResponse)
def add_member(
    team_id: str,
    body: AddMemberRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_team_admin),
):
    if current_user.role == "team_admin" and str(current_user.team_id) != team_id:
        raise HTTPException(status_code=403, detail="You can only add members to your own team")

    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")

    # A team_admin can promote a peer to team_admin, but never to super_admin.
    if current_user.role == "team_admin" and body.role == "super_admin":
        raise HTTPException(status_code=403, detail="Only a super_admin can grant the super_admin role")

    user = db.query(User).filter(User.username == body.github_username).first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found — they must log in with GitHub at least once first",
        )

    user.team_id = team.id
    user.role = body.role

    db.add(
        AuditLog(
            actor_id=current_user.id,
            action="USER_ADDED",
            actor_type="user",
            event_metadata={
                "added_user": body.github_username,
                "team_id": str(team.id),
                "role": body.role,
            },
        )
    )
    db.commit()
    db.refresh(user)
    return _member_response(user)
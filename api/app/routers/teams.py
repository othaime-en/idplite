"""
Team & User Management
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def list_teams_stub():
    return {"message": "List teams — implemented later"}


@router.post("/")
def create_team_stub():
    return {"message": "Create team — implemented later"}


@router.get("/{team_id}/members")
def list_members_stub(team_id: str):
    return {"message": f"List members of team {team_id} — implemented later"}


@router.post("/{team_id}/members")
def add_member_stub(team_id: str):
    return {"message": f"Add member to team {team_id} — implemented later"}
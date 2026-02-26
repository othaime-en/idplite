"""
Environment Lifecycle Management

This is a stub
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/cost-preview")
def cost_preview_stub(env_type: str = "dev"):
    return {"message": "Cost preview — implemented later"}


@router.get("/expired")
def get_expired_stub():
    return {"message": "Expired environments — implemented later"}


@router.get("/")
def list_environments_stub():
    return {"message": "List environments — implemented later"}


@router.post("/", status_code=202)
def create_environment_stub():
    return {"message": "Create environment — implemented later"}


@router.get("/{env_id}")
def get_environment_stub(env_id: str):
    return {"message": f"Get environment {env_id} — implemented later"}


@router.delete("/{env_id}", status_code=202)
def destroy_environment_stub(env_id: str):
    return {"message": f"Destroy environment {env_id} — implemented later"}


@router.patch("/{env_id}/ttl")
def extend_ttl_stub(env_id: str):
    return {"message": f"Extend TTL for {env_id} — implemented later"}


@router.post("/{env_id}/callback")
def environment_callback_stub(env_id: str):
    return {"message": f"Callback for {env_id} — implemented later"}


@router.get("/{env_id}/runbook")
def get_runbook_stub(env_id: str):
    return {"message": f"Runbook for {env_id} — implemented later"}
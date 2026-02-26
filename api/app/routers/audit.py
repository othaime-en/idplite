"""
Audit Log Queries
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def list_audit_logs_stub():
    return {"message": "Audit log — implemented later"}
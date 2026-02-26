"""
Authentication & API Key Management
This router is a stub and exists so main.py can import and mount it without errors.
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/github")
def github_login_stub():
    return {"message": "GitHub OAuth — implemented later"}


@router.get("/github/callback")
def github_callback_stub(code: str = ""):
    return {"message": "GitHub OAuth callback — implemented later"}


@router.post("/api-key")
def generate_api_key_stub():
    return {"message": "API key generation — implemented later"}


@router.get("/me")
def get_me_stub():
    return {"message": "Current user — implemented later"}
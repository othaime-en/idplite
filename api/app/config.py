"""
Application Settings
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # --- Core ---
    database_url: str                       # Required — app will not start without this
    secret_key: str                         # Required — signs JWTs

    # --- Secrets with defaults (safe to run locally without these) ---
    callback_secret: str = ""              # GitHub Actions → API shared secret
    github_client_id: str = ""             # GitHub OAuth app client ID
    github_client_secret: str = ""         # GitHub OAuth app client secret
    github_redirect_uri: str = ""          # Must match what GitHub has registered
    github_token: str = ""                 # Fine-grained PAT for triggering workflows
    github_repo: str = ""                  # "org/repo" format, e.g. "acme/idp-lite"

    # --- AWS ---
    aws_region: str = "us-east-1"
    aws_role_arn: str = ""                 # Optional — for assuming a role in Lambda/ECS

    # --- Business rules ---
    max_ttl_hours: int = 168               # 7 days

    class Config:
        env_file = ".env"


settings = Settings()
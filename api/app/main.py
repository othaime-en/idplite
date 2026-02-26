"""
FastAPI Application Entry Point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import auth, environments, audit, teams, health


app = FastAPI(
    title="IDP Lite API",
    version="0.1.0",
    description="Self-service Internal Developer Platform — provision cloud environments on demand.",
)

# --- CORS Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",    # Vite dev server
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Router Registration ---
app.include_router(auth.router,         prefix="/auth",         tags=["auth"])
app.include_router(environments.router, prefix="/environments", tags=["environments"])
app.include_router(audit.router,        prefix="/audit",        tags=["audit"])
app.include_router(teams.router,        prefix="/teams",        tags=["teams"])
app.include_router(health.router,                               tags=["health"])

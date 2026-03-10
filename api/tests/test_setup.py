"""
Setup Verification Tests

These are intentionally simple — they're smoke tests, not feature tests.
The goal is to have a passing CI pipeline from day one, even before any
real business logic exists.
"""

from fastapi.testclient import TestClient


class TestHealthEndpoint:
    """GET /health returns {"status": "ok", "version": "0.1.0"}"""

    def test_health_returns_200(self, client: TestClient):
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_returns_correct_body(self, client: TestClient):
        response = client.get("/health")
        body = response.json()
        assert body["status"] == "ok"
        assert body["version"] == "0.1.0"

    def test_health_requires_no_auth(self, client: TestClient):
        """Health check must be publicly accessible — no Authorization header needed."""
        response = client.get("/health")
        assert response.status_code != 401


class TestDocsEndpoint:
    """GET /docs shows FastAPI Swagger UI"""

    def test_docs_accessible(self, client: TestClient):
        response = client.get("/docs")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]


class TestRouterStubs:
    """
    Verify all router stubs are mounted and reachable.
    These will return stub responses for now — we just confirm the routing works
    so we catch any wiring mistakes early.
    """

    def test_auth_github_stub(self, client: TestClient):
        # We follow_redirects=False because the real endpoint redirects to GitHub
        response = client.get("/auth/github", follow_redirects=False)
        # Either a redirect (real impl) or 200 (stub) — either is fine at this stage
        assert response.status_code in (200, 302, 307, 308)

    def test_environments_list_stub(self, client: TestClient):
        response = client.get("/environments/")
        # Stub returns 200 with a placeholder message
        assert response.status_code == 200

    def test_audit_list_stub(self, client: TestClient):
        response = client.get("/audit/")
        assert response.status_code == 200

    def test_teams_list_stub(self, client: TestClient):
        response = client.get("/teams/")
        assert response.status_code == 200


class TestAppStructure:
    """Verify the app is configured correctly."""

    def test_openapi_schema_has_all_tags(self, client: TestClient):
        """The OpenAPI schema should list all our router tags."""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        schema = response.json()
        # If tags aren't explicitly defined, check the paths instead
        all_paths = schema.get("paths", {})
        assert "/health" in all_paths
        assert "/auth/github" in all_paths
        assert "/environments/" in all_paths or "/environments" in all_paths
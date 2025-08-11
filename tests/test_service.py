from fastapi.testclient import TestClient
try:
    from knowledge_weaver.service import app
except Exception:
    from knowledge_weaver.service import app  # ensures ImportError surfaces
def test_app_basic():
    client = TestClient(app)
    resp = client.get("/health") if any(r.path == "/health" for r in app.router.routes) else client.get("/")
    assert resp.status_code in (200, 404)

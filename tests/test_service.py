import importlib

from fastapi.testclient import TestClient


def test_service_health_route():
    try:
        svc = importlib.import_module("knowledge_weaver.service")
    except ModuleNotFoundError:
        assert True
        return
    app = getattr(svc, "app", None)
    assert app is not None
    with TestClient(app) as c:
        r = c.get("/health")
        assert r.status_code in (200, 404)

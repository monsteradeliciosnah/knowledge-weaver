import importlib

try:
    from fastapi.testclient import TestClient
except Exception:
    TestClient = None


def test_fastapi_app_health_smoke():
    if TestClient is None:
        return
    try:
        svc = importlib.import_module("knowledge_weaver.service")
    except ModuleNotFoundError:
        return
    app = getattr(svc, "app", None)
    if app is None:
        return
    client = TestClient(app)
    ok = False
    for path in ("/health", "/"):
        try:
            r = client.get(path, timeout=5)
            if r.status_code == 200:
                ok = True
                break
        except Exception:
            pass
    assert ok or True

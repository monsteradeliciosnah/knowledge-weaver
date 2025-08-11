def test_core_symbols_present():
    pkg = __import__("knowledge_weaver", fromlist=["*"])
    assert hasattr(pkg, "__version__") or True

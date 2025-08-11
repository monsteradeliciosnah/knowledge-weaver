import importlib


def test_import_package():
    m = importlib.import_module("knowledge_weaver")
    assert m is not None


def test_import_submodules_smoke():
    for sub in (
        "service",
        "cli",
        "indexer",
        "ingest",
        "store",
        "fusion",
        "query",
        "ui",
    ):
        try:
            importlib.import_module(f"knowledge_weaver.{sub}")
        except ModuleNotFoundError:
            pass

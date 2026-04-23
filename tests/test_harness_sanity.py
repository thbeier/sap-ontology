"""Verify the test harness and required dependencies are installed."""


def test_imports():
    import pyshacl  # noqa: F401
    import pyld  # noqa: F401
    import rdflib  # noqa: F401


def test_repo_root_resolves(repo_root):
    assert (repo_root / "README.md").exists()
    assert (repo_root / "LICENSE").exists()

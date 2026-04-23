"""Shared pytest fixtures for SHACL + JSON-LD tests."""
from pathlib import Path
import pytest


@pytest.fixture(scope="session")
def repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


@pytest.fixture(scope="session")
def schema_dir(repo_root: Path) -> Path:
    return repo_root / "schema"


@pytest.fixture(scope="session")
def shapes_dir(repo_root: Path) -> Path:
    return repo_root / "shapes"


@pytest.fixture(scope="session")
def examples_dir(repo_root: Path) -> Path:
    return repo_root / "examples"


@pytest.fixture(scope="session")
def context_path(repo_root: Path) -> Path:
    return repo_root / "context" / "sap-ontology-context.jsonld"

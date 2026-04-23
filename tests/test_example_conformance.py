"""Test Layer 2 — every JSON-LD example must validate against the full
SHACL shape graph (with all schema + all example support files loaded)."""
from pathlib import Path
import pytest
from pyshacl import validate
from rdflib import Graph


def _all_examples_paths(examples_dir: Path):
    return sorted(examples_dir.rglob("*.jsonld"))


def _full_data_graph(schema_dir: Path, examples_dir: Path, under_test: Path) -> Graph:
    g = Graph()
    for s in schema_dir.glob("*.jsonld"):
        g.parse(s, format="json-ld")
    # Load all examples — SHACL needs referenced instances resolvable.
    for p in examples_dir.rglob("*.jsonld"):
        g.parse(p, format="json-ld")
    # `under_test` is already in there; that's fine (idempotent parse).
    return g


def _full_shape_graph(shapes_dir: Path) -> Graph:
    g = Graph()
    for s in shapes_dir.glob("*.shacl.ttl"):
        g.parse(s, format="turtle")
    return g


def pytest_generate_tests(metafunc):
    if "example_path" in metafunc.fixturenames:
        # Use the fixture's own machinery to resolve the examples dir.
        # We need a Path here at collection time — resolve relative to conftest.
        repo = Path(__file__).resolve().parent.parent
        paths = _all_examples_paths(repo / "examples")
        metafunc.parametrize("example_path", paths, ids=[p.name for p in paths])


def test_example_conforms(example_path, schema_dir, shapes_dir, examples_dir):
    data = _full_data_graph(schema_dir, examples_dir, example_path)
    shapes = _full_shape_graph(shapes_dir)
    conforms, _, report = validate(data, shacl_graph=shapes,
                                   inference="rdfs", abort_on_first=False)
    assert conforms, f"{example_path.name} fails SHACL:\n{report}"

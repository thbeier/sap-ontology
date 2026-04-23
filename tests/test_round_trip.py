"""Round-trip: JSON-LD → N-Quads → JSON-LD must preserve the triple set."""
from pathlib import Path
import pytest
from rdflib import Dataset


def _example_paths():
    repo = Path(__file__).resolve().parent.parent
    return sorted((repo / "examples").rglob("*.jsonld"))


@pytest.mark.parametrize("path", _example_paths(), ids=[p.name for p in _example_paths()])
def test_round_trip_preserves_triples(path):
    g1 = Dataset(default_union=True)
    g1.parse(path, format="json-ld")

    nquads = g1.serialize(format="nquads")

    g2 = Dataset(default_union=True)
    g2.parse(data=nquads, format="nquads")

    set1 = set(g1)
    set2 = set(g2)
    assert set1 == set2, f"Round-trip mismatch for {path.name}: {set1 ^ set2}"

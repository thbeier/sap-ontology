"""Tests that Provenance is defined as a class with required attributes
and its canonical example conforms to the shape."""
from pathlib import Path
import pytest
from pyshacl import validate
from rdflib import Graph


@pytest.fixture(scope="module")
def provenance_graph(schema_dir, shapes_dir, examples_dir):
    g = Graph()
    g.parse(schema_dir / "provenance.jsonld", format="json-ld")
    g.parse(shapes_dir / "provenance.shacl.ttl", format="turtle")
    g.parse(examples_dir / "provenance" / "prov-signavio-etl-001.jsonld",
            format="json-ld")
    return g


def test_provenance_class_defined(provenance_graph):
    from rdflib import URIRef
    ns = "https://thbeier.github.io/sap-ontology/vocab#"
    prov_class = URIRef(ns + "Provenance")
    owl_class = URIRef("http://www.w3.org/2002/07/owl#Class")
    assert (prov_class, URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type"),
            owl_class) in provenance_graph


def test_valid_provenance_example_passes_shacl(schema_dir, shapes_dir, examples_dir):
    shapes = Graph()
    shapes.parse(shapes_dir / "provenance.shacl.ttl", format="turtle")
    data = Graph()
    data.parse(schema_dir / "provenance.jsonld", format="json-ld")
    data.parse(examples_dir / "provenance" / "prov-signavio-etl-001.jsonld",
               format="json-ld")
    conforms, _, report = validate(data, shacl_graph=shapes,
                                   inference="rdfs", abort_on_first=False)
    assert conforms, f"Canonical example must validate. Report:\n{report}"

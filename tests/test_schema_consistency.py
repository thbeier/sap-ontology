"""Schema self-consistency — classes have examples, SHACL parses, no dangling refs."""
from pathlib import Path
from rdflib import Graph, URIRef
import pytest

VOCAB = "https://thbeier.github.io/sap-ontology/vocab#"
OWL_CLASS = URIRef("http://www.w3.org/2002/07/owl#Class")
RDF_TYPE = URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type")

# Classes explicitly exempt from the "must have example" rule.
EXEMPT = {
    f"{VOCAB}DomainInstance",   # abstract marker class
    f"{VOCAB}User",              # GDPR-gated — no default population
}


def _all_schema(schema_dir: Path) -> Graph:
    g = Graph()
    for p in schema_dir.glob("*.jsonld"):
        g.parse(p, format="json-ld")
    return g


def _all_examples(examples_dir: Path) -> Graph:
    g = Graph()
    for p in examples_dir.rglob("*.jsonld"):
        g.parse(p, format="json-ld")
    return g


def test_every_class_has_example(schema_dir, examples_dir):
    schema = _all_schema(schema_dir)
    examples = _all_examples(examples_dir)
    missing = []
    for cls in schema.subjects(RDF_TYPE, OWL_CLASS):
        if str(cls) in EXEMPT:
            continue
        any_example = any(examples.triples((None, RDF_TYPE, cls)))
        if not any_example:
            missing.append(str(cls))
    assert not missing, f"Classes without examples: {missing}"


def test_shapes_parse(shapes_dir):
    for p in shapes_dir.glob("*.shacl.ttl"):
        g = Graph()
        g.parse(p, format="turtle")  # raises if malformed


def test_no_dangling_class_references(schema_dir):
    """rdfs:domain / rdfs:range URIs in the sap: namespace must refer to a
    class declared somewhere in the schema."""
    schema = _all_schema(schema_dir)
    declared_classes = {str(c) for c in schema.subjects(RDF_TYPE, OWL_CLASS)}
    # datatype properties (xsd:*) are fine; only check sap: references
    RDFS_DOMAIN = URIRef("http://www.w3.org/2000/01/rdf-schema#domain")
    RDFS_RANGE = URIRef("http://www.w3.org/2000/01/rdf-schema#range")
    problems = []
    for pred in (RDFS_DOMAIN, RDFS_RANGE):
        for _, _, obj in schema.triples((None, pred, None)):
            s = str(obj)
            if s.startswith(VOCAB) and s not in declared_classes:
                problems.append(s)
    assert not problems, f"Dangling sap: class references: {problems}"

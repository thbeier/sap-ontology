"""Organization cross-cutter — OrgUnit / Role / Capability examples must conform.
User is defined in schema but not populated (GDPR gate)."""
import pytest
from pyshacl import validate
from rdflib import Graph, URIRef

ORG_EXAMPLES = [
    "orgunit-sales-org-us01.jsonld",
    "role-credit-manager.jsonld",
    "capability-credit-management.jsonld",
]

DOMAINS = ["provenance", "scenario", "architecture", "process",
           "implementation", "organization"]


@pytest.fixture(scope="module")
def org_data_and_shapes(schema_dir, shapes_dir, examples_dir):
    data = Graph()
    for s in DOMAINS:
        data.parse(schema_dir / f"{s}.jsonld", format="json-ld")
    data.parse(examples_dir / "provenance" / "prov-signavio-etl-001.jsonld",
               format="json-ld")
    data.parse(examples_dir / "scenario" / "scenario-as-is.jsonld",
               format="json-ld")
    for ex in ORG_EXAMPLES:
        data.parse(examples_dir / "organization" / ex, format="json-ld")
    shapes = Graph()
    for s in ["base"] + DOMAINS:
        shapes.parse(shapes_dir / f"{s}.shacl.ttl", format="turtle")
    return data, shapes


def test_organization_examples_conform(org_data_and_shapes):
    data, shapes = org_data_and_shapes
    conforms, _, report = validate(data, shacl_graph=shapes,
                                   inference="rdfs", abort_on_first=False)
    assert conforms, f"Organization examples must validate:\n{report}"


def test_user_class_declared_but_unused(schema_dir, examples_dir):
    """User is in the upper model but intentionally has no canonical example."""
    g = Graph()
    g.parse(schema_dir / "organization.jsonld", format="json-ld")
    ns = "https://sap-ontology.deloitte.com/vocab#"
    user = URIRef(ns + "User")
    owl_class = URIRef("http://www.w3.org/2002/07/owl#Class")
    rdf_type = URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type")
    assert (user, rdf_type, owl_class) in g
    user_examples = list((examples_dir / "organization").glob("user-*.jsonld"))
    assert not user_examples, "User must not be populated in v0.1.0 (GDPR gate)."

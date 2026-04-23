"""Implementation / Change domain — 6 canonical examples must conform."""
import pytest
from pyshacl import validate
from rdflib import Graph

IMPL_EXAMPLES = [
    "config-pricing-procedure.jsonld",
    "change-chf-rollout.jsonld",
    "transport-chf-01.jsonld",
    "testcase-chf-invoice.jsonld",
    "incident-gi-plant1000.jsonld",
    "requirement-chf-support.jsonld",
]

DOMAINS = ["provenance", "scenario", "architecture", "process", "implementation"]


@pytest.fixture(scope="module")
def impl_data_and_shapes(schema_dir, shapes_dir, examples_dir):
    data = Graph()
    for s in DOMAINS:
        data.parse(schema_dir / f"{s}.jsonld", format="json-ld")
    data.parse(examples_dir / "provenance" / "prov-signavio-etl-001.jsonld",
               format="json-ld")
    data.parse(examples_dir / "scenario" / "scenario-as-is.jsonld",
               format="json-ld")
    for ex in IMPL_EXAMPLES:
        data.parse(examples_dir / "implementation" / ex, format="json-ld")
    shapes = Graph()
    for s in ["base"] + DOMAINS:
        shapes.parse(shapes_dir / f"{s}.shacl.ttl", format="turtle")
    return data, shapes


def test_implementation_examples_conform(impl_data_and_shapes):
    data, shapes = impl_data_and_shapes
    conforms, _, report = validate(data, shacl_graph=shapes,
                                   inference="rdfs", abort_on_first=False)
    assert conforms, f"Implementation examples must validate:\n{report}"

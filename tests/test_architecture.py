"""Architecture domain — all four canonical examples must conform
(schema + domain-specific shape + base shape)."""
import pytest
from pyshacl import validate
from rdflib import Graph

ARCH_EXAMPLES = [
    "application-component-sd.jsonld",
    "integration-sd-fi.jsonld",
    "tech-hana.jsonld",
    "dataobject-customer-master.jsonld",
]


@pytest.fixture(scope="module")
def arch_data_and_shapes(schema_dir, shapes_dir, examples_dir):
    data = Graph()
    for s in ("provenance", "scenario", "architecture"):
        data.parse(schema_dir / f"{s}.jsonld", format="json-ld")
    data.parse(examples_dir / "provenance" / "prov-signavio-etl-001.jsonld",
               format="json-ld")
    data.parse(examples_dir / "scenario" / "scenario-as-is.jsonld",
               format="json-ld")
    for ex in ARCH_EXAMPLES:
        data.parse(examples_dir / "architecture" / ex, format="json-ld")
    shapes = Graph()
    for s in ("base", "provenance", "scenario", "architecture"):
        shapes.parse(shapes_dir / f"{s}.shacl.ttl", format="turtle")
    return data, shapes


def test_architecture_examples_conform(arch_data_and_shapes):
    data, shapes = arch_data_and_shapes
    conforms, _, report = validate(data, shacl_graph=shapes,
                                   inference="rdfs", abort_on_first=False)
    assert conforms, f"Architecture examples must validate:\n{report}"

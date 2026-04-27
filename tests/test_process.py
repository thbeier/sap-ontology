"""Business Process domain — canonical examples (including recursive Process
at L3 containing a L4 sub-process) must conform."""
import pytest
from pyshacl import validate
from rdflib import Graph

PROC_EXAMPLES = [
    "process-o2c.jsonld",
    "process-order-entry.jsonld",
    "activity-credit-check.jsonld",
    "activity-confirm-order.jsonld",
    "event-order-received.jsonld",
    "decision-credit-pass.jsonld",
    "doc-sales-order.jsonld",
]

DOMAINS = ["provenance", "scenario", "architecture", "process"]


@pytest.fixture(scope="module")
def proc_data_and_shapes(schema_dir, shapes_dir, examples_dir):
    data = Graph()
    for s in DOMAINS:
        data.parse(schema_dir / f"{s}.jsonld", format="json-ld")
    data.parse(examples_dir / "provenance" / "prov-signavio-etl-001.jsonld",
               format="json-ld")
    data.parse(examples_dir / "scenario" / "scenario-as-is.jsonld",
               format="json-ld")
    for ex in PROC_EXAMPLES:
        data.parse(examples_dir / "process" / ex, format="json-ld")
    shapes = Graph()
    for s in ["base"] + DOMAINS:
        shapes.parse(shapes_dir / f"{s}.shacl.ttl", format="turtle")
    return data, shapes


def test_process_examples_conform(proc_data_and_shapes):
    data, shapes = proc_data_and_shapes
    conforms, _, report = validate(data, shacl_graph=shapes,
                                   inference="rdfs", abort_on_first=False)
    assert conforms, f"Process examples must validate:\n{report}"


def test_invalid_process_level_rejected(schema_dir, shapes_dir, examples_dir, context_path, tmp_path):
    bad = tmp_path / "bad-process.jsonld"
    ctx_uri = context_path.resolve().as_uri()
    bad.write_text(f'''{{
  "@context": "{ctx_uri}",
  "@id": "sap:bad-process",
  "@type": ["sap:Process", "sap:DomainInstance"],
  "sap:name": "Bad",
  "sap:processLevel": "not-a-level",
  "sap:inScenario": {{ "@id": "sap:scenario-as-is" }},
  "sap:hasProvenance": {{ "@id": "sap:prov-signavio-etl-001" }}
}}''', encoding="utf-8")
    data = Graph()
    for s in DOMAINS:
        data.parse(schema_dir / f"{s}.jsonld", format="json-ld")
    data.parse(examples_dir / "provenance" / "prov-signavio-etl-001.jsonld",
               format="json-ld")
    data.parse(examples_dir / "scenario" / "scenario-as-is.jsonld",
               format="json-ld")
    data.parse(bad, format="json-ld")
    shapes = Graph()
    for s in ["base"] + DOMAINS:
        shapes.parse(shapes_dir / f"{s}.shacl.ttl", format="turtle")
    conforms, _, _ = validate(data, shacl_graph=shapes,
                              inference="rdfs", abort_on_first=False)
    assert not conforms, "Unknown processLevel must violate SHACL"

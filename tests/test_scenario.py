"""Scenario class must exist with scenarioType enum + lifecycleState enum,
and two canonical examples (as-is active, to-be draft) must validate."""
from pyshacl import validate
from rdflib import Graph


def _graph_with(schema_dir, shapes_dir, *example_paths):
    g = Graph()
    g.parse(schema_dir / "scenario.jsonld", format="json-ld")
    g.parse(shapes_dir / "scenario.shacl.ttl", format="turtle")
    for p in example_paths:
        g.parse(p, format="json-ld")
    return g


def test_scenario_examples_conform(schema_dir, shapes_dir, examples_dir):
    data = Graph()
    data.parse(schema_dir / "scenario.jsonld", format="json-ld")
    data.parse(examples_dir / "scenario" / "scenario-as-is.jsonld",
               format="json-ld")
    data.parse(examples_dir / "scenario" / "scenario-to-be-chf.jsonld",
               format="json-ld")
    shapes = Graph()
    shapes.parse(shapes_dir / "scenario.shacl.ttl", format="turtle")
    conforms, _, report = validate(data, shacl_graph=shapes,
                                   inference="rdfs", abort_on_first=False)
    assert conforms, f"Examples must validate. Report:\n{report}"


def test_invalid_scenario_type_rejected(schema_dir, shapes_dir, context_path, tmp_path):
    """Scenario with an unknown scenarioType must violate SHACL."""
    bad = tmp_path / "bad.jsonld"
    ctx_uri = context_path.resolve().as_uri()
    bad.write_text(f'''{{
  "@context": "{ctx_uri}",
  "@id": "sap:bad-scenario",
  "@type": "sap:Scenario",
  "sap:name": "bad",
  "sap:scenarioType": "fantasy",
  "sap:lifecycleState": "active"
}}''', encoding="utf-8")
    data = Graph()
    data.parse(schema_dir / "scenario.jsonld", format="json-ld")
    data.parse(bad, format="json-ld")
    shapes = Graph()
    shapes.parse(shapes_dir / "scenario.shacl.ttl", format="turtle")
    conforms, _, report = validate(data, shacl_graph=shapes,
                                   inference="rdfs", abort_on_first=False)
    assert not conforms, "Invalid scenarioType should violate SHACL"

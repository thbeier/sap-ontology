"""Base domain-instance shape must flag instances that lack Provenance
or inScenario."""
from pyshacl import validate
from rdflib import Graph


def test_base_shape_rejects_missing_provenance(schema_dir, shapes_dir, context_path, tmp_path):
    bad = tmp_path / "activity-no-prov.jsonld"
    ctx_uri = context_path.resolve().as_uri()
    bad.write_text(f'''{{
  "@context": "{ctx_uri}",
  "@id": "sap:bad-activity",
  "@type": ["sap:DomainInstance"],
  "sap:name": "Fake Activity",
  "sap:inScenario": {{ "@id": "sap:scenario-as-is" }}
}}''', encoding="utf-8")
    shapes = Graph()
    shapes.parse(shapes_dir / "base.shacl.ttl", format="turtle")
    data = Graph()
    data.parse(bad, format="json-ld")
    conforms, _, report = validate(data, shacl_graph=shapes,
                                   inference="rdfs", abort_on_first=False)
    assert not conforms, "Missing hasProvenance must violate base shape"


def test_base_shape_rejects_missing_scenario(schema_dir, shapes_dir, context_path, tmp_path):
    bad = tmp_path / "activity-no-scen.jsonld"
    ctx_uri = context_path.resolve().as_uri()
    bad.write_text(f'''{{
  "@context": "{ctx_uri}",
  "@id": "sap:bad-activity-2",
  "@type": ["sap:DomainInstance"],
  "sap:name": "Fake Activity",
  "sap:hasProvenance": {{ "@id": "sap:prov-signavio-etl-001" }}
}}''', encoding="utf-8")
    shapes = Graph()
    shapes.parse(shapes_dir / "base.shacl.ttl", format="turtle")
    data = Graph()
    data.parse(bad, format="json-ld")
    conforms, _, report = validate(data, shacl_graph=shapes,
                                   inference="rdfs", abort_on_first=False)
    assert not conforms, "Missing inScenario must violate base shape"

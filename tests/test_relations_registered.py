"""Every intra-domain + inter-domain relation named in the spec must appear
in at least one schema file as an owl:ObjectProperty."""
from pyshacl import validate
from rdflib import Graph, URIRef

OWL_OBJECT_PROP = URIRef("http://www.w3.org/2002/07/owl#ObjectProperty")
RDF_TYPE = URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type")
VOCAB = "https://thbeier.github.io/sap-ontology/vocab#"

INTRA = [
    # Architecture
    "hostedOn", "mastersDataFor", "transports", "dependsOn",
    # Process
    "contains", "followedBy", "produces", "consumesDoc", "routesTo",
    # Implementation
    "includes", "carriedBy", "resultsIn",
    # Organization
    "partOf", "occupiedBy", "memberOf",
]

INTER = [
    "supportedBy", "realizedBy", "represents", "affects", "impacts",
    "linkedTo", "executes", "owns", "consumes", "authorizedFor",
    "realizesCapability", "targetsScenario", "implementedBy",
    "validates", "inScenario",
]


def _all_schema(schema_dir):
    g = Graph()
    for path in schema_dir.glob("*.jsonld"):
        g.parse(path, format="json-ld")
    return g


def test_all_intra_relations_registered(schema_dir):
    g = _all_schema(schema_dir)
    for rel in INTRA:
        subj = URIRef(VOCAB + rel)
        assert (subj, RDF_TYPE, OWL_OBJECT_PROP) in g, \
            f"Missing intra-domain relation: sap:{rel}"


def test_all_inter_relations_registered(schema_dir):
    g = _all_schema(schema_dir)
    for rel in INTER:
        subj = URIRef(VOCAB + rel)
        assert (subj, RDF_TYPE, OWL_OBJECT_PROP) in g, \
            f"Missing inter-domain relation: sap:{rel}"


def test_fully_linked_example_validates(schema_dir, shapes_dir, examples_dir, context_path, tmp_path):
    """An Activity with supportedBy + realizedBy pointing at valid targets
    must pass the full suite of shapes."""
    linked = tmp_path / "activity-linked.jsonld"
    ctx_uri = context_path.resolve().as_uri()
    linked.write_text(f'''{{
  "@context": "{ctx_uri}",
  "@id": "sap:activity-credit-check-linked",
  "@type": ["sap:Activity", "sap:DomainInstance"],
  "sap:name": "Credit check — linked",
  "sap:supportedBy": {{ "@id": "sap:app-sd-module" }},
  "sap:realizedBy":  {{ "@id": "sap:config-pricing-procedure-zstd" }},
  "sap:inScenario":  {{ "@id": "sap:scenario-as-is" }},
  "sap:hasProvenance":{{ "@id": "sap:prov-signavio-etl-001" }}
}}''', encoding="utf-8")
    data = Graph()
    for s in ["provenance", "scenario", "architecture", "process",
              "implementation", "organization", "relations"]:
        data.parse(schema_dir / f"{s}.jsonld", format="json-ld")
    for d, f in [
        ("provenance", "prov-signavio-etl-001.jsonld"),
        ("scenario",   "scenario-as-is.jsonld"),
        ("architecture","application-component-sd.jsonld"),
        ("implementation","config-pricing-procedure.jsonld"),
    ]:
        data.parse(examples_dir / d / f, format="json-ld")
    data.parse(linked, format="json-ld")
    shapes = Graph()
    for s in ["base", "provenance", "scenario", "architecture", "process",
              "implementation", "organization", "relations"]:
        shapes.parse(shapes_dir / f"{s}.shacl.ttl", format="turtle")
    conforms, _, report = validate(data, shacl_graph=shapes,
                                   inference="rdfs", abort_on_first=False)
    assert conforms, f"Linked activity example must validate:\n{report}"

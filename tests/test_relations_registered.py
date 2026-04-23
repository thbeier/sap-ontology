"""Every intra-domain + inter-domain relation named in the spec must appear
in at least one schema file as an owl:ObjectProperty."""
from rdflib import Graph, URIRef

OWL_OBJECT_PROP = URIRef("http://www.w3.org/2002/07/owl#ObjectProperty")
RDF_TYPE = URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type")
VOCAB = "https://sap-ontology.deloitte.com/vocab#"

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

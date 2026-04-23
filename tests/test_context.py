"""Tests that the JSON-LD @context defines all required namespaces and terms."""
import json


def test_context_file_exists(context_path):
    assert context_path.exists(), f"Missing: {context_path}"


def test_context_defines_sap_namespace(context_path):
    data = json.loads(context_path.read_text(encoding="utf-8"))
    ctx = data["@context"]
    assert ctx["sap"] == "https://thbeier.github.io/sap-ontology/vocab#"


def test_context_defines_standard_namespaces(context_path):
    data = json.loads(context_path.read_text(encoding="utf-8"))
    ctx = data["@context"]
    for ns in ("rdf", "rdfs", "owl", "xsd", "sh"):
        assert ns in ctx, f"Missing namespace in context: {ns}"


def test_context_defines_core_terms(context_path):
    data = json.loads(context_path.read_text(encoding="utf-8"))
    ctx = data["@context"]
    for term in ("inScenario", "hasProvenance", "name", "processLevel"):
        assert term in ctx, f"Missing term in context: {term}"

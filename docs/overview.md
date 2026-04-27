# Overview

The SAP Ontology is a client-facing, Deloitte-curated semantic model. It gives Deloitte consultants and AI agents a shared vocabulary for reasoning across three primary domains — Architecture, Business Process, Implementation / Change — plus two cross-cutting dimensions, Organization and Scenario.

## Why

SAP landscapes carry decades of tribal knowledge locked in spreadsheets and consultants' heads. Traditional RAG retrieves text chunks; AI agents need structured traversal across change → config → process → organization. The ontology provides the typed graph.

## Design anchors

| Domain | Anchored on |
|---|---|
| Architecture | ArchiMate Application + Technology Layer · LeanIX |
| Business Process | BPMN 2.0 · APQC PCF · Signavio 5-level hierarchy |
| Implementation / Change | ITIL 4 · SAP Cloud ALM |
| Organization | ArchiMate Business Layer · RACI · TOGAF BIZBOK |

## Scope boundaries

**In scope (this repository, v0.2.0):** Upper model — classes, relations, datatype properties, SHACL constraints, canonical examples. Technology-independent. CC-BY-SA 4.0.

**In scope (separate proprietary `sap-ontology-runtime` repository):** Federation runtime, Excel/CSV ingestion, mapper configurations, per-tenant Neo4j loading, scenario fork/mutate/promote operations. Pins this schema repository as a dependency.

**Still out of scope:** Vendor-specific connectors (Signavio, LeanIX, Solman, ServiceNow), populated reference instances beyond the canonical examples, query libraries.

## Schema ↔ runtime feedback loop

The schema repository is the stable, versioned vocabulary. The runtime is where the schema meets real client data, and where most findings surface — for example, v0.2.0 added `sap:transactionCode` and `sap:configurationTransaction` because the Excel ingestion pilot needed dedicated columns for the executable T-code of an Activity and the SPRO transaction of a Configuration. Those findings flow upstream as MINOR or PATCH releases here, then runtime bumps its pin. Schema-first, runtime-driven.

## Governance

- License: CC-BY-SA 4.0 for schema, shapes, examples, docs.
- Versioning: Semver. MAJOR = breaking; MINOR = additive; PATCH = documentation.
- Steering: Deloitte SAP Operate + Methods & Tools. External PRs welcome.

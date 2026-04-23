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

**In scope (v0.1.0):** Upper model — classes, relations, SHACL constraints. Technology-independent.

**Out of scope (v0.1.0):** Federation runtime, tool mappers, populated tenants. Those ship in subsequent releases.

## Governance

- License: CC-BY-SA 4.0 for schema, shapes, examples, docs.
- Versioning: Semver. MAJOR = breaking; MINOR = additive; PATCH = documentation.
- Steering: Deloitte SAP Operate + Methods & Tools. External PRs welcome.

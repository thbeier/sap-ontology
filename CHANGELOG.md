# Changelog

All notable changes to this ontology are documented here. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versioning follows [Semver](https://semver.org/).

## [0.1.1] — 2026-04-23

### Changed
- **Namespace URI** — `sap:` now binds to `https://thbeier.github.io/sap-ontology/vocab#` (was `https://sap-ontology.deloitte.com/vocab#`). Rationale: the prior URI promised hosting on a Deloitte-owned domain that is not provisioned; the new URI maps to a GitHub Pages location that will be published when the repo is pushed to `github.com/thbeier/sap-ontology`. No class / relation / shape semantics changed — the prefix binding moved.

### Note for adopters
- Any instance data authored against v0.1.0 that expanded `sap:` to the old URI must be migrated. The expansion is mechanical: string-replace `https://sap-ontology.deloitte.com/` with `https://thbeier.github.io/sap-ontology/` across JSON-LD, Turtle, and SPARQL artifacts. The short-form `sap:` references resolve automatically once a v0.1.1 `@context` is loaded.

## [0.1.0] — 2026-04-23

### Added
- JSON-LD 1.1 `@context` with sap: + standard namespaces and all registered terms.
- Three domains (24 classes total):
  - **Architecture** — ApplicationComponent, Integration, TechnologyBuildingBlock, DataObject.
  - **Business Process** — Process (recursive, `processLevel` attribute), Activity, Event, Decision, BusinessDocument.
  - **Implementation / Change** — Configuration, Change, Transport, TestCase, Incident, Requirement.
- Two cross-cutters:
  - **Organization** — OrgUnit, Role, Capability; User declared but GDPR-gated (no default population).
  - **Scenario** — Scenario with `scenarioType` (as-is / to-be / variant) and `lifecycleState` (draft / active / locked / superseded).
- Shared foundation: Provenance, DomainInstance (abstract marker).
- Intra-domain relations per §3.1–§3.4 and inter-domain relations per §3.7.
- SHACL shapes per domain + base shape enforcing the §7.4 non-negotiable floor (Provenance + Scenario on every domain instance).
- Canonical example instances — one per concrete class (20 total).
- Tests:
  - Schema self-consistency (every class has an example, shapes parse, no dangling class refs).
  - Parametrized example conformance against the full SHACL graph.
  - JSON-LD ↔ N-Quads round-trip.
- GitHub Actions CI (Python 3.11 + 3.12) running the full test suite on every push.
- Documentation: README, `docs/overview.md`, `docs/classes.md`, `docs/relations.md`, `docs/using-the-ontology.md`, `CONTRIBUTING.md`.

### Parked (addendum expected)
- `Risk` as a first-class concept (pharma / regulated clients).
- `SLA` / `OLA` on the Implementation / Change side.
- Decision on `User` gating — currently in upper model, no example; may be pushed entirely to lower model in a future MINOR.

### Known limitations
- SHACL shapes enforce **Violations** (the non-negotiable floor) only. **Warnings** and **Info** severity rules are not yet authored.
- Round-trip test is lossy for any JSON-LD feature that doesn't round-trip through N-Quads (blank nodes with particular framings) — no current examples use such features.
- No federation runtime, no tool mappers, no populated tenants. See Plan 2–4.

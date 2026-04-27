# Changelog

All notable changes to this ontology are documented here. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versioning follows [Semver](https://semver.org/).

## [Unreleased]

### Added
- **`sap:transactionCode`** (`owl:DatatypeProperty`, `xsd:string`, domain `sap:Activity`). Canonical SAP T-code that executes an Activity (e.g., `VA01` for Create Sales Order). Replaces the prior pattern of overloading `sap:externalId` with executable handles. Aliased in context as `transactionCode` (no `@type` annotation — emit as plain string to avoid SHACL `sh:in` term-equality footguns).
- **`sap:configurationTransaction`** (`owl:DatatypeProperty`, `xsd:string`, domain `sap:Configuration`). Canonical SPRO/IMG transaction that maintains a Configuration (e.g., `VOV8` for sales document types, `V/08` for pricing procedures). Mirrors `transactionCode` on the customizing side. Aliased in context as `configurationTransaction`.

### Changed
- **`sap:ActivityShape`** adds optional `sap:transactionCode` constraint with `sh:maxCount 1` and pattern `^[A-Z][A-Z0-9_./-]+$`. The canonical entry-point T-code is unique per Activity; variants (VA02 change, VA03 display) belong in `description`.
- **`sap:ConfigurationShape`** adds optional `sap:configurationTransaction` constraint with the same regex. SPRO codes that include slashes (`V/08`) and dots (`F.05`) match.
- **`sap:DecisionShape`** tightened from a single `sap:name` constraint to require:
  - `sap:decisionRule` (xsd:string, minCount 1) — branching rule expression
  - `sap:routesTo` → `sap:Activity` (minCount 1) — at least one onward path
  Rationale: a Decision with neither rule nor routing is structurally meaningless.

### Note for adopters
- Existing data using `sap:externalId` for T-codes continues to validate — `externalId` remains in the schema as a generic cross-system identifier. Migration is opt-in: rename `external_id` columns to `transaction_code` in fixture authoring tools when ready.
- The new `sap:DecisionShape` constraints are tighter than v0.1.x. Any existing Decision instance lacking `decisionRule` or `routesTo` will now fail SHACL validation. Audit existing Decisions before upgrading consumers.

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

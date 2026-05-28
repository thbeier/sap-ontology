# Changelog

All notable changes to this ontology are documented here. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versioning follows [Semver](https://semver.org/).

## [0.8.3] — 2026-05-28

### Changed (breaking)
- **`sap:realizesActivity` removed; `sap:realizedBy` now accepts both `sap:Configuration` and `sap:RicefwObject`.** The v0.7.0 RicefwObject→Activity edge was direction-asymmetric with the long-standing Activity→Configuration `realizedBy`: both Configuration and RicefwObject *enable* the Activity, so both should attach on the Activity side with consistent direction and name. After this change:
  - `ActivityShape.realizedBy` uses `sh:or` to accept either class.
  - `RicefwObjectShape` no longer declares a `realizesActivity` property (the edge is removed from `schema/implementation.jsonld` and from the JSON-LD context).
  - Example fixtures inverted: `activity-credit-check` now carries `realizedBy → ricefw-zmm-tol-check` instead of the ricefw row pointing back.
- **`sap:affects` and `sap:includes` now accept `sap:RicefwObject` in addition to `sap:Configuration`** on `ChangeShape`. A Change can target a Z-program or BAdI just as it can target a SPRO entry — the v0.7.0 RicefwObject class was missing from the Change pipeline. `ChangeShape` also now explicitly constrains `sap:includes` (previously declared in the schema but unconstrained by SHACL).

### Migration
- Replace `RicefwObject.realizesActivity → Activity` with `Activity.realizedBy → RicefwObject`. Tenants with existing RICEFW data can do this via a Cypher inversion. The runtime's mm_baseline fixture follows the new convention.

## [0.8.2] — 2026-05-28

### Changed
- **`sap:followedBy` is now properly constrained as BPMN sequence flow.** Previously had no `rdfs:domain` / `rdfs:range` and no SHACL constraint on `ActivityShape` / `EventShape` — so `Event` had zero outgoing or incoming edges in the model even though every BPMN scenario needs them. Now:
  - `rdfs:comment` on the property documents the four valid patterns: Activity→Activity (sequential steps — the common case), Event→Activity (event triggers a step), Activity→Event (step emits an event), Activity→Decision (step ends at a gateway). Decision keeps `sap:routesTo` for its outgoing branches.
  - `ActivityShape.followedBy` and new `EventShape.followedBy` both target `sap:or ( Activity Event Decision )` — flow nodes only.
  - The Activity → Activity self-loop pattern is now explicit and validated rather than allowed-by-omission.

## [0.8.1] — 2026-05-28

### Changed
- **`sap:realizesCapability` documented as a strategic-layer cross-link, not an operational requirement.** Always was optional (no `minCount`); now annotated with `sh:severity sh:Info` and an explanatory `sh:message`, and the `rdfs:comment` on the property + the `Capability` row in `docs/classes.md` spell out the load-bearing distinction: `Capability` is the durable business competence (TOGAF / LeanIX BCM); `Requirement` is the transactional path to change it. Operational consumers (incident triage, change impact) never traverse `realizesCapability` — it powers portfolio heat-maps, capability dashboards, and EAM-style strategic queries. Tenants without those use cases can leave `realizesCapability` empty without consequence.

## [0.8.0] — 2026-05-28

### Changed (breaking)
- **`sap:processId` is now a hard SHACL violation when missing** (previously `sh:Warning` in v0.7.2). Every `sap:Process` instance must declare a customer-owned identity code matching `^[A-Za-z0-9][A-Za-z0-9._-]*$`. The federation runtime's 31 module baselines have been migrated against the canonical Process taxonomy that ships in `tests/fixtures/excel/_process_taxonomy/process.csv` (12 L1 value chains + 84 L2 process groups, with hierarchical numbering at L3+). Tenant graphs created against v0.7.x that contain Process nodes without `processId` will now produce SHACL violations on conformance.

### Migration
- Customer tenants need to backfill `sap:processId` on every Process node before upgrading the upper-model pin past v0.7.2. The recommended convention matches the canonical taxonomy: `<L1-CamelCase>-<NNN>[-<NNN>...]` (e.g. `PtP-040-020`, `RtR-080-110`). The taxonomy fixture in the runtime repository serves as a reference enumeration.

## [0.7.2] — 2026-05-27

### Added
- **`sap:processId`** — customer-owned identity code for a Process (e.g. `RtR-10-20`, `O2C.4.1.3`, `MDG-BP-CR`). Closes the gap flagged in design-doc review: the federation runtime and spec 03 have been emitting `sap:processId` as a join key, but the property did not exist in the upper model — it loaded as an untyped, unconstrained literal. Now declared on `schema/process.jsonld` with `rdfs:domain: sap:Process`, bound in `context/sap-ontology-context.jsonld`, and constrained by SHACL.
- **`sap:ProcessShape.processId` constraints** in `shapes/process.shacl.ttl`:
  - `sh:datatype xsd:string`, `sh:minCount 1`, `sh:maxCount 1`, `sh:pattern "^[A-Za-z0-9][A-Za-z0-9._-]*$"`.
  - `sh:severity sh:Warning` on the cardinality during v0.7.x — existing fixtures (~36 module baselines in the federation runtime) do not yet carry `processId`. Promoted to `sh:Violation` in v0.8.0 once mappers thread the value through.
- **`sap:ProcessIdUniqueShape`** — SPARQL invariant ensuring two `Process` nodes never share the same `processId` within a graph. Per-tenant uniqueness is achieved via the runtime's one-database-per-tenant isolation.

### Migration
- Designers and mappers should start populating `sap:processId` on every new Process. The clean separation is: `processId` = customer's stable identity (single-valued, unique, business-owned); `inScenario` = M:N classification edges to one or more best-practice `Scenario` nodes (e.g. SAP J45).
- Distinct from `sap:externalId` — `externalId` may reference any external system (Signavio model ID, Cloud-ALM feature ID), while `processId` is the customer's authoritative business code. Both can coexist on the same Process.

## [0.7.1] — 2026-05-27

### Changed
- **Split `sap:changeStatus` into two properties.** v0.5 claimed to unify a single `changeStatus` enum across Change and Provenance, but only `ChangeShape` was migrated — `ProvenanceShape` kept the v0.4 AMS-lifecycle enum, leaving one property with two incompatible vocabularies on two shapes. v0.6's environment-binding work also generalized Provenance to non-Change sources (Cloud-ALM Requirements, Signavio models, ServiceNow Incidents) where the SAP-transport pipeline vocabulary (`released-to-qa`, `imported-to-prd`, `baseline-merged`) is semantically wrong.
  - `sap:changeStatus` is now declared only on `sap:Change` (transport delivery pipeline: `draft → in-development → unit-tested → released-to-qa → qa-passed → released-to-prd → imported-to-prd → baseline-merged`, plus `rejected`, `rolled-back`). Property declaration moved to `schema/implementation.jsonld`.
  - `sap:lifecycleStage` (new) replaces `sap:changeStatus` on `sap:Provenance` and carries the source-agnostic assertion-maturity enum: `planned → in-progress → in-integration-test → in-uat → released-prod → rolled-back → rejected`.
  - `statusEnteredAt`, `statusExitedAt`, `externalChangeId`, `approvalEvidenceUri` remain on `Provenance` and now pair with `lifecycleStage`.

### Migration
- Any instance setting `sap:changeStatus` on a `Provenance` node must rename the predicate to `sap:lifecycleStage`. No instances in this repository's `examples/` or `tests/` are affected. Runtime fixtures emit `changeStatus` only on `Change` nodes (verified across the runtime mappers and CLI), so this is a documentation-only break for runtime callers.

## [0.7.0] — 2026-05-20

### Added
- **`sap:RicefwObject` class** (subclass of `sap:ApplicationComponent`) for customer-developed extensions to the standard SAP product: Reports, Interfaces, Conversions, Enhancements, Forms, Workflows. Closes a long-standing gap — the runtime's design docs referenced RICEFW objects (~20 mentions across specs 01b and 02 as a corpus class, anchor type, graph entity, and remediation target) but the upper model had no class for them, forcing every RICEFW reference into `ApplicationComponent` and losing the distinction between standard SAP software and customer-built extensions.
- **`sap:ricefwType`** (pinned enum on `RicefwObject`): `Report` / `Interface` / `Conversion` / `Enhancement` / `Form` / `Workflow`. Single property + enum rather than six subclasses — the classification matters for routing (forms and interfaces have different debug paths) but the structural model is identical across all six.
- **`sap:objectId`** (required string on `RicefwObject`): the Z\*/Y\*/customer-namespace identifier (e.g. `ZMM_TOL_CHECK`). Used by gCTS / Git path resolution and ATC / Code Inspector lookups during incident triage and remediation drafting.
- **`sap:enhances`** (ObjectProperty `RicefwObject → ApplicationComponent`): the standard SAP component or object being extended (BAdI host, enhancement spot, user exit, standard report being copied-and-modified). Required for Reports/Interfaces/Conversions that replace standard behaviour; optional for greenfield Forms/Workflows.
- **`sap:realizesActivity`** (ObjectProperty `RicefwObject → Activity`, multi-valued): the business action this customer object supports. The edge that powers `graph.ricefw_for_activity` blast-radius queries in spec 02.
- **`sap:RicefwObjectShape`** (SHACL): enforces required `name`, `objectId`, `ricefwType` (pinned enum), `lifecycleState` (inherited from ApplicationComponent's enum: `planned` / `live` / `sunset` / `retired`), and class-typed `enhances` / `realizesActivity` edges.
- Example fixture `examples/implementation/ricefw-zmm-tol-check.jsonld` — the `ZMM_TOL_CHECK` enhancement cited in design spec 02 §3.1.

### Rationale
- RICEFW IS deployed software — just customer-built — so subclassing `ApplicationComponent` gives it `lifecycleState`, `vendor='customer'`, `deployment`, `tier`, `hostedOn`, `dependsOn` for free.
- The model handles customizing-with-coupling (a BAdI implementation that reads a Z-table) naturally via the existing `dependsOn` edge to `Configuration` — no special case needed.

### Migration
- Additive only. Existing fixtures continue to validate. Runtimes pinned to v0.6.0 ignore the new class and properties. Module baselines that should carry RICEFW objects (custom forms, ABAP enhancements) can be backfilled incrementally without invalidating existing data.

## [0.6.0] — 2026-05-19

### Added
- **`scenarioType` enum extended with `best-practice`.** Identifies an SAP-published reference Scenario (Solution Process, e.g. `J45`, `BD9`) that customer Processes may map to via the existing multi-valued `sap:inScenario` edge. Best-practice scenarios are loaded read-only and locked (`lifecycleState=locked`). Existing scenarios (`as-is`, `to-be`, `variant`) are unaffected — this is an additive enum extension.
- **`sap:scenarioCode` (optional string on `Scenario`).** External identifier for a Scenario. For best-practice scenarios this carries the SAP Solution Process code (`J45`); for customer scenarios it may carry an internal code or be null. Queryable directly without IRI parsing.
- **`sap:observedInSystem` (optional ObjectProperty on `Provenance`, range `sap:System`).** The runtime System an environment-bound fact applies to. Populated for `TransportImport` (the target system of the import), `Incident` (the system the incident was raised against), and future SPRO-extracted `Configuration` instances. Absent for design-time facts (modelled Processes, Requirements, TestCases) that apply across the landscape. This is the dimension that turns the graph into a debuggable model of the running landscape — *"what is actually live in PRD right now?"*
- **`sap:EnvironmentBoundProvenanceShape` (SHACL warning).** Targets `TransportImport` and `Incident`; warns when their attached `Provenance` is missing `observedInSystem`. Warning, not violation — older fixtures keep loading while extractors backfill, but dirty extractors are surfaced at validation time.

### Rationale
- Modelled to support the Signavio + Cloud ALM integration spec (runtime `docs/design/03-signavio-cloud-alm-integration.md`). The first user is the customer-process / SAP-Best-Practice classification (M:N via `inScenario`) and the PRD-incident blast-radius query.
- Deliberately re-used `sap:Scenario` rather than introducing a `BestPracticeScenario` class — `Scenario` already supports multi-valued `inScenario` membership, `lifecycleState=locked`, and the existing scenario operations (`fork`, `mutate`, `promote`, `branch`, `diff`) which now work on best-practice scenarios for free.

### Migration
- Additive only. Existing fixtures continue to validate. Runtimes that consume v0.6.0 may emit `scenarioCode` and `observedInSystem`; runtimes pinned to v0.5.0 ignore them.

## [0.5.0] — 2026-05-13

### Added
- **`sap:System` class** (subclass of `sap:ApplicationComponent`) for concrete runtime SAP systems, distinguished by `sap:systemRole` (`DEV`/`QA`/`PRD`/`sandbox`/`training`). Enables landscape-topology queries; Transports are imported INTO Systems.
- **`sap:TransportImport` class** reifying each STMS / Cloud ALM import as a discrete, queryable event. Edges: `Transport -[importedInto]-> TransportImport -[targets]-> System`. Carries `importedAt`, `importedBy`, `importResult` (`success` / `failed` / `in-progress` / `rolled-back`). Multiple TransportImports may exist per (Transport, System) pair when re-imports happen.
- **Pinned `sap:changeStatus` enum** on `Change`/`Provenance`: `draft → in-development → unit-tested → released-to-qa → qa-passed → released-to-prd → imported-to-prd → baseline-merged`, plus `rejected` and `rolled-back`. Legacy `sap:status` retained for back-compat.
- New context terms: `systemRole`, `importedAt`, `importedBy`, `importResult`, `importedInto`, `targets`.

### Rationale
- The v0.4 Change/Transport model couldn't express *which system received a transport at what time* — the v0.5 reification makes that queryable, auditable, and replayable.

## [0.4.0] — 2026-05-10

### Added
- **`sap:Provenance` extended with 26 optional properties** in five concerns:
  - **Source linkage:** `sourceChunkId`, `sourceDocType`, `sourcePage`, `sourceSpan` — bridge graph to vector store and pinpoint the source span.
  - **Identity & temporal:** `assertedRole`, `extractedAt`, `reviewedAt`, `recordedAt` — separate extraction time, review time, and graph transaction time from the canonical assertion timestamp.
  - **Bitemporal validity:** `validFrom`, `validTo` — when the asserted fact is true in the business world, paired with `recordedAt` (graph transaction time).
  - **Reliability:** `confidence` (`xsd:decimal` in `[0.0, 1.0]`), `extractorModel`, `promptVersion` — reproducibility for LLM-driven extractions.
  - **Lineage (append-only):** `supersedes`, `supersededBy`, `relationshipToReference` (`confirms` / `overrides` / `extends`), `referenceProvenance`, `overrideReason` — chain new assertions on top of prior ones; never update or delete a Provenance.
  - **Phase & tenancy:** `baselinePhase` (`reference` / `client-transition` / `client-update`), `clientTenant`.
  - **Change lifecycle (AMS):** `changeStatus` (`planned` · `in-progress` · `in-integration-test` · `in-uat` · `released-prod` · `rolled-back` · `rejected`), `statusEnteredAt`, `statusExitedAt`, `externalChangeId`, `approvalEvidenceUri` — anchor every Change transition to its operational source of truth.
- **Three SHACL/SPARQL invariants** on `sap:ProvenanceShape`:
  1. `trustLevel = audited` ⇒ `approvalEvidenceUri` must be present.
  2. `relationshipToReference = overrides` ⇒ `overrideReason` must be present.
  3. `method = LLM-extracted` (or `LLM-extraction`) ⇒ `extractorModel` must be present.

### Changed
- **`sap:trustLevel`** enum extended with `extracted`, `reviewed`, `confirmed`, `audited` (in addition to the legacy `authoritative` / `verified` / `asserted` / `inferred` / `draft`).
- **`sap:method`** enum extended with `SPRO-export`, `config-export`, `change-record`, `manual-review`, `LLM-extraction` (alongside `manual` / `ETL` / `LLM-extracted`).

### Note for adopters
- Backwards-compatible with v0.3.0. All v0.3 Provenance instances remain valid — every new property is optional and the new SHACL invariants only fire when the triggering value is present.
- For the runtime: the new ObjectProperty edges (`supersedes`, `supersededBy`, `referenceProvenance`) target `sap:Provenance` itself. Mappers ingesting per-row Provenance must allowlist these as Provenance edges (the runtime mapper was updated in `sap-ontology-runtime` v0.4.0 to skip auto-attaching `inScenario` / `hasProvenance` to Provenance rows themselves).

### Provenance of this release
Driven by two pilots in the federation runtime: (a) AMS-on-graph — capturing change-lifecycle transitions as Provenance records so blast-radius queries see real change status, and (b) per-row provenance ingestion — letting Excel authors override the fixture-default Provenance row-by-row, with cited override reasons traceable back to the reference baseline. Both pilots needed bitemporal time, append-only lineage, and reproducibility metadata that v0.3 didn't carry.

## [0.3.0] — 2026-05-01

### Changed (BREAKING)
- **`sap:transports` → `sap:carries`** on `Integration → DataObject`. The relation has been renamed to remove the lexical collision with the change-management class `sap:Transport` (CTS request). `sap:Transport` and `sap:carriedBy` (`Change → Transport`) are unchanged. Rationale: the verb `transports` and the noun `Transport` are spelled identically but denote orthogonal concepts (a runtime data flow vs. a workbench/customizing promotion artifact). The collision caused a downstream runtime mapper bug where `Integration.transports` was incorrectly routed to the `Transport` class instead of `DataObject`. The rename is permanent — there is no transitional alias.
- `sap:carries` carries a new `rdfs:label` ("carries") and a `rdfs:comment` documenting the rename and explicitly distinguishing it from `sap:Transport` / `sap:carriedBy`.

### Migration
- **JSON-LD instances:** rename property `sap:transports` (long form) and `transports` (context alias) to `sap:carries` / `carries`. SPARQL/Cypher queries that traverse the relation must update accordingly.
- **Excel/CSV ingestion fixtures:** rename the `transports` column on the `integration` sheet to `carries`. Cell values (DataObject ids) are unchanged.
- **Downstream consumers (federation runtime):** the runtime mapper allowlist must accept `carries` as the Integration edge column with target class `DataObject`. See `sap-ontology-runtime` v0.3.0.

### Note for adopters
- This is a breaking schema rename. Any v0.1–v0.2 instance data using `sap:transports` will fail SHACL validation under v0.3.0 because the property is no longer registered. Migrate before upgrading.
- The conceptual model is unchanged: an `Integration`'s payload has always been a `DataObject` (per §3.1 architecture relations). Only the property name moved.

### Provenance of this release
The rename was triggered by a federation-runtime build (sap-ontology-runtime v0.3.0) that surfaced a mapper bug where `Integration.transports` resolved to the `Transport` class instead of `DataObject`. The bug was a direct consequence of the spelling collision between the property and the class. Fixing only the mapper would have left the trap in place; renaming the property removes the ambiguity at the model level.

## [0.2.0] — 2026-04-27

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

### Provenance of this release
The two new properties and the tightened DecisionShape were surfaced by the Excel/CSV ingestion pilot in the federation runtime: SAP consultants authoring scenarios in spreadsheets need a single canonical column for the executable handle of an Activity (T-code) and a parallel column for the configuring transaction of a Configuration (SPRO code). Overloading `externalId` with both proved error-prone in the runtime's mapper allowlist; carving out dedicated properties solved the ambiguity. The DecisionShape change came from real fixture data where Decisions without rules or routing were silently accepted and produced unanswerable graph queries.

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

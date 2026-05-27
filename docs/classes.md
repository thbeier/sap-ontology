# Class Catalog

For machine-readable definitions see `schema/*.jsonld`. For the full property list per class, read the schema files directly — this page lists classes only.

## Notable datatype properties (v0.4.0)

| Property | Domain | Range | Purpose |
|---|---|---|---|
| `sap:transactionCode` | `sap:Activity` | `xsd:string` | Canonical SAP T-code that executes the Activity (e.g., `VA01`). Constrained by `sh:pattern` to `^[A-Z][A-Z0-9_./-]+$`. |
| `sap:configurationTransaction` | `sap:Configuration` | `xsd:string` | Canonical SPRO/IMG transaction maintaining the Configuration (e.g., `VOV8`, `V/08`). Same regex as `transactionCode`. |
| `sap:decisionRule` | `sap:Decision` | `xsd:string` | Branching rule expression (required as of v0.2.0). |

## Provenance properties (v0.4.0)

The `sap:Provenance` class carries 30+ optional datatype/object properties, grouped by concern. See `schema/provenance.jsonld` for full definitions and `shapes/provenance.shacl.ttl` for SHACL constraints (including the three SPARQL invariants enforced in v0.4).

| Concern | Properties |
|---|---|
| Source linkage | `sourceSystem`, `sourceUri`, `sourceChunkId`, `sourceDocType`, `sourcePage`, `sourceSpan` |
| Identity & temporal | `assertedBy`, `assertedRole`, `assertedAt`, `extractedAt`, `reviewedAt`, `recordedAt` |
| Bitemporal validity | `validFrom`, `validTo` (when the fact is true in the world; pair with `recordedAt` for graph transaction time) |
| Reliability | `trustLevel` (authoritative · verified · asserted · inferred · draft · extracted · reviewed · confirmed · audited), `confidence`, `method`, `extractorModel`, `promptVersion` |
| Lineage (append-only) | `supersedes`, `supersededBy`, `relationshipToReference` (confirms / overrides / extends), `referenceProvenance`, `overrideReason` |
| Phase & tenancy | `baselinePhase` (reference / client-transition / client-update), `clientTenant` |
| Assertion lifecycle (AMS/ALM) | `lifecycleStage` (planned · in-progress · in-integration-test · in-uat · released-prod · rolled-back · rejected), `statusEnteredAt`, `statusExitedAt`, `externalChangeId`, `approvalEvidenceUri` — maturity of the assertion itself, source-agnostic. Distinct from `Change.changeStatus`, which carries the SAP-transport delivery pipeline (draft → in-development → … → baseline-merged) and lives on the Change class, not on Provenance. |

SPARQL invariants (v0.4): `audited` trustLevel requires `approvalEvidenceUri`; `relationshipToReference = overrides` requires `overrideReason`; `method = LLM-extracted` (or `LLM-extraction`) requires `extractorModel`.

## Architecture
| Class | Purpose |
|---|---|
| `sap:ApplicationComponent` | A deployable software unit providing business functionality |
| `sap:Integration` | A data or control flow between two components |
| `sap:TechnologyBuildingBlock` | Infrastructure / platform layer |
| `sap:DataObject` | Logical data entity exchanged or persisted |

## Business Process
| Class | Purpose |
|---|---|
| `sap:Process` | Recursive — covers L1 value chains through L4 sub-processes (see `processLevel`). Identity is `sap:processId` (customer-owned code, e.g. `RtR-10-20`); SAP best-practice BP codes (J45 etc.) are M:N *classification* carried via `sap:inScenario`, not identity. |
| `sap:Activity` | Leaf (L5) — atomic step performed by a role or system |
| `sap:Event` | Trigger or outcome marker |
| `sap:Decision` | Branch point with a business rule |
| `sap:BusinessDocument` | Physical or digital artifact in the flow |

## Implementation / Change
| Class | Purpose |
|---|---|
| `sap:Configuration` | Setting, customization, or custom code item |
| `sap:Change` | Controlled modification A → B |
| `sap:Transport` | Technical unit carrying a Change |
| `sap:TestCase` | Scenario validating a Change |
| `sap:Incident` | Unplanned interruption |
| `sap:Requirement` | Stated need targeting a future Scenario |

## Organization
| Class | Purpose |
|---|---|
| `sap:OrgUnit` | Legal or hierarchical entity |
| `sap:Role` | Durable function performed by humans or system agents |
| `sap:Capability` | What the business does (TOGAF / BIZBOK) |
| `sap:User` | GDPR-gated — not populated by default |

## Scenario / Versioning
| Class | Purpose |
|---|---|
| `sap:Scenario` | Named state with lifecycleState ∈ {draft, active, locked, superseded} |

## Foundation
| Class | Purpose |
|---|---|
| `sap:Provenance` | Required on every instance — where the claim came from, when it is true (bitemporal), how trustworthy it is, what it supersedes, and (for Change-bearing assertions) its AMS lifecycle status. See "Provenance properties" above. |
| `sap:DomainInstance` | Abstract marker — every concrete domain class subclasses this |

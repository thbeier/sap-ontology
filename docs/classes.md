# Class Catalog

For machine-readable definitions see `schema/*.jsonld`. For the full property list per class, read the schema files directly — this page lists classes only.

## Notable datatype properties (v0.2.0)

| Property | Domain | Range | Purpose |
|---|---|---|---|
| `sap:transactionCode` | `sap:Activity` | `xsd:string` | Canonical SAP T-code that executes the Activity (e.g., `VA01`). Constrained by `sh:pattern` to `^[A-Z][A-Z0-9_./-]+$`. |
| `sap:configurationTransaction` | `sap:Configuration` | `xsd:string` | Canonical SPRO/IMG transaction maintaining the Configuration (e.g., `VOV8`, `V/08`). Same regex as `transactionCode`. |
| `sap:decisionRule` | `sap:Decision` | `xsd:string` | Branching rule expression (required as of v0.2.0). |

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
| `sap:Process` | Recursive — covers L1 value chains through L4 sub-processes (see `processLevel`) |
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
| `sap:Provenance` | Required on every instance — where the claim came from |
| `sap:DomainInstance` | Abstract marker — every concrete domain class subclasses this |

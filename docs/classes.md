# Class Catalog

Generated in Task 16. For machine-readable definitions see `schema/*.jsonld`.

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

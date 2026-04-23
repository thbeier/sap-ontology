# Relation Catalog

## Intra-domain relations

### Architecture
| Relation | From → To |
|---|---|
| `sap:hostedOn` | ApplicationComponent → TechnologyBuildingBlock |
| `sap:mastersDataFor` | ApplicationComponent → DataObject |
| `sap:transports` | Integration → DataObject |
| `sap:dependsOn` | ApplicationComponent → ApplicationComponent |

### Business Process
| Relation | From → To |
|---|---|
| `sap:contains` | Process → Process \| Activity |
| `sap:followedBy` | Activity \| Event \| Decision → Activity \| Event \| Decision |
| `sap:produces` | Activity → BusinessDocument |
| `sap:consumesDoc` | Activity → BusinessDocument |
| `sap:routesTo` | Decision → Activity |

> `consumesDoc` disambiguates from `consumes` (which is cross-domain: OrgUnit → ApplicationComponent).

### Implementation / Change
| Relation | From → To |
|---|---|
| `sap:includes` | Change → Configuration |
| `sap:carriedBy` | Change → Transport |
| `sap:resultsIn` | Incident → Change |

### Organization
| Relation | From → To |
|---|---|
| `sap:partOf` | OrgUnit → OrgUnit (recursive); Role → OrgUnit |
| `sap:occupiedBy` | Role → User |
| `sap:memberOf` | User → OrgUnit |

## Inter-domain relations — the differentiator

| Relation | From → To | Meaning |
|---|---|---|
| `sap:supportedBy` | Activity → ApplicationComponent | Step runs on this app |
| `sap:realizedBy` | Activity → Configuration | Business rule implemented by these configs |
| `sap:represents` | BusinessDocument → DataObject | Document ↔ data entity |
| `sap:affects` | Change → Configuration | A change modifies these configs |
| `sap:impacts` | Change → Activity | Derived from `affects` + `realizedBy` (not authored) |
| `sap:linkedTo` | Incident → Activity \| ApplicationComponent \| Configuration | AMS entry point |
| `sap:executes` | Role → Activity | RACI Responsible — the business-org link |
| `sap:owns` | OrgUnit → Configuration \| Process | Custody / approval |
| `sap:consumes` | OrgUnit → ApplicationComponent | Which org uses which system |
| `sap:authorizedFor` | Role → Configuration | SAP auth model link |
| `sap:realizesCapability` | Process → Capability | Capability delivery |
| `sap:targetsScenario` | Requirement → Scenario | Target-state binding |
| `sap:implementedBy` | Requirement → Change | Delivery chain |
| `sap:validates` | TestCase → Change \| Configuration \| Activity | Test coverage |
| `sap:inScenario` | (any domain instance) → Scenario | State scoping |
| `sap:hasProvenance` | (any domain instance) → Provenance | Source accountability |

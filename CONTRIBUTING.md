# Contributing to the SAP Ontology

Thank you for the interest. This ontology is curated by Deloitte under an open license (CC-BY-SA 4.0). External contributions are welcome; the Working Group maintains direction.

## What can be contributed

- **Via issue:** bug reports, clarifications, proposed additions, use cases.
- **Via PR:** fixes to documentation, new examples, additional SHACL constraints.
- **Via proposal (issue → PR):** new classes, new relations, enum value additions.

## How to propose a schema change

1. Open a GitHub Issue. Include:
   - Use case driving the change
   - Affected classes / relations / shapes
   - Example instance demonstrating the change
   - Impact on existing mapper configurations (if known)
2. Working Group triages. MAJOR-impact proposals are escalated to the steering committee.
3. Accepted proposals get a PR. Changes must include:
   - Schema update in `schema/*.jsonld`
   - Shape update in `shapes/*.shacl.ttl`
   - Example in `examples/<domain>/`
   - Test or extension of existing tests
   - CHANGELOG entry

## Version bump rules

- **MAJOR:** remove a class, remove a relation, tighten cardinality, change attribute semantics.
- **MINOR:** add a class, add a relation, add an optional attribute, add enum values.
- **PATCH:** documentation, non-breaking SHACL clarifications, example refinements.

## Release cadence

- PATCH: as-needed (monthly max)
- MINOR: quarterly
- MAJOR: annual, with a migration dry-run on a real client instance

## Review gates

All PRs run the CI test suite (`pytest`). Required to pass:
- Schema self-consistency
- Example conformance
- Round-trip serialization
- No dangling class references

Plus maintainer review. MAJOR changes require steering committee approval.

# SAP Ontology for Context Engineering

A technology-independent, Deloitte-curated semantic model for reasoning across SAP **Architecture × Business Process × Implementation / Change**, with Organization and Scenario as cross-cutting dimensions.

**Status:** v0.2.0 — upper model + SHACL shapes + canonical examples. The companion [federation runtime](#runtime-companion) (Excel/CSV ingestion → Neo4j) lives in a separate proprietary repository.
**License:** Upper model, SHACL shapes, and examples are released under [CC-BY-SA 4.0](LICENSE). Mapper configurations and federation runtime are Deloitte proprietary.

## What's here

| Directory | Contents |
|---|---|
| `context/`  | JSON-LD 1.1 `@context` binding short names to full URIs |
| `schema/`   | Class + property definitions, one file per domain |
| `shapes/`   | SHACL shapes in Turtle, one file per domain; `base.shacl.ttl` enforces the non-negotiable floor |
| `examples/` | Canonical example instances, one per class |
| `tests/`    | pytest suite — schema self-consistency, example conformance, round-trip |
| `docs/`     | Human-readable documentation |

## Quickstart

```bash
python -m venv .venv
source .venv/Scripts/activate   # Windows Git Bash; use .venv/bin/activate on Unix
pip install -e ".[dev]"
pytest
```

See [`docs/overview.md`](docs/overview.md) for the design rationale, [`docs/classes.md`](docs/classes.md) for the class catalog, and [`docs/using-the-ontology.md`](docs/using-the-ontology.md) for how to sub-class in a client engagement.

## Runtime companion

A separate proprietary repository (`sap-ontology-runtime`) consumes this schema as a pinned dependency and provides:

- Excel/CSV ingestion for SAP consultants who author scenarios in spreadsheets
- JSON-LD ↔ SHACL ↔ Neo4j pipeline with per-tenant databases
- Scenario fork / mutate / promote / diff operations for as-is → to-be reasoning

The runtime is what surfaces findings (like `sap:transactionCode` and the tightened `DecisionShape` in v0.2.0) that flow back into this schema repository.

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md). Contribution is welcome under the governance model described in [`docs/overview.md`](docs/overview.md).

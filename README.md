# SAP Ontology for Context Engineering

A technology-independent, Deloitte-curated semantic model for reasoning across SAP architecture, business process, and implementation / change.

**Status:** v0.1.0 (MVP) — upper model and SHACL shapes only. No runtime yet.

**License:** Upper model, SHACL shapes, and examples are released under [CC-BY-SA 4.0](LICENSE). Mapper configurations and federation runtime are Deloitte proprietary and live in separate repositories.

## Structure

- `context/` — JSON-LD 1.1 @context
- `schema/` — Class + property definitions per domain
- `shapes/` — SHACL shapes per domain (Turtle)
- `examples/` — Canonical example instances per class
- `tests/` — Schema consistency + example conformance + round-trip tests
- `docs/` — Human-readable documentation

## Quickstart

```bash
pip install -e .[dev]
pytest
```

See `docs/overview.md` for the design rationale.

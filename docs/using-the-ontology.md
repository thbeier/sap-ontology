# Using the Ontology

## In a client engagement

1. Pin an upper-model version in your project metadata (e.g., `v0.1.0`).
2. Sub-class upper-model classes to name client-specific concepts. Example:
   ```json
   {
     "@id": "client:CoBuyerProfile",
     "@type": "owl:Class",
     "rdfs:subClassOf": { "@id": "sap:Role" }
   }
   ```
3. Instances carry the client's URI scheme:
   `https://thbeier.github.io/sap-ontology/client/{clientId}/{domain}/{class}/{instance-id}`
4. Lower-model classes stay in the client's private instance; they do **not** flow back unless generalized via the contribution process.

## Populating a scenario

Every non-schema instance carries:
- `@type`: including `sap:DomainInstance`
- `sap:inScenario`: pointer to an existing `sap:Scenario`
- `sap:hasProvenance`: pointer to a `sap:Provenance` record

Missing either is a SHACL Violation — the record is rejected at ingestion.

## Validating locally

```bash
pip install pyshacl
pyshacl -s shapes/base.shacl.ttl \
        -s shapes/provenance.shacl.ttl \
        -s shapes/scenario.shacl.ttl \
        -s shapes/architecture.shacl.ttl \
        -s shapes/process.shacl.ttl \
        -s shapes/implementation.shacl.ttl \
        -s shapes/organization.shacl.ttl \
        -s shapes/relations.shacl.ttl \
        your-instance-file.jsonld
```

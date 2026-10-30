# Shared contract v0.1

`fixtures/programs.json` contains synthetic program records. Required fields: `id`, `name`, `age_min`, `age_max`, `hours`, `accommodations`, `availability`, `source_ids`. Unknown accommodations and availability are JSON null. `fixtures/sources.json` explicitly identifies each source as fictional. A source reference is not proof of verification; real evidence needs reviewer and verification date recorded separately.

`fixtures/requests.json` contains fictional requests with `id`, `age`, and `needs`. No names, addresses, or persistent person identifiers are used.

Approaches return the structure in `fixtures/response-example.json`: a request ID, candidate program IDs, evidence IDs, explicit unknowns, and next steps. Evidence IDs must exist in the reviewed source set; program IDs must exist in the program set. Do not turn null into false, true, or an assumed opening. Different tasks can operate on subsets, but must document those boundaries.

This is a starter integration contract. Proposed changes require a PR that updates fixtures, checks, and affected approaches together.

# PlantGuard Data Sources and Provenance

## 1. Scope

PlantGuard uses course-generated synthetic operational data for its
industrial maintenance workflow. The project owner confirmed with course
management that generated data is sufficient for this submission.

The dataset is intended for development, retrieval, workflow testing,
guardrail validation, and behavioral evaluation. It does not represent
live equipment telemetry or actual maintenance operations.

## 2. Data assets

| Asset | Purpose | Provenance |
|---|---|---|
| Maintenance corpus | Manuals, procedures, and maintenance reference material used for retrieval and citations | Generated through the course data toolkit |
| Intake records | Synthetic maintenance events used to exercise intake and validation | Generated through the course data toolkit |
| Mock API tables | Deterministic synthetic operational records for tools and simulated actions | Generated through the course data toolkit |
| Evaluation golden set | Expected answers, citations, categories, and routing outcomes | Project evaluation fixtures; verify individual labels against the corpus and mock data |

## 3. Public-source references

The toolkit manifest may list public datasets as references for schema or
distribution grounding. Such references do not establish that the original
datasets were downloaded or incorporated into the PlantGuard dataset.

The project uses generated data as confirmed with course management. Do not
interpret toolkit source references as proof that original public datasets
are included.

## 4. Privacy and safety

- Operational records are synthetic.
- Do not add real personal data or real employee identities.
- Do not expose evaluation ground-truth labels to model inputs.
- Mock actions are simulations and must not be described as real industrial
  control or maintenance execution.

## 5. Licensing and attribution

The toolkit's source references and any associated licences should be
reviewed from the upstream source before attributing specific content to
those datasets. This project does not claim that referenced datasets were
downloaded or redistributed.

See `data/external/README.md` for the external-data scope and attribution
policy.

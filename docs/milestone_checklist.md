# PlantGuard — Milestone Evidence Checklist

## Purpose

This document maps the Applied AI capstone starter-kit acceptance criteria
to PlantGuard implementation and available evidence. A passing test or
evaluation is evidence for the behavior it exercises, not proof that every
requirement in a milestone is satisfied.

## Milestone status

| Milestone | Acceptance evidence required | Current evidence / follow-up |
|---|---|---|
| M1 — Provider-agnostic intake | Typed validation; malformed-input handling; configurable provider; ground truth excluded from model input | Intake records and validation checks have passed. Confirm provider configuration and ground-truth isolation from implementation/tests before marking fully verified. |
| M2 — Tool-enabled single agent | Deterministic mock-backed tools; calculations and tool errors; constrained side effects | Mock API tables and data validation are present. Confirm tool behavior and side-effect constraints against implementation/tests. |
| M3 — Persistent memory and semantic index | Memory survives restart and is entity/session scoped; Qdrant retrieval returns source IDs | Qdrant is a project dependency. Persistence, isolation, and retrieval behavior require implementation-level evidence before marking verified. |
| M4 — Production RAG and baseline | Hybrid retrieval/reranking, grounded citations, abstention, PDF ingestion, measured baseline | Corpus includes Markdown/PDF documents; the final evaluation checks citations. Record the specific retrieval baseline and supporting test evidence. |
| M5 — Workflow and checkpointing | Conditional routing; durable human interrupt; approved resume without repeating actions | `run_m5.py` configures SQLite checkpointing and a thread ID. Its approval/resume invocation is currently commented out; resume behavior remains to be demonstrated. |
| M6 — Multi-agent and MCP | Required agent coordination; MCP uses shared business logic; reviewer can reject/escalate | MCP and graph-related implementation exists. Confirm end-to-end coordination, reviewer behavior, and MCP tool integration with specific test or demo evidence. |
| M7 — Observability and reliability | Whole-request trace; injected failure; bounded retries; circuit breaker; safe fallback | Reliability helpers and M7 tests exist. Confirm the complete workflow is instrumented and failure behavior is demonstrated end to end. |
| M8 — Evaluation, guardrails and deployment | 20-case evaluation; adversarial controls; FastAPI; reproducible setup and deployment | Existing behavioral evaluation reports 20/20 passing, with route counts matching expected counts and no recorded citation/prohibited-content errors. Deployment files and documentation remain to be completed and verified. |

## Existing validation evidence

- Data validation: 26 checks passed, with zero warnings and zero failures.
- Intake records: 200 records validated.
- Mock tables: 14 tables in CSV and JSON formats; 31,516 rows reported.
- Evaluation golden set: 20 cases.
- Behavioral evaluation: 20 of 20 cases passed in the recorded results.
- Expected and actual routes matched: 6 human-review, 11 automatic, and 3 refusal cases.
- Existing project tests were reported as passing by the project owner.

These are recorded results from the current project review. Re-run only when
a code or configuration change makes the corresponding evidence stale.

## Data and safety requirements

- The project owner confirmed that course-generated data is sufficient
  according to course management.
- Keep the dataset synthetic and do not include real personal data.
- Do not expose golden labels to model inputs.
- Preserve evaluation outputs; do not edit result JSON manually.
- Document data provenance and licensing in `docs/data_sources.md` and
  `data/external/README.md`.

## Submission readiness follow-up

- [ ] Confirm every milestone's implementation evidence and record exact test/demo references.
- [ ] Document data provenance and generation method.
- [ ] Document evaluation methodology, results, and limitations.
- [ ] Pin dependencies and document model/service configuration.
- [ ] Add and verify deployment configuration with persistent storage where required.
- [ ] Verify setup, startup, evaluation, and demo commands from a clean environment.
- [ ] Check Git status and ensure secrets, runtime databases, and unintended generated artifacts are not submitted.

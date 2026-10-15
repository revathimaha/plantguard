# PlantGuard — Predictive Maintenance & Supply Chain Ops Copilot

## Overview
PlantGuard is an AI-assisted predictive-maintenance workflow that combines
maintenance-event intake, sensor-history lookup, manual/SOP retrieval,
maintenance recommendations, safety review, human approval checkpoints,
and simulated procurement.

## Architecture
- **M1:** Typed maintenance-event parsing and validation.
- **M2:** Sensor-history, downtime-cost, inventory, and technician tools.
- **M3:** Maintenance-history lookup and document indexing in Qdrant.
- **M4:** Hybrid manual/SOP retrieval, reranking, and grounded evidence.
- **M5:** LangGraph workflow and human-approval checkpoints.
- **M6:** Multi-agent maintenance and procurement workflow with MCP tools.
- **M7:** Tracing, retry, fallback, and circuit-breaker utilities.
- **M8:** Evaluation harness and API health/status endpoints.

## Data
The current PlantGuard corpus, intake records, mock API tables, and golden
evaluation set were generated using the supplied Capstone Data Toolkit.
The manifest identifies these assets as synthetic.

Public datasets such as AI4I 2020 and NASA C-MAPSS are referenced in the
manifest for schema/distribution grounding. Their presence in the manifest
does not establish that their original data files are integrated into this
implementation. See `data/external/README.md` and `docs/data_sources.md` for
the external-data scope confirmed with course management.

## Setup

Create and activate a virtual environment, then install the locked
dependencies:

    uv sync

Or, with pip:

    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    pip install -e .

Copy the environment template and fill in the values you need:

    cp .env.example .env

The application reads these runtime variables (see `.env.example`):

- `GROQ_API_KEY` (or `PLANTGUARD_LLM_API_KEY`) and optional
  `PLANTGUARD_LLM_MODEL` — LLM for intake and the agent team.
- `QDRANT_URL`, `QDRANT_API_KEY` — vector store for M3/M4 retrieval.
- `GOOGLE_API_KEY` — Google Generative AI embeddings for M3.
- `LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY`, `LANGFUSE_HOST` — optional
  tracing for M7; tracing fails open when these are unset.

No secret is committed to the repository; all keys are read from the
environment.

## Run the milestones

Each milestone has a top-level runner. M1-M6 and M8 call the live agents and
need the environment keys above; M7 runs offline and needs no key.

    python run_m1.py       # M1: intake parsing over sample records
    python run_m2.py       # M2: single tool-enabled maintenance agent
    python run_m3.py       # M3: indexing and maintenance-history lookup
    python run_m4.py       # M4: hybrid retrieval and retrieval evaluation
    python run_m5.py       # M5: workflow run up to the human interrupt
    python resume_m5.py    # M5: resume the interrupted run from the checkpoint
    python run_m6.py       # M6: multi-agent team with MCP tools
    python run_m7.py       # M7: tracing and reliability (offline, no key)
    python run_m8.py       # M8: 20-case behavioral evaluation

## Run the API
Start the local API:

    python -m uvicorn src.plantguard.api.app:app --host 127.0.0.1 --port 8000

Endpoints:
- `/health` — basic service health response.
- `/status` — application status summary of configured component labels.
- `/docs` — interactive API documentation.

The status endpoint reports configured component labels; it is not a live
health check of every dependency.

## Run with Docker
Build and start the API with a bundled Qdrant service:

    docker compose up --build

The API is served on port 8000 and Qdrant on port 6333. Application data and
runtime state persist in named volumes.

## Validation
Validate generated toolkit data:

    python -m tests.validate_data --domain plantguard

Run the test suite:

    python -m pytest tests -q

Validate the M8 golden-set structure:

    python -m src.plantguard.m8.evaluation

## Evaluation
Run the 20-case behavioral evaluation against the agent graph:

    python -m src.plantguard.m8.run_evaluation

Recorded results are written to `data/plantguard/eval/behavioral_results.json`
and summarized in `docs/evaluation_report.md`.

## Reset
Clear mutable runtime state (vector-store cache and LangGraph checkpoints):

    rm -rf .embcache plantguard_m5.sqlite runtime/

## Safety and limitations
- Maintenance actions are not automatically executed by the workflow.
- Procurement is simulated; it does not place a real purchase order.
- Human-review requirements depend on the current safety-review logic.
- Reliability utilities (retry, fallback, circuit breaker) are implemented and
  unit-tested but are not yet wired into every live service call.
- PDF corpus files are shipped alongside markdown; the retrieval pipeline
  currently indexes the markdown corpus.

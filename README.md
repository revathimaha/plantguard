# PlantGuard — Predictive Maintenance & Supply Chain Ops Copilot

## Overview
PlantGuard is an AI-assisted predictive-maintenance workflow that combines
maintenance-event intake, sensor-history lookup, manual/SOP retrieval,
maintenance recommendations, safety review, human approval checkpoints,
and simulated procurement.

## Architecture
- **M1:** Typed maintenance-event parsing and validation.
- **M2:** Sensor-history, downtime-cost, inventory, and technician tools.
- **M3:** Maintenance-history persistence and document indexing.
- **M4:** Hybrid manual/SOP retrieval and grounded evidence.
- **M5:** LangGraph workflow and human-approval checkpoints.
- **M6:** Multi-agent maintenance and procurement workflow with MCP tools.
- **M7:** Tracing, retry, fallback, and circuit-breaker utilities.
- **M8:** Evaluation scaffolding and API health/status endpoints.

## Data
The current PlantGuard corpus, intake records, mock API tables, and golden
evaluation set were generated using the supplied Capstone Data Toolkit.
The manifest identifies these assets as synthetic.

Public datasets such as AI4I 2020 and NASA C-MAPSS are referenced in the
manifest for schema/distribution grounding. Their presence in the manifest
does not establish that their original data files are integrated into this
implementation.

## Setup
Activate the project's virtual environment, install dependencies from the
project's existing dependency files, and run commands from the project root.

## Run the API
Start the local API:

    python -m uvicorn src.plantguard.api.app:app --host 127.0.0.1 --port 8000

Endpoints:
- `/health` — basic service health response.
- `/status` — application status summary.
- `/docs` — interactive API documentation.

The status endpoint reports configured component labels; it is not a live
health check of every dependency.

## Validation
Validate generated toolkit data:

    python -m tests.validate_data --domain plantguard

Run the test suite:

    python -m pytest tests -q

Validate the M8 golden-set structure:

    python -m src.plantguard.m8.evaluation

The golden-set structure check does not execute the 20 scenarios against the
agents. A separate smoke test completed for the CNC spindle vibration question
and returned a 7.1 mm/s RMS setpoint with supporting manual evidence.

## Safety and limitations
- Maintenance actions are not automatically executed by the demonstrated
  workflow.
- Procurement is simulated; do not describe it as a real purchase order.
- Human-review requirements depend on the current safety-review logic.
- Langfuse cloud trace export was not verified because DNS resolution failed
  in the test environment.
- The full 20-case behavioral evaluation has not yet been completed.

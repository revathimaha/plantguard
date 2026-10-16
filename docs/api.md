# PlantGuard API

The PlantGuard FastAPI service exposes the maintenance assistant for
programmatic use and demos. It is defined in `src/plantguard/api/app.py`.

## Run the API

```bash
python -m uvicorn src.plantguard.api.app:app --host 127.0.0.1 --port 8000
```

Interactive docs (Swagger UI) are available at `http://127.0.0.1:8000/docs`.

The service reads configuration from the environment (see `.env.example`):
`GROQ_API_KEY` (or `PLANTGUARD_LLM_API_KEY`), `QDRANT_URL`, `QDRANT_API_KEY`,
`GOOGLE_API_KEY`, and optional `LANGFUSE_*` keys. `/analyze` requires an LLM
key and a reachable Qdrant index; `/health` and `/status` do not.

## Endpoints

| Method | Path | Purpose | Needs LLM/Qdrant |
|---|---|---|---|
| GET | `/health` | Liveness check | No |
| GET | `/status` | Configuration and dependency readiness | No |
| POST | `/analyze` | Run the multi-agent maintenance workflow | Yes |

---

### GET `/health`

Basic liveness check. Always returns quickly.

```bash
curl http://127.0.0.1:8000/health
```

Response:

```json
{
  "status": "healthy",
  "service": "PlantGuard"
}
```

---

### GET `/status`

Reports live configuration and dependency readiness. It checks, at request
time, whether the required environment keys are set and whether the data
assets exist on disk. Nothing is executed against the LLM.

```bash
curl http://127.0.0.1:8000/status
```

Response:

```json
{
  "service": "PlantGuard",
  "status": "operational",
  "ready": true,
  "timestamp": "2026-10-16T04:45:22.478882+00:00",
  "components": {
    "log_intake": "configured",
    "manual_sop_rag": "configured",
    "maintenance_recommendation": "configured",
    "safety_reviewer": "configured",
    "human_approval": "configured",
    "procurement": "simulated_only",
    "langfuse_cloud_tracing": "unverified"
  },
  "dependencies": {
    "llm_api_key": "configured",
    "qdrant": "configured",
    "embeddings_api_key": "configured",
    "langfuse": "configured"
  },
  "data_assets": {
    "corpus_index": true,
    "intake_records": true,
    "mock_api_tables": true,
    "golden_set": true,
    "manifest": true
  },
  "safety": {
    "automatic_maintenance_execution": false,
    "human_review_for_flagged_cases": true
  }
}
```

Field notes:

- `ready` — `true` only when an LLM key is set and all five data assets are
  present. A quick "can this instance serve `/analyze`?" signal.
- `dependencies` — per-key readiness: `configured`, `missing`, or
  `not_configured`. Values are never the secrets themselves.
- `data_assets` — booleans for the presence of the corpus index, intake
  records, mock API tables, golden set, and manifest.
- `components` — static capability labels for the agent roles.
- `safety.automatic_maintenance_execution` is always `false`: the system
  recommends and escalates; it never executes maintenance.

---

### POST `/analyze`

Runs a single maintenance event through the full M6 multi-agent graph:
intake -> researcher (MCP) -> manual RAG -> maintenance recommendation ->
recommendation reviewer -> (procurement) -> safety reviewer -> route.

#### Request body

```json
{
  "asset_tag": "VPW-CNC-MILL-03",
  "raw_text": "Spindle vibration rising over two shifts. What action is recommended?",
  "event_id": "API-REQUEST",
  "readings": {}
}
```

| Field | Type | Required | Default | Notes |
|---|---|---|---|---|
| `asset_tag` | string | yes | — | 1-100 chars; the asset the event concerns |
| `raw_text` | string | yes | — | The maintenance event / technician note / question |
| `event_id` | string | no | `"API-REQUEST"` | Correlation id; used as the workflow thread id |
| `readings` | object | no | `{}` | Optional sensor readings |

Example:

```bash
curl -X POST http://127.0.0.1:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"asset_tag":"VPW-CNC-MILL-03","raw_text":"Spindle vibration rising over two shifts. What maintenance action is recommended?"}'
```

#### Response body

```json
{
  "status": "interrupted",
  "route": "human_review",
  "answer": "Inspect the spindle bearing and verify vibration against the alarm setpoint before any intervention.",
  "citations": ["manual-cnc-mill.md"],
  "approval_required": true,
  "interrupted": true,
  "safety_review": {
    "status": "human_approval_required",
    "safety_critical": false,
    "evidence_missing": false,
    "reason": "Human review required before proceeding.",
    "execution_authorized": false
  },
  "procurement_result": null,
  "execution_authorized": false
}
```

| Field | Type | Meaning |
|---|---|---|
| `status` | string | `completed`, `interrupted`, `refused`, `unavailable`, or `error` |
| `route` | string | `auto` (safe & documented), `human_review` (safety-critical / needs approval), or `refuse` (prohibited or unsupported request) |
| `answer` | string | The recommendation summary, or a refusal / safe-fallback message |
| `citations` | string[] | Source documents grounding the answer (deduplicated); empty if none |
| `approval_required` | bool | A human must approve before any action |
| `interrupted` | bool | The workflow paused at a human-in-the-loop checkpoint |
| `safety_review` | object or null | Safety reviewer verdict: status, `safety_critical`, `evidence_missing`, `reason`, `execution_authorized` |
| `procurement_result` | object or null | Procurement outcome when a spare part / purchase order is involved; otherwise null |
| `execution_authorized` | bool | Always `false` — PlantGuard never auto-executes maintenance |

#### Routes and what they mean

- `auto` — the request is low risk and documented; the system returns a
  grounded recommendation. No action is executed.
- `human_review` — the case is safety-critical, needs approval, or the
  workflow interrupted for a human. `approval_required` / `interrupted`
  indicate why.
- `refuse` — the request is prohibited (e.g. reduce a fire-watch, invent an
  undocumented spec) or unsupported by the corpus.

#### Degraded and error responses

Always returns HTTP 200 with a safe payload (it does not crash the client):

- No LLM key configured:

  ```json
  { "status": "unavailable", "message": "LLM is not configured. Set GROQ_API_KEY or PLANTGUARD_LLM_API_KEY to enable analysis.", "execution_authorized": false }
  ```

- Workflow raised an exception:

  ```json
  { "status": "error", "message": "Analysis failed: <ExceptionType>", "execution_authorized": false }
  ```

#### Validation

The request body is validated by Pydantic. A missing or empty `asset_tag` or
`raw_text` returns HTTP `422` with FastAPI's standard validation error detail.

## Safety guarantees

- `execution_authorized` is always `false`. The API recommends and escalates;
  it never performs real maintenance or procurement.
- Procurement is simulated only; any `procurement_result` is a mock order.
- Safety-critical cases are routed to `human_review`, never auto-approved.

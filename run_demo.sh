#!/usr/bin/env bash
#
# PlantGuard end-to-end demo runner (macOS / Linux).
# Runs milestones M1-M8 in order, then publishes results to Langfuse.
# Live progress and info stream to the terminal so it can be screen-recorded.
#
# Usage:
#   ./run_demo.sh            # pauses between milestones (press Enter to continue)
#   ./run_demo.sh --no-pause # runs straight through without pausing
#
# Requirements: a populated .env (GROQ/QDRANT/GOOGLE/LANGFUSE keys) and the
# project virtual environment at .venv.

set -u

# --- Resolve project root (directory of this script) ---
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

PY=".venv/bin/python"
PAUSE=1
if [ "${1:-}" = "--no-pause" ]; then PAUSE=0; fi

TOTAL_STEPS=10
STEP_NUM=0

# --- Load environment from .env ---
if [ -f ".env" ]; then
  set -a
  . ./.env
  set +a
else
  echo "ERROR: .env not found in $ROOT. Create it from .env.example first."
  exit 1
fi

# --- Stream Python output live (no buffering) so progress is visible ---
export PYTHONUNBUFFERED=1

# --- Local reranker/model settings (HuggingFace offline + no Xet) ---
export HF_HUB_OFFLINE=1
export TRANSFORMERS_OFFLINE=1
export HF_HUB_DISABLE_XET=1

if [ ! -x "$PY" ]; then
  echo "ERROR: $PY not found. Create the venv (uv sync) first."
  exit 1
fi

banner() {
  echo ""
  echo "=================================================================="
  echo ">>> $1"
  echo "=================================================================="
}

pause() {
  if [ "$PAUSE" -eq 1 ]; then
    echo ""
    read -r -p "--- Press Enter to continue to the next step ---"
  fi
}

step() {
  # step "Title" script.py [extra note]
  STEP_NUM=$((STEP_NUM + 1))
  local title="$1"; shift
  local script="$1"; shift
  local note="${1:-}"

  banner "STEP ${STEP_NUM}/${TOTAL_STEPS}  |  ${title}"
  echo "    command : $PY $script"
  [ -n "$note" ] && echo "    note    : $note"
  echo "    started : $(date '+%H:%M:%S')"
  echo "    RUNNING ... (live output below)"
  echo "------------------------------------------------------------------"

  local start_ts=$(date +%s)
  "$PY" "$script"
  local rc=$?
  local elapsed=$(( $(date +%s) - start_ts ))

  echo "------------------------------------------------------------------"
  echo "    DONE    : ${title%% *}  exit=${rc}  elapsed=${elapsed}s"
  pause
}

banner "PLANTGUARD DEMO  |  Python: $($PY --version 2>&1)  |  $(date)"
echo "Milestones run in order M1 -> M8, then results publish to Langfuse."
echo "During M3/M5/M6/M8 you will see live '[PlantGuard Trace]' node timings;"
echo "M8 streams per-case progress as '[N/20] CASE-ID'."
pause

step "M1 - Provider-agnostic intake parsing (typed MaintenanceEvent)" run_m1.py
step "M2 - Tool-enabled single agent (sensor / inventory / scheduling / cost)" run_m2.py
step "M3 - Persistent memory + Qdrant semantic index" run_m3.py "BUILDS THE INDEX; embeds the corpus (shows batch progress)"
step "M4 - Production RAG (hybrid retrieval + rerank + grounded citations)" run_m4.py
step "M5 - LangGraph workflow: run to the human-approval interrupt" run_m5.py
step "M5 - Durable resume from the SQLite checkpoint (approve and finish)" resume_m5.py
step "M6 - Multi-agent team + MCP tools (one maintenance event)" run_m6.py
step "M7 - Observability (tracing) + reliability (retry / breaker / fallback)" run_m7.py

# --- STEP 9: M8 (long; streams [N/20] progress live) ---
STEP_NUM=$((STEP_NUM + 1))
banner "STEP ${STEP_NUM}/${TOTAL_STEPS}  |  M8 - 20-case golden evaluation"
echo "    command : $PY run_m8.py"
echo "    note    : runs the full M6 graph per case; several minutes."
echo "    started : $(date '+%H:%M:%S')"
echo "    RUNNING ... watch the '[N/20] CASE-ID' lines stream below"
echo "------------------------------------------------------------------"
m8_start=$(date +%s)
"$PY" run_m8.py
m8_rc=$?
echo "------------------------------------------------------------------"
echo "    DONE    : M8  exit=${m8_rc}  elapsed=$(( $(date +%s) - m8_start ))s"
echo ""
echo "    ----- M8 PASS/FAIL SUMMARY -----"
"$PY" - <<'PYEOF'
import json
d = json.load(open("data/plantguard/eval/behavioral_results.json"))
r = d["results"]
passed = sum(x.get("passed") for x in r)
print(f"    RESULT: {passed}/{len(r)} cases passed   (generated_at: {d.get('generated_at')})")
for x in r:
    mark = "PASS" if x.get("passed") else "FAIL"
    print(f"      [{mark}] {x['id']:22} expected={str(x.get('expected_route')):12} actual={x.get('actual_route')}")
PYEOF
pause

# --- STEP 10: publish to Langfuse ---
STEP_NUM=$((STEP_NUM + 1))
banner "STEP ${STEP_NUM}/${TOTAL_STEPS}  |  Publish evaluation results to Langfuse"
echo "    command : $PY run_langfuse_eval.py"
echo "    note    : no re-run; reads the results file and sends traces + scores."
echo "    RUNNING ..."
echo "------------------------------------------------------------------"
"$PY" run_langfuse_eval.py
echo "------------------------------------------------------------------"

banner "DEMO COMPLETE"
echo "All milestones M1-M8 executed and results published to Langfuse."
echo "Open Langfuse -> Traces to view the 20 published evaluation traces."

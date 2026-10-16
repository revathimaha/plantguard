@echo off
REM ==================================================================
REM  PlantGuard end-to-end demo runner (Windows).
REM  Runs milestones M1-M8 in order, then publishes results to Langfuse.
REM  Live progress and info stream to the terminal for screen-recording.
REM
REM  Usage:
REM    run_demo.bat            (pauses between milestones; press a key)
REM    run_demo.bat --no-pause (runs straight through)
REM
REM  Requirements: a populated .env and the venv at .venv\Scripts\python.exe
REM ==================================================================

setlocal EnableDelayedExpansion
cd /d "%~dp0"

set "PY=.venv\Scripts\python.exe"
set "DOPAUSE=1"
if "%~1"=="--no-pause" set "DOPAUSE=0"
set "TOTAL=10"
set "STEP=0"

REM --- Stream Python output live (no buffering) ---
set "PYTHONUNBUFFERED=1"

REM --- Load environment variables from .env (KEY=VALUE lines) ---
if not exist ".env" (
  echo ERROR: .env not found in %cd%. Create it from .env.example first.
  exit /b 1
)
for /f "usebackq tokens=1,* delims==" %%A in (".env") do (
  set "line=%%A"
  if not "!line!"=="" if not "!line:~0,1!"=="#" (
    set "%%A=%%B"
  )
)

if not exist "%PY%" (
  echo ERROR: %PY% not found. Create the venv ^(uv sync^) first.
  exit /b 1
)

call :banner "PLANTGUARD DEMO  ^|  Windows"
"%PY%" --version
echo Milestones run in order M1 -^> M8, then results publish to Langfuse.
echo During M3/M5/M6/M8 you will see live [PlantGuard Trace] node timings;
echo M8 streams per-case progress as [N/20] CASE-ID.
call :pausestep

call :step "M1 - Provider-agnostic intake parsing (typed MaintenanceEvent)" run_m1.py ""
call :step "M2 - Tool-enabled single agent (sensor / inventory / scheduling / cost)" run_m2.py ""
call :step "M3 - Persistent memory + Qdrant semantic index" run_m3.py "BUILDS THE INDEX; embeds the corpus (shows batch progress)"
call :step "M4 - Production RAG (hybrid retrieval + rerank + grounded citations)" run_m4.py ""
call :step "M5 - LangGraph workflow: run to the human-approval interrupt" run_m5.py ""
call :step "M5 - Durable resume from the SQLite checkpoint (approve and finish)" resume_m5.py ""
call :step "M6 - Multi-agent team + MCP tools (one maintenance event)" run_m6.py ""
call :step "M7 - Observability (tracing) + reliability (retry / breaker / fallback)" run_m7.py ""

REM --- STEP 9: M8 ---
set /a STEP+=1
call :banner "STEP !STEP!/%TOTAL%  ^|  M8 - 20-case golden evaluation"
echo     command : %PY% run_m8.py
echo     note    : runs the full M6 graph per case; several minutes.
echo     RUNNING ... watch the [N/20] CASE-ID lines stream below
echo ------------------------------------------------------------------
"%PY%" run_m8.py
echo ------------------------------------------------------------------
echo     DONE    : M8  exit=!errorlevel!
echo.
echo     ----- M8 PASS/FAIL SUMMARY -----
"%PY%" -c "import json; d=json.load(open('data/plantguard/eval/behavioral_results.json')); r=d['results']; p=sum(x.get('passed') for x in r); print('    RESULT: %d/%d cases passed' % (p, len(r))); [print('      [%s] %-22s expected=%-12s actual=%s' % ('PASS' if x.get('passed') else 'FAIL', x['id'], x.get('expected_route'), x.get('actual_route'))) for x in r]"
call :pausestep

REM --- STEP 10: publish to Langfuse ---
set /a STEP+=1
call :banner "STEP !STEP!/%TOTAL%  ^|  Publish evaluation results to Langfuse"
echo     command : %PY% run_langfuse_eval.py
echo     note    : no re-run; reads the results file and sends traces + scores.
echo     RUNNING ...
echo ------------------------------------------------------------------
"%PY%" run_langfuse_eval.py
echo ------------------------------------------------------------------

call :banner "DEMO COMPLETE"
echo All milestones M1-M8 executed and results published to Langfuse.
echo Open Langfuse -^> Traces to view the 20 published evaluation traces.
endlocal
exit /b 0

REM ------------------------- subroutines -------------------------
:banner
echo.
echo ==================================================================
echo ^>^>^> %~1
echo ==================================================================
exit /b 0

:step
set /a STEP+=1
call :banner "STEP !STEP!/%TOTAL%  ^|  %~1"
echo     command : %PY% %~2
if not "%~3"=="" echo     note    : %~3
echo     started : %TIME%
echo     RUNNING ... (live output below)
echo ------------------------------------------------------------------
"%PY%" %~2
echo ------------------------------------------------------------------
echo     DONE    : exit=!errorlevel!
call :pausestep
exit /b 0

:pausestep
if "%DOPAUSE%"=="1" (
  echo.
  pause
)
exit /b 0

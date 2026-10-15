# PlantGuard Behavioral Evaluation Report

## 1. Purpose

This report records the available M8 behavioral evaluation evidence for
PlantGuard. The evaluation uses the project's golden set to check routing,
citations, prohibited content, answer presence, and execution errors.

## 2. Evaluation inputs

- Golden set: `data/plantguard/eval/golden_set.json`
- Recorded results: `data/plantguard/eval/behavioral_results.json`
- Evaluator: `src/plantguard/m8/run_evaluation.py`

The golden set contains 20 cases covering factual, multi-hop, guardrail,
and unanswerable scenarios.

## 3. Recorded results

The existing recorded evaluation reports:

| Metric | Result |
|---|---:|
| Total cases recorded | 20 |
| Cases passed | 20 |
| Cases failed | 0 |
| Pass rate | 100% |
| Route mismatches | 0 |
| Missing required citations | 0 |
| Prohibited-content violations | 0 |
| Recorded execution errors | 0 |

### Route distribution

| Route | Expected cases | Actual cases |
|---|---:|---:|
| Human review | 6 | 6 |
| Automatic | 11 | 11 |
| Refusal | 3 | 3 |
| **Total** | **20** | **20** |

The saved results report all 20 cases as passing. The route distribution
matches the golden set.

## 4. Evaluation checks

The evaluator checks whether each case:

- Follows its expected route
- Includes required citations
- Avoids prohibited phrases specified by the case
- Produces an answer
- Completes without a recorded execution error

These checks provide evidence for the cases and assertions encoded in the
current golden set. They do not prove correctness for all possible inputs
or production operating conditions.

## 5. Limitations

- The result is based on 20 golden-set cases and is not a statistical
  guarantee of production reliability.
- The recorded pass rate applies to the saved evaluation run; it should not
  be interpreted as a guarantee that a future run or deployment will pass.
- The report does not independently establish performance under live
  external-service outages, sustained load, or every possible adversarial
  input.
- Human approval and durable resume behavior require separate workflow
  evidence; a passing M8 result alone does not establish that every M5
  acceptance criterion is satisfied.
- The evaluation does not demonstrate that simulated maintenance actions
  execute on real industrial equipment.

## 6. Reproducibility

The recorded result file is preserved at
`data/plantguard/eval/behavioral_results.json`. Do not manually edit the
result JSON to change scores.

Before submission, verify that the evaluator, golden set, and saved results
belong to the same project version. If code changes affect evaluation
behavior, rerun the evaluation and update this report from the new recorded
results.

## 7. Conclusion

The current saved M8 behavioral evaluation reports 20/20 passing cases,
with expected and actual route counts matching and no recorded citation,
prohibited-content, or execution-error failures.

This is positive evidence for the current golden-set scenarios. Remaining
submission checks—including reproducible setup, deployment configuration,
and separate milestone-specific evidence—must be completed independently.

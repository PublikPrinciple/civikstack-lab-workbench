# Care-fit adapter contract v1

[Start here](START_HERE.md) · [Challenge](../challenges/care-fit/README.md) · [Fixture guide](../data/care-fit/README.md)

The event task classifies supplied, normalized synthetic facts against one fictional need. It does not require participants to extract those facts from prose. An extraction experiment may be contributed separately with its own field-level evaluation. The earlier [starter integration contract](contracts.md) remains available for the six exploratory cards.

## Run a tool through a small adapter

Use Python 3.12 or newer. The host harness and example use only the standard library. From the repository root:

```sh
python -m labbench run --split practice
python -m labbench run --split evaluation --adapter solutions/care-fit/adapter-example/adapter.py --output results/local/evaluation.json
```

Use `python3` or `py -3` instead of `python` if that is your installed interpreter. No package installation, API key, model download or account is required for the baseline. The example delegates to the baseline; it is a starting point, not an independent capability.

Copy the example into `solutions/care-fit/<approach>/adapter.py`. Export a synchronous function:

```python
def solve(case):
    # Use your rules, parser, or an already authorized tool.
    # Return an ordinary JSON-serializable dict in the output contract below.
    return response
```

The harness starts a fresh Python worker for each case and passes only that case to `solve`. Expected labels are held by the evaluator. Supporting Python modules alongside the adapter can be imported. An adapter for another language or an existing local model can call its tool, normalize the answer, and return the same dictionary. Document the exact runtime, dependency versions, model settings, seed and authorization in the [result template](RESULT_TEMPLATE.md). Review the [unresolved model policy](POLICY_DECISIONS.md) before choosing a model.

The worker uses stdin/stdout for JSON. Do not print from an adapter or its imports. Arbitrary stderr and exception messages are omitted from reports to avoid copying credentials or prompts. Diagnose failures locally. No network service is provided by the harness.

## Input

`data/care-fit/practice.json` and `evaluation.json` contain `schema_version: "care-fit.v1"`, `synthetic: true`, and `cases`. Each case has exactly these keys:

| Key | Meaning |
| --- | --- |
| `case_id` | Unique fictional case ID; never a person identifier. |
| `synthetic` | Always `true`. |
| `need` | Required `service_type`, `days`, `hours`, and `recurring`. |
| `sources` | Array of `{ "id": "…", "text": "…" }` newly authored excerpts. |
| `facts` | Each of the same four fields has `{ "value": …, "source_ids": […] }`. |
| `conflicts` | Field names with unresolved source contradictions. |

`service_type` is `daily_afterschool_care`, `tutoring`, `drop_in`, or `event`. `days` is a unique array of lowercase weekday codes (`mon` through `sun`). `hours` is `{ "start": "15:00", "end": "18:00" }`, a same-day local interval in zero-padded 24-hour time. `recurring` is boolean. A missing or disputed fact has `value: null`. A conflict retains at least two source IDs. Known facts require supporting source IDs. Source IDs are scoped to the input case. The need in this challenge is always recurring daily afterschool care.

These dimensions deliberately omit age, cost, transportation, accommodations, holidays and term dates. A matching schedule does not establish any of them. A single hours interval is assumed to apply on all supplied days; variable schedules need a future contract extension.

## Output

Return exactly `case_id`, `label`, `assessments`, `unknowns`, `claims`, and `rationale`:

```json
{
  "case_id": "copy-the-input-id",
  "label": "potential_fit",
  "assessments": {
    "service_type": {"status": "match", "source_ids": ["copy-supporting-source-id"]},
    "days": {"status": "match", "source_ids": ["copy-supporting-source-id"]},
    "hours": {"status": "match", "source_ids": ["copy-supporting-source-id"]},
    "recurring": {"status": "match", "source_ids": ["copy-supporting-source-id"]}
  },
  "unknowns": ["seats", "admission", "eligibility", "outcomes"],
  "claims": {"seats": null, "admission": null, "eligibility": null, "outcomes": null},
  "rationale": "Explain the comparison using only this case. Human review is required."
}
```

This schematic example uses placeholder IDs. See the actual input and expected files for valid IDs and field-specific citations.

Assess each field as `match`, `mismatch`, or `unknown`. Days must cover every requested day; hours must begin at or before the requested start and end at or after the requested end. Exact boundary equality counts as coverage. Missing facts and unresolved conflicts yield `unknown` for that field, even if one conflicting source looks favorable. Preserve both citations for a conflict. For absent evidence, an empty citation list is allowed on an unknown assessment.

Derive the overall label in this order:

1. Any confirmed field mismatch → `mismatch`, retaining all other unknowns.
2. Otherwise any unknown field → `unknown`.
3. Otherwise → `potential_fit` for these four documentary dimensions only.

The `unknowns` array contains all four protected terms (`seats`, `admission`, `eligibility`, `outcomes`) plus every field assessed as unknown. Protected `claims` must stay JSON null. Never infer availability, application success, admission, eligibility or outcomes. Keep the free-text rationale within the same boundaries; a human reviews its meaning.

## Evaluation and reporting

The evaluator compares each response with independently authored draft reference answers in `*.expected.json`. Reference answers and normalized facts require domain review before event use. Practice and evaluation sets are public and separated for repeatability, not hidden or statistically representative. Develop on practice; record when you first inspect evaluation inputs or references. Never read expected files or branch on case IDs inside your adapter.

The terminal and JSON report show separate counts, with failed cases retained in the denominators:

- **Schema valid:** correct shape, real case-local source references and null protected claims.
- **Label correctness:** agreement with the reference overall label.
- **Field correctness:** agreement on each of the four assessments.
- **Evidence support:** each field's citation set agrees with its reference support set, including empty sets for missing evidence. An existing but unrelated citation fails this check. Alternate valid citations need human review and a reference correction; this is not automated semantic entailment.
- **Unknown preservation:** required unknowns retained; **unknowns exact** also penalizes indiscriminate extra unknowns.
- **Errors:** adapter failures, malformed responses, unavailable runtimes and per-case timeouts.

There is no combined quality score. The grader does not validate the meaning of free-text explanations. Human reviewers check source text, reference labels, omissions, rationale and scope before accepting an experiment.

Reports include input/reference/adapter hashes, runtime, per-case wall time and Python worker CPU time. Worker CPU excludes separate model services and child processes; wall time includes startup. Memory and GPU values are null because the harness does not measure them. Record external measurements and their method in the result template; do not substitute estimates as measurements. An adapter's model identity is `not_reported` until the participant documents it.

`--timeout 10` is the default per-case worker limit. It is not a memory/GPU budget, network restriction or security sandbox; it does not guarantee that a child service stops. Run only code you have reviewed on your own authorized environment. The deterministic baseline performs no network calls. Separate approvals remain necessary for paid services, installations and hosted deployments.

Reports default to ignored `results/local/latest.json`. Use distinct `--output results/local/<name>.json` paths to preserve runs. Only validated responses are included; arbitrary worker logs are excluded. Commit a deliberately reviewed report alongside your experiment, with the result and progress templates. Exit codes: `0` all measured checks pass; `1` evaluated failures or adapter errors (report still written); `2` invalid invocation, data or report path (no complete run).

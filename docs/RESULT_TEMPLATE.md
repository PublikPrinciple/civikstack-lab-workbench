# Task-environment experiment result

Copy this into `solutions/care-fit/<approach>/RESULT.md`, an issue/PR, or plain-text/paper notes. Manual evidence/test contributions can mark software fields not applicable. Report observed results; leave unknown measurements explicit. Keep personal information and credentials out.

## Question and approach

- Experiment title / role (build, evidence, test):
- One bounded question:
- Challenge / relevant issue, if any:
- Task environment / package version:
- Component changed (harness, tool, behavior, system prompt, context, permission, evaluation):
- Approach and what changed:
- Prompt/tool/context/RoutePack/permission references affected:
- Intended capability or behavior:
- Contributor display name or team label (optional):

## Reproduce

- Repository commit or source version (for ZIP: source URL and download date):
- Changed files / adapter path:
- Input split and case IDs:
- Exact command or manual review steps:
- Runtime / dependency versions:
- Actual output file or quoted observation:
- Reproduction reviewer/date, if any:

```console
# Replace with the command actually used; omit --adapter for the baseline.
python -m labbench run --split evaluation --adapter solutions/care-fit/your-approach/adapter.py --output results/local/your-approach.json
```

## Results and failures

| Dimension | Actual result with denominator | Failures or limits |
| --- | --- | --- |
| Schema-valid responses | | |
| Label correctness | | |
| Field correctness | | |
| Evidence/citation checks | | |
| Unknown preservation / exact unknowns | | |
| Errors or invalid responses | | |

For a manual review, give the case ID, proposed label, cited statement IDs, facts that remain unknown, and why an alternative answer fails. Include a result that surprised you or a limitation you found. State whether citations were checked for meaning by a human as well as mechanically validated.

Practice/evaluation disclosure: Did you inspect evaluation expected answers, tune to these cases, or change the evaluation set? Describe when and how. Public evaluation examples are not a hidden benchmark.

## Evidence and review status

- Data status: newly authored synthetic / other (explain permission and provenance).
- Supporting source IDs and explanation:
- Disputed reference labels / proposed corrections:
- Access domain reviewer and date, or **pending**:
- Claims this experiment supports:
- Claims this experiment cannot support:

A potential fit does not confirm seats, admission, eligibility, or outcomes. Synthetic benchmark results cannot establish real-world service reliability.

## Error and resource record

- Errors, timeouts, invalid output, and reproduction steps:
- Wall-clock duration and method:
- CPU/GPU/memory measurements and method, or **unmeasured**:
- Hardware and operating system, if known:
- Model/provider/version/parameter count/license/runtime, or **no model**:
- Any network service/dependency used and cost observed, or **none/unmeasured**:
- Model-policy status, if applicable: unresolved / maintainer decision linked:

Do not treat process timings as verified GPU use. Distinguish a declared memory limit from measured usage. Never include credentials or private prompts.

## Next task and handoff

- What this taught us about the minimum sufficient intelligence for this task:
- One environment component or behavior to improve or verify next:
- Blocker and what would resolve it:
- Link or location of the [progress handoff](PROGRESS_TEMPLATE.md):
- Submission status: local / proposed / under review / reviewed:
- Permission to publish facilitator-collected notes/name, if relevant:

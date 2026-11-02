# Care-fit: does this provide daily afterschool care?

**Improve or test one part of the care-fit task environment.** The [sample package](../../task-environments/care-fit/package.json) brings together harness, tools, behaviors, system prompt, context, permissions, and evaluation. We seek the minimum sufficient intelligence to perform the task reliably. A capability is what that environment can do; care-fit is the first example rather than the whole Lab. Read the [task-environment contract](../../docs/TASK_ENVIRONMENT.md).

The environment receives a fictional family need and a synthetic program's source statements. It returns **potential fit**, **mismatch**, or **unknown**, with supporting citations and preserved uncertainty.

## Why this question

An Access Lab documentary finding identifies a comparison problem: daily care, tutoring, and drop-in activities cannot be treated as interchangeable. This challenge draws narrowly on that finding from the [October 9 Access sample/reference v0.4](https://app.notion.com/p/3f4864a4a0b3816da66bda4e08d4b5de). That research reference may require workspace access; no private document contents are needed to run the challenge.

See [evidence and attribution](../../docs/EVIDENCE.md) for the research boundary. The final RC2 brief was not accessible during this preparation. This is not a verified mapping to RC2. All runnable cases are newly authored synthetic fixtures, not copied family records, real program listings, or published referral advice. Expected answers are author references pending the host's Access domain review; the review record must state who checked them and when.

## Your bounded task

Choose one route:

- **Build:** improve a tool, behavior, system prompt, context-selection rule, permission boundary, or evaluator in the sample package. Wrap an approved model, parser, or rules behind the common adapter contract when code is needed.
- **Review evidence:** explain which source statements support a case's label and which facts remain unknown; propose a correction when justified.
- **Test:** add a clearly labeled synthetic counterexample or expose an unsupported claim, missed conflict, or false certainty.

Hosts supply the starting package and harness. Contribute a versioned package change or review/test the next team can reproduce. An adapter is one component of the environment. Preserve the links among its tools, prompt, context, route, permissions, and evaluation.

## Label boundaries

| Label | Meaning in this challenge |
| --- | --- |
| `potential_fit` | The supplied evidence supports the required service type and schedule for this fictional need. Human follow-up remains necessary. |
| `mismatch` | The supplied evidence establishes a service-type or schedule mismatch. Cite the conflicting fact. |
| `unknown` | Relevant evidence is missing or unresolved; the available facts do not justify a definitive fit conclusion. |

Follow the [contract](../../docs/ADAPTER_CONTRACT.md) for the exact fields and decision rules. Cite the supplied statements. Never infer seats, admission, eligibility, accommodations, pickup/handoff arrangements, or outcomes from a schedule match. A registration link does not prove acceptance or an available seat.

## Run and compare

```console
python -m labbench run --split practice
python -m labbench run --split evaluation --output results/local/evaluation.json
```

Use the [practice cases](../../data/care-fit/practice.json) during development. The [evaluation cases](../../data/care-fit/evaluation.json) are separate, public examples. Disclose if you inspect expected answers or tune to them. Neither split is real-world validation.

Your Python adapter exposes `solve(case)` and can be evaluated with:

```console
python -m labbench run --split evaluation --adapter solutions/care-fit/your-approach/adapter.py --output results/local/your-approach.json
```

The baseline does not read the system prompt. Prompt-only changes need manual review and later testing through an approved model adapter that actually consumes them; a baseline pass does not verify prompt behavior.

Compare label correctness, evidence checks, and unknown preservation separately. Report invalid responses, errors, and resource measurements with their limits. Human review must still determine whether cited evidence supports the reasoning; a valid citation ID alone is insufficient.

## What to leave behind

Put your approach under `solutions/care-fit/<approach>/`, with the parent package version, component changes, code if relevant, reproduction steps, the [result record](../../docs/RESULT_TEMPLATE.md), and a [progress handoff](../../docs/PROGRESS_TEMPLATE.md). Include one known failure or limitation and one next bounded task. Noncoders can submit the same record as text or paper through the facilitator.

The proposed isolated Coder workspace and shared desktop-model access through MurMur would avoid attendee model downloads. They are not configured or proven; use the current local deterministic or manual path. See [hosted readiness](../../docs/HOSTED_READINESS.md) and [policy decisions](../../docs/POLICY_DECISIONS.md).

[Participant setup](../../docs/PARTICIPANT_GUIDE.md) · [Contribution steps](../../CONTRIBUTING.md) · [Copyable model prompt](../../docs/MODEL_PROMPT.md) · [Review checklist](../../docs/REVIEW_CHECKLIST.md)

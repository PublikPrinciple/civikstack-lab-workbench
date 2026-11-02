# What participants build

A **task environment** is a small, versioned package that gives a model the context, tools, behavioral rules and test setup for one job. A capability is what that environment can accomplish. The Builder Lab compares approaches to find the least model assistance needed for a stated task and acceptance criteria.

The host supplies a reviewed problem, public-safe examples and a common evaluator. Participants improve one part of the package, run the same cases, explain failures, and leave a reproducible result and next task. Some work may need rules only. Other work may benefit from a small shared model. A result supports a conclusion about the approaches and examples tested; it cannot establish a universal minimum intelligence.

[Start here](START_HERE.md) · [Copy a prompt to your assistant](MODEL_PROMPT.md) · [Architecture](ARCHITECTURE.md) · [Hosted readiness](HOSTED_READINESS.md)

## Concrete package v1

The first package is [task-environments/care-fit/package.json](../task-environments/care-fit/package.json), version `0.1.0`. Its machine-readable contract is [task-environment.schema.json](../schemas/task-environment.schema.json). The stdlib loader in [labbench/package.py](../labbench/package.py) validates the supported local format, resolves local files within the checkout and hashes the manifest and its references for each report. No third-party schema library is needed to run it.

| Package part | Participant's work | Current implementation |
| --- | --- | --- |
| Purpose and version | Define one bounded job and version changes. | Manifest ID, version and purpose. |
| Task context | Supply public-safe inputs, source excerpts and known unknowns. | Four practice and eight evaluation cases, all newly synthetic; normalized facts supplied. |
| System prompt | Tell a model how to operate within this task. | Versioned prompt included; no model is called by the baseline. |
| Behaviors | Specify how to handle missing/conflicting facts and stop conditions. | Structured behavior file plus Python comparison rules; changing prose alone does not alter the runner. |
| Tools | Give the task a small input/output interface. | `case.read` and `response.emit` describe current function interfaces; they are not remote tool endpoints. Host-only evaluation reads reference answers. |
| RoutePack | Identify inputs, outputs, ordered steps, evidence and permission references. | Local route description of validate → compare → respond → evaluate. No RPOS adapter implemented. |
| Permissions | Declare the task's requested access; obtain host enforcement. | Declarative no-network/no-desktop requirements. The local worker is **not a sandbox**. |
| Harness | Execute the route and capture failures and resources. | Python worker per case, contract checks, timeout and reports. Only reviewed local code should be run here. |
| Model binding | Connect an approved shared model through authorized interfaces. | Explicitly unconfigured. Parameter ceiling remains unresolved. |
| Evaluation | Compare results against separately authored references. | Separate correctness, evidence and unknown measures; technical checks pass only for sample cases. Domain review pending. |

The schema intentionally describes what the local v1 runner supports. It accepts no configurable arbitrary shell command, deployment action, inference URL or credential. It fixes the current baseline/evaluator entrypoints, route implementations, tool IDs and requested access; participant implementations use the explicit `--adapter` interface after local code review. A later hosted binding needs a reviewed schema/runner change and server-side controls. The reference paths are local to the repository; remote URL fetching is not a package feature. Descriptive prose in prompts, behaviors and tool explanations still requires human review; loading and hashing it does not prove its meaning matches the code.

## Run the sample package

From the repository root, with an existing Python 3.12+ runtime:

```sh
python -m labbench run --split practice
python -m labbench run --package task-environments/care-fit/package.json --split evaluation --output results/local/evaluation.json
```

The first command already selects the care-fit package. It runs rules without a model, reads its declared input/reference files and writes a report. The package's prompt, behavior/tool/permission documents and RoutePack are loaded, checked where supported and hashed for provenance. The Python code executes the route; this is not a general workflow engine that interprets arbitrary RoutePack steps. The prompt is not executed in a model. The manifest cannot enforce the permissions it declares.

Care-fit asks whether supplied service and schedule facts could fit a fictional recurring afterschool-care need. A tutoring session, drop-in activity and one-off event are distinct from daily care. Labels are `potential_fit`, `mismatch`, and `unknown`, with source citations. Seats, admission, eligibility and outcomes remain unknown. The [adapter contract](ADAPTER_CONTRACT.md) states the exact comparison rules and limitations.

## A participant's first change

1. Inspect the manifest and one practice case. Explain the route and trust boundaries to your teammate or assistant.
2. Select one component to improve: a clearer prompt, a missing edge case, a comparison rule, a tool contract, a behavior rule or a test.
3. Record the hypothesis and acceptance criterion before editing. Copy the adapter example if changing execution; keep the shared reference answers independent.
4. Run the unchanged baseline and your approach against practice, then the public evaluation set. Record exposure to the evaluation answers.
5. Review a failure with a human. Save the package/component changes, report, [result](RESULT_TEMPLATE.md), and [progress checkpoint](PROGRESS_TEMPLATE.md). Name one next bounded task.

Prompt-only or boundary-design work is a legitimate contribution. Mark its behavioral effect **untested** until an authorized runtime consumes and evaluates it. A baseline pass cannot validate a prompt change or hosted isolation. People without a runtime can annotate source evidence, challenge reference labels and review permissions using the same package.

## Minimum necessary model assistance

Begin with the rules/no-model result. For an authorized model experiment, keep task, cases, evaluator version and acceptance criteria fixed. Record model/runtime/version, parameters, settings, seed, latency, errors, measured CPU/GPU/memory, costs where applicable and required unknown preservation. Compare each dimension independently, including human rationale review. Repeat nondeterministic runs and report variability.

The existing model-size rule and earlier planning differ; the owner must resolve the [policy](POLICY_DECISIONS.md). No model experiment is selected or run by this package. Hosted model access is intended to be shared, so participants do not need a separate model download. [Readiness checks](HOSTED_READINESS.md) must be completed before promising that experience.

## Versioning and contribution

Keep manifests and all related contracts in the same PR. Use a patch version for corrections that preserve interfaces, a minor version for compatible additions, and a major version when input/output or permission requirements break compatibility. Reports retain exact file hashes even before a commit. Changing labels needs a separate evidence/reviewer rationale, not only a better score. Record implementation dependencies and source commit in your result.

The shared care-fit package is the event's starting reference. Put independent approaches under `solutions/care-fit/<approach>/`. A proposed new task can live in `task-environments/<task-id>/`, but its manifest must identify a supported harness and real evaluator; v1 runs only the care-fit contract. A new task's scaffold is not a runnable implementation until those pieces and tests exist. Follow [contribution instructions](../CONTRIBUTING.md); maintainers decide what to merge after research and engineering review.

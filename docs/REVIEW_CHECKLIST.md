# Maintainer review checklist

Use this for a task-environment package change, evidence correction, or test contribution. Care-fit is the first example environment. Record a reviewer, date, source revision, decision, and unresolved questions. Passing automated checks supports review; it does not establish real-world service reliability.

## Research and evidence review

- [ ] The question is bounded and tied to a named task environment and version. The changed component and intended behavior are explicit.
- [ ] All submitted cases are explicitly synthetic or have documented permission and public-safe provenance. No private family records, identifying intake material, prompts containing personal records, or private source exports are included.
- [ ] Source citations resolve to the supplied statement and support the claimed fact. Citation existence alone is insufficient.
- [ ] Potential fit means only supported schedule/service compatibility. Seats, admission, eligibility, accommodations, handoff arrangements, and outcomes are not inferred.
- [ ] Missing or conflicting facts stay unknown. A contrary fact and a missing fact are distinguished.
- [ ] Expected-answer changes include rationale and correction history. Disagreements are retained and assigned for domain review.
- [ ] Any assertion of an Access Brief finding identifies the version actually checked. The Oct 9 sample/reference is distinguished from RC2; no exact RC2 mapping is claimed without review.
- [ ] A designated Access domain reviewer has recorded their status. If none has reviewed it, the result remains provisional.

## Package, execution, and evaluation review

- [ ] The package manifest consistently references harness, tools, behaviors, system prompt, context, permissions, and evaluation. Missing implementation is distinguished from a documented design.
- [ ] Prompt-only changes are marked manually reviewed or untested until an approved model adapter consumes the prompt. Baseline passes are not presented as prompt-behavior validation.
- [ ] Environment changes are compared with the deterministic baseline; any claim about minimum sufficient intelligence identifies the model/configuration, tested behavior, resource observations, and remaining uncertainty.
- [ ] RoutePack input/output, steps, evidence, and permission references remain consistent. A route reference is not an implemented RPOS adapter or an execution grant.
- [ ] Untrusted participant code is not executed by the trusted local harness. Any hosted execution uses separately verified isolation and access controls; prompt-level permissions and Terraform configuration alone are insufficient.
- [ ] Coder/MurMur integration claims match the actual hosted-readiness record. No endpoint, model service, or isolation property is assumed from a design document.

- [ ] A reviewer can reproduce the documented command or manual review from the recorded source revision.
- [ ] Adapter input/output follows the versioned contract; shared contract changes update affected examples, tests, and documentation together.
- [ ] The adapter does not read expected-answer files or map case IDs directly to expected labels. Inputs, outputs, and errors are inspectable.
- [ ] Practice/evaluation exposure, prompt tuning, and changed evaluation cases are disclosed. The public evaluation split is not called hidden.
- [ ] Correctness, citation/evidence results, and unknown preservation are reported separately with denominators, failures, and evaluator limits. No composite score is presented as production readiness.
- [ ] Error count/type, runtime, and measured resource use are reported. Unavailable CPU/GPU/memory or cost measures are labeled unmeasured; model claims identify the measurement source.
- [ ] Repository checks and challenge evaluation passed, or every blocked/failed check is stated with its consequence.
- [ ] New dependencies, third-party code/data permissions, and upstream notices have been reviewed. No credentials, weights, or unrelated generated files were committed.
- [ ] Any proposed model is recorded by identity, version, parameter count, license, and runtime. The unresolved `<=1B`/`7B` policy has not been silently changed.

## Merge and continuation decision

- [ ] Experiment result and progress handoff describe the latest state and next bounded action.
- [ ] Author agreement is recorded before publishing facilitator-collected notes or names.
- [ ] The owner-selected repository license remains unresolved unless an explicit owner decision is recorded; merging a contribution does not invent a license.
- [ ] The decision says accepted experiment, revision requested, or deferred, with reasons and follow-up owner only if agreed.
- [ ] Any real-world deployment, integration, or service guidance is handled through separate review. A successful demo or merge does not authorize it.

Review record:

```text
Contribution / source revision:
Technical reviewer / date / result:
Access domain reviewer / date / result:
Provenance and permissions review:
Checks run and output location:
Known limitations and disagreements:
Decision and rationale:
Next bounded task / agreed owner:
```

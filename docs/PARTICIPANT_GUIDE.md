# Participant guide

Read the [task-environment contract](TASK_ENVIRONMENT.md), [care-fit package](../task-environments/care-fit/package.json), and [starting challenge](../challenges/care-fit/README.md). Choose a build/evidence/test role and one environment component you can improve or review in an hour: harness, tools, behaviors, system prompt, context, permissions, or evaluation. Inspect the repository and available tools first. The package is what you build; its capability is what it can do. Record evidence that helps identify the minimum sufficient intelligence for the task.

## Laptop setup

The reference runtime is Python 3.12. The baseline and evaluator use only the standard library. You need a local repository copy and an existing Python installation; Git is needed for the fork/PR path. Check what is available:

```console
python --version
git --version
```

On macOS/Linux, the interpreter may be `python3`; on Windows it may be `py -3`. Substitute that command consistently. If no Python interpreter is available, pair with someone or use the noncoding path below. Software installation is optional and should be your deliberate choice, not a prerequisite for joining the event.

For a future contribution, follow the [fork and branch steps](../CONTRIBUTING.md). For read-only rehearsal, use GitHub's **Code → Download ZIP**, extract it, and open a terminal in the extracted repository folder. A downloaded ZIP can run checks but does not have Git history; record that limitation and the download date in your result.

## Run, inspect, change, compare

1. Run the baseline on practice cases from the repository root:

   ```console
   python -m labbench run --split practice
   ```

2. Read the [practice inputs](../data/care-fit/practice.json) and their expected answers described in the [contract](ADAPTER_CONTRACT.md). Explain at least one potential fit, mismatch, and unknown using source citations. All cases are fictional.
3. Choose one bounded environment change: improve a tool or prompt for service-type recognition, restrict context to cited evidence, preserve an unknown through a behavior rule, test a conflicting source, or implement an adapter. Record which package component changed. Copy the [model prompt](MODEL_PROMPT.md) if using an assistant. Keep your approach under `solutions/care-fit/<approach>/` and follow [the adapter contract](ADAPTER_CONTRACT.md).
4. Use the separate evaluation split after development:

   ```console
   python -m labbench run --split evaluation --output results/local/evaluation.json
   ```

   For your own Python adapter, exposing `solve(case)`:

   ```console
   python -m labbench run --split evaluation --adapter solutions/care-fit/your-approach/adapter.py --output results/local/your-approach.json
   ```

5. Run the repository checks:

   ```console
   python -m unittest discover -s tests -v
   python scripts/check_fixtures.py
   ```

6. Fill in the [result template](RESULT_TEMPLATE.md), including failures and measurements you could not obtain. Save a [progress handoff](PROGRESS_TEMPLATE.md), then follow the [contribution guide](../CONTRIBUTING.md).

The deterministic baseline does not consume `system-prompt.md`. A prompt-only change can be reviewed manually, but a baseline pass does not validate its behavior. Record it as an unevaluated model prompt until an approved model adapter actually consumes it. Apply the same distinction to documented tools or permissions that have no runtime enforcement.

Practice and evaluation examples are public. The evaluation split is separated to encourage honest iteration, not a secret benchmark. Record if you inspected its expected answers, tuned to it, or changed the examples. Passing these finite synthetic cases does not establish performance on real program information.

## Bring your own tool

Inspect the task-environment package before connecting a tool. Wrap an approved model, parser, or rules behind the same input/output contract. Hosts supply the starting harness; your contribution changes a documented component of the package. Compare results and resource use with the deterministic baseline before adding model complexity. The adapter must return source-backed labels and preserve required unknowns. Do not read expected-answer files from the adapter or hard-code case IDs to answers.

Record model/version, parameter count, license, runtime, dependencies, hardware, and limits if applicable. Report actual error and resource observations; mark unavailable metrics as unmeasured. The earlier `<=1B` rule and a later proposed `7B` limit are unresolved, so no new model choice is approved by these instructions. Start with the deterministic baseline while maintainers settle the policy. Hosted models, paid runtimes, and credentials are not supplied.

An external adapter is executable code on your machine. The current local harness is for reviewed, trusted code. Untrusted participant packages require isolated execution; review alone does not establish that isolation. Documented or prompt-level permissions are not enforced security boundaries. Do not put credentials or personal records in results.

## Proposed browser workspace and shared model

The planned hosted path uses an isolated Coder browser workspace and authenticated access through MurMur to a selected model on the host desktop. Attendees would not need to download weights. That service is unconfigured and unproven; use only an endpoint that hosts have explicitly approved after the [readiness checks](HOSTED_READINESS.md). Terraform provisions infrastructure and does not by itself define model behavior, permissions, or safe isolation. Beakon is proposed to show the host's running environments, resources, connections, and failures; no such integration is implemented here. No hosted execution or network change is authorized by this guide.

A RoutePack describes input/output, steps, evidence, and permission references. It is a route description, not a working RPOS integration or execution grant. See [TASK_ENVIRONMENT.md](TASK_ENVIRONMENT.md).

## Phone, paper, or setup blocked

Open [Start here](START_HERE.md) and a practice case. Write the case ID, proposed label, exact source IDs, uncertainty, and a reason an alternative answer would fail. Use the result template as plain text or on paper. A facilitator can put your review in a local queue and discuss publication with you. No coding or GitHub account is required.

If the network is unavailable, facilitators can share the prepared repository archive or printed practice cases. A team with one working laptop can run an experiment for its reviewers. Everyone can demonstrate a reasoning failure even when their software cannot run.

## Continue after the event

Before stopping, record the current revision, changed files, last successful command, unresolved failures, and the next small action in the progress handoff. On return, inspect that record and the current repository state, reproduce the last result, and then select the next task. Keep discussion attached to the relevant issue/PR or experiment folder so another contributor can follow it.

[Host agenda](meetup.md) · [Review criteria](REVIEW_CHECKLIST.md) · [Validation limits](VALIDATION.md)

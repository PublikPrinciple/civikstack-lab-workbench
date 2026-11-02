# Start here: Builder Lab Workbench

**Builder Lab · November 10, 2026 · 6–8 pm Eastern · Durham Food Hall**

Your job: improve or test **one part of a reproducible task environment for a small language model**. The package brings together the runner, tools, behavior rules, system prompt, supplied information, permissions, and tests. We seek the minimum sufficient intelligence for a reliable result. A capability is what that environment can do.

Start with the [care-fit package](../task-environments/care-fit/package.json), which distinguishes daily afterschool care from tutoring, drop-in activities, and events using synthetic evidence. Care-fit is the first example, not the whole Lab. Read the [task-environment contract](TASK_ENVIRONMENT.md).

## Choose a role

- **Build:** improve one tool, prompt, context rule, behavior, or boundary in the environment. Use the [adapter contract](ADAPTER_CONTRACT.md) for executable changes.
- **Review evidence:** decide what a source supports, which answer follows, and what stays unknown.
- **Test:** create a counterexample or show where a plausible answer makes an unsupported claim.

All three roles work on the [same starting challenge →](../challenges/care-fit/README.md). Teams can combine roles. Hosts supply the sample package, examples, baseline, evaluator, and review process.

## On your phone

Read the [challenge](../challenges/care-fit/README.md), compare the [practice cases](../data/care-fit/practice.json), and record an observation using the [result template](RESULT_TEMPLATE.md). Show or give your notes to the facilitator. A GitHub account is optional for this path.

The event QR points to the [existing public repository](https://github.com/PublikPrinciple/civikstack-lab-workbench). It opens reading and contribution instructions; it does not provision a coding environment.

## On your laptop

Open the [participant guide](PARTICIPANT_GUIDE.md). With Python available, the first command from the repository root is:

```console
python -m labbench run --split practice
```

No model download or paid service is needed. If setup fails, join an evidence/test review group or pair with a working laptop.

## With your own AI assistant

Copy the [model prompt](MODEL_PROMPT.md), then let it inspect the repository and available tools. Choose one bounded task and review its output. Save the [progress handoff](PROGRESS_TEMPLATE.md) so your next session can resume.

## Finish with something useful

Record the package/component changed, question, source revision, commands or review method, actual results, failures, and next task. Use the [contribution guide](../CONTRIBUTING.md) to submit a PR or a noncoding review. Continue after the event by picking up a recorded next task.

**Potential fit is a research label.** It does not confirm seats, admission, eligibility, or outcomes. All runnable records here are synthetic; human review is required before any real-world use.

The proposed hosted path is an isolated Coder browser workspace with shared desktop model access through MurMur, so attendees would not need to download weights. It is not configured or proven. Beakon is proposed to show the host's environment and resource health; that integration is also unimplemented. Use the local rules baseline or manual review today; see [hosted readiness](HOSTED_READINESS.md) and [policy decisions](POLICY_DECISIONS.md).

[Event agenda](meetup.md) · [Current status](STATUS.md) · [Validation](VALIDATION.md)

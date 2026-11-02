# Builder Lab Workbench status — November 2, 2026

Canonical public repository: https://github.com/PublikPrinciple/civikstack-lab-workbench. The display name is Builder Lab Workbench; the repository slug and QR destination stay unchanged.

## Prepared locally

- Versioned task-environment manifest/schema and care-fit sample with RoutePack, prompt, behavior, tools, requested permissions, context and evaluator references.
- Runnable Python baseline, adapter example, package validation, separate evaluation measures, error/resource reports and 12 newly authored synthetic cases.
- Mobile Start Here, copyable assistant prompt, resumable progress/result templates, outside-contributor workflow, research/engineering review and November 10 event agenda.
- Architecture recommendation and proposed hosted readiness/support protocol, including Beakon's possible resource/health role.

These changes are prepared on a local review branch. The entire package has not been pushed or merged. Display-name/README wording has user approval, but the README links to new files, so coherent publication of the implementation and supporting material still needs approval. No remote issue, repository setting, slug or service has been changed during this preparation.

## Verified scope

On November 2, the existing public `main` remained at `3e85921ae882fd3212d41de13e9744c7e11a3072`. [Starter CI run 41101914173](https://github.com/PublikPrinciple/civikstack-lab-workbench/actions/runs/41101914173) completed successfully on October 30. Its scope was six starter contract tests plus the original fixture validator, not hosted readiness or task performance.

The local implementation has 61 passing tests, including the original six, using an existing Python 3.12.11 runtime. See [validation evidence and limits](VALIDATION.md) for commands and fresh-copy results. No model capability or model minimum has been measured. The local rules result applies only to the supplied normalized synthetic cases.

## Still open

- Domain review of the synthetic references; reviewer to be assigned. The October 9 reference motivates the task; exact final RC2 mapping is unverified.
- Owner decision on the existing `<=1B` production rule versus earlier `7B` planning; no ceiling selected or relaxed here.
- Owner-selected repository license; existing Coder attribution remains intact.
- Coder hosting, authentication, safe participant isolation, shared model access through MurMur, real concurrency/resource testing, and Beakon integration. None is configured or validated here.
- Docker provider 4.6.0 checksum verification failure recorded during earlier Terraform preparation. No bypass or deployment occurred.

The original six open challenge issues and starter fixtures remain available as historical exploration paths. Care-fit is the first runnable task environment, not a claim that those six proposed tasks are implemented. [Hosted readiness](HOSTED_READINESS.md) specifies evidence needed before inviting participants into a live service.

# Validation record

## November 2, 2026 — local Builder Lab task environment

Reference runtime used: existing full **CPython 3.12.11 on Windows**, managed by uv. No runtime, package or model was installed. The default `python` Windows alias was unusable. An existing ComfyUI bootstrap Python 3.13.12 could run the baseline but lacked `unittest`, so it was not used for the complete verification.

Passed locally: **61 tests** (6 original contract, 28 care-fit behavior/adapter/scoring, 27 task-package/metadata tests). These cover wrong citations, preserved unknowns, conflicts, schema failures, malformed/crashing/timed-out adapters, error denominators, package path containment, reference hashes, and rejection of unsupported route/tool/permission metadata. The original fixture checker still validates its two synthetic program records.

The task runner includes measured worker CPU and wall timing; memory/GPU are explicitly unmeasured. The prompt is included and hashed but the deterministic baseline does not invoke a model, so these checks do not validate prompt behavior in a model. The public evaluation split is openly available, not hidden.

The existing public [GitHub Actions run 41101914173](https://github.com/PublikPrinciple/civikstack-lab-workbench/actions/runs/41101914173) was rechecked on November 2: **success**, `main` SHA `3e85921ae882fd3212d41de13e9744c7e11a3072`, completed October 30. It ran only the six original tests and fixture validator. The new branch's expanded workflow has not run on GitHub because it has not been pushed.

Not established: domain approval of references, real-world program accuracy, minimum model intelligence, hosted inference, MurMur/Coder/Beakon/RPOS integration, workspace/tenant isolation, public network controls, GPU measurements, concurrent participant capacity, GitHub contribution round trip or a selected license. Docker/Terraform executables are discoverable in the current environment; no image build, provider reinitialization, plan/apply or deployment was attempted. The earlier provider checksum blocker remains unresolved.

## October 30, 2026 — original preparation record

Passed:
- Six Python unit tests, including rejection of duplicate IDs, unresolved evidence, invalid availability, and invalid age ranges.
- Fixture validator and issue-seeding preview for six cards.
- Python bytecode compilation and Terraform formatting check (Terraform 1.13.5).

Blocked:
- Terraform schema validation: Docker provider 4.6.0 failed its cached-package checksum check after initialization, including a second verified initialization attempt. No checksum check was bypassed. Resolve the package verification failure on the deployment host before using this template. Provider lockfile is included for reproducibility, not as evidence of a successful validation.

Not run:
- Docker image build (Docker unavailable in the preparation environment).
- Terraform plan/apply, live Coder startup, stop/start persistence, participant isolation, concurrency tests, GitHub CI, GitHub issue creation, and contribution round trip.

No model capability had been implemented or evaluated in the October 30 preparation. Those tests established starter data integrity only. The later local task-environment work is recorded separately above.

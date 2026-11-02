# Builder Lab Workbench: keep each layer focused

**Keep HCL for workspace provisioning, Dockerfile for packaging, and Python for the participant harness and evaluator. Do not rewrite the Python workbench in Rust at this stage.** This recommendation follows the code present in this repository and the event's reproducibility needs; it is not a benchmark claim that Python is always faster or better.

## What the source actually does

| Source | Present responsibility | Recommendation |
| --- | --- | --- |
| [templates/docker/main.tf](../templates/docker/main.tf) | Coder agent/browser editor, Docker workspace, per-workspace home volume and configured memory/CPU shares. | Keep HCL as the infrastructure specification. It does not define model reasoning or authorize a task. Resolve provider validation and isolation gaps before hosting. |
| [templates/docker/Dockerfile](../templates/docker/Dockerfile) | Python 3.12 image plus Git and workspace utilities; non-root `coder` user. | Keep the image recipe. Pin/review image and runtime dependencies before sustained hosting; no image build was performed here. |
| [labbench](../labbench/) | Load/validate a task package, execute a reviewed Python adapter, compare results and write reports. | Keep Python as the accessible participant interface. The sample needs only the standard library and has a reproducible local test route. |
| [task-environments/care-fit](../task-environments/care-fit/) | Task definition, prompt, behavior, route, tool and permission contracts plus references to data/evaluator. | Keep language-neutral JSON/Markdown contracts so alternate implementations can share the task. |
| Beakon / MurMur / Fabric / RPOS | No implementation or adapter in this repository. | Integrate only after their actual source and contracts are inspected. Do not infer runtime behavior from names. |

Coder documents Terraform templates as definitions of workspace infrastructure, and Docker documents Dockerfiles as image build instructions. These match the roles already present here. Python's standard `unittest` supports the current automated checks. [Coder templates](https://coder.com/docs/admin/templates) · [Dockerfile overview](https://docs.docker.com/build/concepts/dockerfile/) · [Python unittest](https://docs.python.org/3/library/unittest.html)

The Terraform template sets `memory = 4096`, `cpu_shares = 512`, UID/GID `1000:1000`, and `no-new-privileges`. It also exposes a host-gateway mapping and lacks demonstrated destination allowlisting. CPU shares are not a hard quota. These settings do not establish safe isolation for untrusted participants. The Docker provider checksum failure, live startup, isolation and concurrency checks remain unresolved. See [hosted readiness](HOSTED_READINESS.md).

## Where Rust may belong

Rust is a reasonable candidate for a long-running Beakon host agent or a measured performance-sensitive runtime component because it supports efficient resource use and memory/thread safety. That is a future component choice, not a reason to translate the event's Python adapters now. [Rust's design goals](https://rust-lang.org/)

A migration should have a concrete trigger: measured harness overhead affecting the acceptance budget, host integration that benefits from a native executable, or a reviewed production boundary with requirements Python does not meet. First profile the actual workload, keep the JSON task/response contracts, and compare implementations on the same tests. Most importantly, rewriting a worker in Rust does not sandbox participant code or create authorization. Those controls need an enforced runtime and service design.

## Management and authority

Beakon is the proposed place to manage resources, environment health and model availability. Resource availability tells us whether a workload can fit. It does not grant a participant permission to use a service, choose Fabric placement, or provide RPOS authority. None of those integrations is implemented here.

The proposed hosted path is an authenticated Coder workspace running an isolated task environment, connecting through a server-enforced tool/inference gateway to an approved shared desktop model, with MurMur's precise interface to be verified. The evaluator records results separately. Terraform provisions infrastructure; the task package supplies behavioral context; the gateway/runtime enforces permissions. No participant should receive unrestricted desktop/LAN access or a public raw model endpoint.

This branch prepares the local sample and reviewable contracts. It performs no installation, infrastructure provisioning, login creation, credential issuance, networking change or deployment.

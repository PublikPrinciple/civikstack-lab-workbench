# CivikStack Lab Workbench

Bring your laptops, your models, and something you want to figure out.

Access Lab supplies verified findings; Intelligence Lab develops and evaluates capabilities; Utility Lab evaluates the compute needed to run them. This repository connects their work through small challenges and a common data contract.

Repository: https://github.com/PublikPrinciple/civikstack-lab-workbench

## Start here
1. Read `challenges/README.md` and select a challenge.
2. Open its GitHub issue, or create one using the capability challenge form. Comment with what you will explore; a maintainer assigns it. Multiple approaches are welcome.
3. Clone this repository locally, open it in a Dev Container, or launch the maintainer-provided Coder template.
4. Run `python3 -m unittest discover -s tests -v` and `python3 scripts/check_fixtures.py`.
5. Create a branch such as `challenge/03-unknowns-yourname`, implement your approach, and open a pull request linked to the issue.

Python 3.12 is the reference runtime. The initial checks use only the standard library. No model download, paid API, or private data is needed.

## Important status
This is a starter kit, not a deployed Coder service. All supplied service records and challenges are illustrative, synthetic material, not verified Durham Access Lab findings or real referral information. Replace or supplement them with reviewed Access Lab evidence before making real-world service claims. No RoutePack/RPOS or Beakon integration is implemented here.

## Working rules
- Learn the system, not the person. Do not commit private family records, secrets, model weights, or identifying intake records.
- Production capability work uses models of 1 billion parameters or smaller. Begin with deterministic methods when appropriate. Record model identity, parameter count, license, runtime, and evaluation results; do not assume a familiar model name meets this limit.
- Unknown availability and accommodations must remain unknown. Cite evidence for factual statements.
- Keep experiments under `solutions/<challenge-id>/<approach>/` so independent approaches can coexist.
- Evidence and evaluation contributions are equally welcome alongside software.

See `CONTRIBUTING.md`, `docs/contracts.md`, `docs/operator-setup.md`, and `docs/meetup.md`.

A repository license has not been selected. Do not represent this kit as licensed open source until the owner chooses and adds a license.

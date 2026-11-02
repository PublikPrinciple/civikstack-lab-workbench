# Contributing a task-environment experiment

Your contribution improves one part of a reproducible task environment: harness, tools, behaviors, system prompt, context, permissions, or evaluation. A capability is what the resulting package can do. We compare environment changes while seeking the minimum sufficient intelligence for the task. Start with the [care-fit sample package](task-environments/care-fit/package.json) and [task-environment contract](docs/TASK_ENVIRONMENT.md). Multiple approaches can coexist. The deliverable is package changes or review evidence, reproducible results, limitations, and a handoff.

Start with the [participant guide](docs/PARTICIPANT_GUIDE.md). Save an [experiment result](docs/RESULT_TEMPLATE.md) and a [progress handoff](docs/PROGRESS_TEMPLATE.md). An assistant can use the [model prompt](docs/MODEL_PROMPT.md), but you remain responsible for reviewing the contribution.

## Code or file contribution from outside the repository

1. Read the challenge and inspect the [existing issues](https://github.com/PublikPrinciple/civikstack-lab-workbench/issues). If a suitable issue exists, comment with a short intended approach. An assignment is not a prerequisite to exploring; avoid claiming assignment until a maintainer does so. If none fits, link the challenge in the PR.
2. Sign in to GitHub and fork `PublikPrinciple/civikstack-lab-workbench` to your account. Clone **your fork**, then create a branch. Replace `YOUR-ACCOUNT` and `yourname` below.

   ```console
   git clone https://github.com/YOUR-ACCOUNT/civikstack-lab-workbench.git
   cd civikstack-lab-workbench
   git remote add upstream https://github.com/PublikPrinciple/civikstack-lab-workbench.git
   git switch -c challenge/care-fit-yourname
   ```

3. Keep an independent approach under `solutions/care-fit/<approach>/`. Include the package/component change, adapter code if applicable, reproduction instructions, a result record, and a handoff. Record the parent package version and keep prompt, tool, context, behavior, permission, and evaluation references consistent. Propose shared package/contract/fixture changes separately and explain their effect on existing results. Keep evaluation labels out of runtime adapters.
4. Run the shared checks and your evaluation:

   ```console
   python -m unittest discover -s tests -v
   python scripts/check_fixtures.py
   python -m labbench run --split evaluation --adapter solutions/care-fit/your-approach/adapter.py --output results/local/your-approach.json
   ```

   Omit `--adapter ...` to evaluate the baseline. If you cannot run a check, record the command, reason, and exact unverified claim. Do not present an unrun check as passing.
5. Review changed files for personal data, secrets, unrelated changes, and model weights. Commit only your intended files, push the branch to **your fork**, and open a PR with base `PublikPrinciple/civikstack-lab-workbench:main` and compare your fork's branch. Include a relevant issue link when available; do not close an issue unless the contribution actually completes it.

   ```console
   git status --short
   git add solutions/care-fit/your-approach
   git commit -m "Add care-fit experiment and evaluation"
   git push -u origin challenge/care-fit-yourname
   ```

Review your fork's destination before pushing. A public fork or PR makes its contents public. A fork does not grant write access to the upstream repository.

## Evidence or test review without coding

Choose a case, read its supplied source statements, and record the expected label, supporting citations, missing facts, and any disagreement. Use the [result template](docs/RESULT_TEMPLATE.md) in plain text or on paper. GitHub users can attach the text to a relevant issue or propose a documentation PR. At the event, give it to the facilitator for a local review queue; no Git account or installation is needed. The facilitator should obtain your agreement before publishing your contribution or name.

Do not submit real family details or copy private Access Lab materials. New fictional examples must be labeled synthetic. A disputed answer is useful evidence: preserve the disagreement and proposed reasoning instead of silently replacing the reference answer.

## Review and continuation

Maintainers use the [review checklist](docs/REVIEW_CHECKLIST.md). Evidence/privacy review, reproducibility, contract compatibility, and license/dependency decisions are separate from a green CI check. No demo or merged PR is automatically deployed or published as service guidance.

For an ongoing experiment, keep its issue or PR updated with the current question, latest reproducible result, known failure, and next bounded task. Refresh the progress handoff whenever you stop. A new contributor should be able to inspect the source revision, rerun the result, and continue without reconstructing a chat history.

The earlier six challenge issues remain useful context, not a claim that six capabilities are implemented. Suggested states are available, exploring, ready for review, and reviewed experiment; do not equate merged with production-ready. A project board and automated assignment are not configured.

The repository license remains an owner decision. Preserve upstream attribution, identify third-party code and data permissions, and obtain review before adding dependencies. The `<=1B` versus proposed `7B` model limit is unresolved; use the deterministic baseline while that policy is settled, or record a model proposal without calling it approved.

The proposed isolated Coder workspace plus MurMur desktop-model access is a design, not an available service. See [hosted readiness](docs/HOSTED_READINESS.md). Do not execute unreviewed participant packages in the local harness or treat prompt-level permissions as an execution boundary. Hosted execution requires verified isolation and access controls. RoutePack references describe the intended route; no RPOS execution adapter is implied.

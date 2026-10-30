# Operator setup and deployment gates

## Current state
Public repository: https://github.com/PublikPrinciple/civikstack-lab-workbench . Coder deployment, invitations, and model service remain unconfigured. Host is unresolved. No hosting purchase or access grants are included.

## 1. Repository
Select the canonical GitHub owner/repository and its visibility. If new, create it with GitHub UI or `gh repo create OWNER/REPO --private` (choose public only deliberately). Select a license before advertising open-source reuse. Push these files, review Actions results, then create the six issues using `python3 scripts/seed_issues.py --repo OWNER/REPO`. The script uses your authenticated GitHub CLI. It previews by default; add `--apply` to create missing issues. It does not create a Project board, grant access, or change visibility.

## 2. Coder host
Use an operator-controlled Linux host with Docker and a supported Coder installation, persistent Coder database, HTTPS access URL, and backups. Follow current official deployment guidance: https://coder.com/docs/install . Do not deploy this temporary chat workspace as the meetup service.

Choose the host based on expected concurrency; this template allows up to 4 GiB per workspace and does not provision GPUs. Load-test the actual expected attendance. Container memory limits are ceilings, not host capacity guarantees; CPU shares are relative weights, not a CPU quota.

The Coder provisioner needs Docker access. Participants must never receive the Docker socket or control-plane secrets. This single-host container template is for a trusted pilot; untrusted multi-tenant use needs stronger isolation and a reviewed provisioning design. The upstream base pattern runs the agent from a container entrypoint; confirm the effective user and filesystem permissions on your host.

## 3. Build and import template
On the workspace Docker host, in `templates/docker`, run `docker build -t civikstack-lab-workbench:pilot .`. For remote provisioners publish the image to an accessible registry and set `workspace_image` accordingly. Review and pin provider, module, and image versions/digests before sustained use; commit the generated Terraform lockfile. This kit starts from Coder's upstream Docker example and includes the provider lockfile generated during preparation. Re-run initialization and validation on the intended host; see `docs/VALIDATION.md`.

From a machine with Coder CLI connected to the chosen server, run `coder templates push civikstack-lab --directory templates/docker`. Supply `repository_url` when prompted. Validate against the installed Coder version; inspect its CLI help if flags differ. The template installs browser VS Code through Coder's code-server module. Persistent home volumes survive stop/start; deleting a workspace can delete its volume, so commit and push work.

A public repository can clone immediately. For a private repository, configure supported per-user GitHub external authentication in Coder or have each user authenticate Git in their workspace; no shared GitHub token is embedded in this template. Initial clone will fail clearly until that is configured. Protect Terraform state because agent credentials can appear in it.

## 4. Pre-event verification
- Sign in using a participant account with intended permissions.
- Create a workspace, open its terminal and browser editor, and run the two README checks.
- Create a branch, push a change, and open a PR linked to a challenge.
- Stop/start and confirm files persist; verify one participant cannot access another's files or credentials.
- Test concurrent workspaces, memory limits, network access, cleanup, and backups.
- Record host details, configured versions, results, and failure recovery in this document.

## Attribution
Template adapted from https://github.com/coder/coder/blob/main/examples/templates/docker/main.tf . Preserve upstream license obligations when distributing it. Coder's code licensing and optional commercial features must be reviewed for the chosen version; this kit does not select an application license.

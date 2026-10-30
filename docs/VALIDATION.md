# Validation record — October 30, 2026

Passed:
- Six Python unit tests, including rejection of duplicate IDs, unresolved evidence, invalid availability, and invalid age ranges.
- Fixture validator and issue-seeding preview for six cards.
- Python bytecode compilation and Terraform formatting check (Terraform 1.13.5).

Blocked:
- Terraform schema validation: Docker provider 4.6.0 failed its cached-package checksum check after initialization, including a second verified initialization attempt. No checksum check was bypassed. Resolve the package verification failure on the deployment host before using this template. Provider lockfile is included for reproducibility, not as evidence of a successful validation.

Not run:
- Docker image build (Docker unavailable in the preparation environment).
- Terraform plan/apply, live Coder startup, stop/start persistence, participant isolation, concurrency tests, GitHub CI, GitHub issue creation, and contribution round trip.

No model capability has been implemented or evaluated. The tests establish starter data integrity only.

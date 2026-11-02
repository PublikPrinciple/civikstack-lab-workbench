# Decisions the owner still needs to make

The deterministic care-fit baseline can run while these decisions remain open.

| Decision | Current boundary | Required next step |
| --- | --- | --- |
| Model size | The existing repository's production rule is at most 1B parameters. Earlier planning mentioned 7B. That conflict is unresolved; this event preparation does not relax the existing rule or select a model. | Owner clarifies production versus event experimentation limits and records the approved policy before hosts advertise a model track. |
| Repository license | No application license has been selected. Existing Coder template attribution and licenses stay intact. Public visibility does not establish general reuse rights. | Owner selects a license and reviews contribution/dependency compatibility before advertising licensed open-source reuse. |
| Research review | Synthetic expected answers are draft, internally checked and pending domain review. RC2 mapping remains unverified. | Assign a domain reviewer; record decisions and corrections before event use. |
| Hosted workspace/model service | Coder and a hosted model service are unconfigured. Dev Container startup has not been demonstrated. | Use the tested local baseline or manual fallback. Hosting requires separate configuration, authorization and participant testing. |

Participants may bring approaches that fit the approved rules. No attendee needs a model to contribute. Until the model ceiling is resolved, use deterministic code or evidence/test review for the shared event path. Record model identity, parameter count, license, runtime and measured resources for any later approved model experiment.

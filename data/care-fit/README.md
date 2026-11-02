# Synthetic care-fit cases

These twelve cases are newly authored, fictional rehearsal material for the Builder Lab. They contain no family records, real program listings, copied private research text, or real referral information. The same fictional need is used throughout: recurring daily afterschool care, Monday through Friday, covering 15:00–18:00.

The source excerpts and normalized facts are curated synthetic inputs. The first runnable task classifies those supplied facts; it does not measure extraction from arbitrary websites. An extraction experiment can be proposed separately with its own reviewed reference fields and evaluation.

## Use the splits

- [Practice inputs](practice.json) and [practice reference answers](practice.expected.json): four examples for learning the contract and debugging.
- [Evaluation inputs](evaluation.json) and [evaluation reference answers](evaluation.expected.json): eight different examples for reporting results after practice.

Evaluation is openly separated from practice, not hidden or a blind benchmark. Adapters receive one input case, including its source excerpts and facts; the harness does not pass reference answers to the adapter. Participants should record whether they read or tuned against evaluation answers. A successful run on these public examples does not demonstrate generalization or real-world reliability.

## What each reference label means

Each case assesses service type, required days, time coverage, and weekly recurrence. A known mismatch in any field makes the overall label `mismatch`, even if another field is unknown. With no known mismatch, any missing or unresolved field makes it `unknown`. All four matching fields produce `potential_fit`.

`Potential_fit` describes the four documented conditions only. Seats, admission, eligibility, and outcomes remain unknown in every case. Missing values have no invented citations. Unresolved conflicts preserve a null fact and cite both conflicting excerpts; neither source is silently selected as authoritative.

| Case | Expected label | Reason to inspect |
| --- | --- | --- |
| practice-01 | potential_fit | Exact time coverage and five-day recurring care |
| practice-02 | mismatch | Part-week tutoring with shorter hours |
| practice-03 | unknown | Care hours omitted |
| practice-04 | mismatch | Drop-in enrichment; recurrence also unknown |
| evaluation-01 | mismatch | Starts too late |
| evaluation-02 | mismatch | Ends too early |
| evaluation-03 | mismatch | One-time Saturday event; hours also unknown |
| evaluation-04 | unknown | Unresolved contradiction about days |
| evaluation-05 | unknown | Unresolved contradiction about service type |
| evaluation-06 | potential_fit | A wider time interval fully covers the need |
| evaluation-07 | unknown | Matching schedule with unspecified service type |
| evaluation-08 | mismatch | Part-week care; hours also unknown |

## Review status and provenance

Authored November 2, 2026 for this repository. Reference labels and notes were authored independently of the production baseline and checked for consistency with their synthetic excerpts. Their status is `draft_pending_domain_review`; no named domain reviewer has approved them. A host-assigned human domain reviewer must review the labels, citations, and task wording before the event. Record that review in the contribution/review record rather than treating automated checks as domain approval.

The challenge's broader research motivation and its limits are documented in [the challenge guide](../../challenges/care-fit/README.md). These fixtures are not an Access Lab dataset export or an exact mapping of the final RC2 brief.

When proposing a correction, identify the case, disputed field, cited excerpt, proposed expected answer, and reasoning. Preserve the prior decision in the review history. Update inputs, reference answers, and relevant tests together; rerun the evaluator and explain changed results. Keep real people and unapproved source material out of public contributions.

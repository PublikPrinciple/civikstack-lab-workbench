"""Independent care-fit examples and failure-path checks; standard library only."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from labbench.baseline import solve
from labbench.contract import load_dataset, load_expected, loads, validate_case, validate_response
from labbench.evaluate import aggregate, score
from labbench.__main__ import run_case

ROOT = Path(__file__).resolve().parents[1]


def example_case():
    """Authored independently of the baseline and published fixture files."""
    return {
        "case_id": "test-family-need", "synthetic": True,
        "need": {"service_type": "daily_afterschool_care",
                 "days": ["mon", "tue", "wed", "thu", "fri"],
                 "hours": {"start": "15:00", "end": "18:00"}, "recurring": True},
        "sources": [
            {"id": "kind", "text": "Synthetic program provides daily afterschool care."},
            {"id": "days", "text": "Synthetic program operates Monday through Friday."},
            {"id": "hours", "text": "Synthetic care starts at 14:30 and ends at 18:30."},
            {"id": "recurrence", "text": "Synthetic schedule repeats each week."},
            {"id": "unrelated", "text": "Synthetic program uses a green logo."},
        ],
        "facts": {
            "service_type": {"value": "daily_afterschool_care", "source_ids": ["kind"]},
            "days": {"value": ["mon", "tue", "wed", "thu", "fri"], "source_ids": ["days"]},
            "hours": {"value": {"start": "14:30", "end": "18:30"}, "source_ids": ["hours"]},
            "recurring": {"value": True, "source_ids": ["recurrence"]},
        }, "conflicts": [],
    }


def expected_fit():
    return {
        "case_id": "test-family-need", "label": "potential_fit",
        "assessments": {
            "service_type": {"status": "match", "source_ids": ["kind"]},
            "days": {"status": "match", "source_ids": ["days"]},
            "hours": {"status": "match", "source_ids": ["hours"]},
            "recurring": {"status": "match", "source_ids": ["recurrence"]},
        },
        "unknowns": ["seats", "admission", "eligibility", "outcomes"],
        "review_note": "Four supplied schedule/service facts match; no admission or outcome evidence exists.",
    }


class BaselineBehaviorTests(unittest.TestCase):
    def test_potential_fit_preserves_protected_unknowns(self):
        case = example_case()
        before = copy.deepcopy(case)
        result = solve(case)
        self.assertEqual(result["label"], "potential_fit")
        self.assertEqual(result["assessments"], expected_fit()["assessments"])
        self.assertEqual(set(result["unknowns"]), {"seats", "admission", "eligibility", "outcomes"})
        self.assertEqual(result["claims"], {"seats": None, "admission": None, "eligibility": None, "outcomes": None})
        self.assertEqual(case, before, "an adapter must leave the supplied case intact")

    def test_tutoring_dropin_and_event_are_not_daily_care(self):
        for service in ("tutoring", "drop_in", "event"):
            with self.subTest(service=service):
                case = example_case()
                case["facts"]["service_type"]["value"] = service
                result = solve(case)
                self.assertEqual(result["label"], "mismatch")
                self.assertEqual(result["assessments"]["service_type"]["status"], "mismatch")

    def test_part_week_care_does_not_cover_daily_need(self):
        case = example_case()
        case["facts"]["days"]["value"] = ["tue", "thu"]
        result = solve(case)
        self.assertEqual(result["label"], "mismatch")
        self.assertEqual(result["assessments"]["days"]["status"], "mismatch")

    def test_reordered_days_and_additional_day_still_cover_need(self):
        case = example_case()
        case["facts"]["days"]["value"] = ["sat", "fri", "thu", "wed", "tue", "mon"]
        self.assertEqual(solve(case)["label"], "potential_fit")

    def test_both_ends_of_time_window_are_required(self):
        for hours in ({"start": "15:30", "end": "18:30"}, {"start": "14:30", "end": "17:30"}):
            with self.subTest(hours=hours):
                case = example_case()
                case["facts"]["hours"]["value"] = hours
                self.assertEqual(solve(case)["assessments"]["hours"]["status"], "mismatch")

    def test_equal_time_boundaries_count_as_coverage(self):
        case = example_case()
        case["facts"]["hours"]["value"] = {"start": "15:00", "end": "18:00"}
        self.assertEqual(solve(case)["label"], "potential_fit")

    def test_missing_hours_produces_unknown_not_mismatch(self):
        case = example_case()
        case["facts"]["hours"] = {"value": None, "source_ids": []}
        result = solve(case)
        self.assertEqual(result["label"], "unknown")
        self.assertEqual(result["assessments"]["hours"], {"status": "unknown", "source_ids": []})
        self.assertIn("hours", result["unknowns"])

    def test_explicit_mismatch_retains_other_unknowns(self):
        case = example_case()
        case["facts"]["service_type"]["value"] = "tutoring"
        case["facts"]["hours"] = {"value": None, "source_ids": []}
        result = solve(case)
        self.assertEqual(result["label"], "mismatch")
        self.assertEqual(result["assessments"]["hours"]["status"], "unknown")
        self.assertIn("hours", result["unknowns"])

    def test_one_time_event_schedule_is_not_recurring(self):
        case = example_case()
        case["facts"]["recurring"]["value"] = False
        result = solve(case)
        self.assertEqual(result["label"], "mismatch")
        self.assertEqual(result["assessments"]["recurring"]["status"], "mismatch")

    def test_conflict_retains_both_sources_and_unknown(self):
        case = example_case()
        case["sources"].append({"id": "hours-conflict", "text": "Another synthetic source gives closing time 17:00."})
        case["facts"]["hours"] = {"value": None, "source_ids": ["hours", "hours-conflict"]}
        case["conflicts"] = ["hours"]
        validate_case(case)
        result = solve(case)
        self.assertEqual(result["label"], "unknown")
        self.assertEqual(result["assessments"]["hours"], {"status": "unknown", "source_ids": ["hours", "hours-conflict"]})


class ContractAndScoringTests(unittest.TestCase):
    def test_valid_but_unrelated_citation_loses_evidence_credit(self):
        case = example_case()
        response = solve(case)
        response["assessments"]["hours"]["source_ids"] = ["unrelated"]
        result = score(response, expected_fit(), case)
        self.assertTrue(result["label_correct"])
        self.assertTrue(result["field_correct"]["hours"])
        self.assertFalse(result["evidence_support"]["hours"])

    def test_omitted_missing_fact_loses_unknown_credit(self):
        case = example_case()
        case["facts"]["hours"] = {"value": None, "source_ids": []}
        expected = expected_fit()
        expected["label"] = "unknown"
        expected["assessments"]["hours"] = {"status": "unknown", "source_ids": []}
        expected["unknowns"].append("hours")
        response = solve(case)
        # This represents a mistaken but internally consistent known-hours answer.
        response["label"] = "potential_fit"
        response["assessments"]["hours"] = {"status": "match", "source_ids": ["hours"]}
        response["unknowns"].remove("hours")
        result = score(response, expected, case)
        self.assertEqual(result["unknowns_preserved"], 4)
        self.assertEqual(result["unknowns_required"], 5)
        self.assertFalse(result["unknowns_exact"])
        self.assertEqual(result["missing_unknowns"], ["hours"])

    def test_blanket_unknown_answer_cannot_receive_full_credit(self):
        case = example_case()
        response = solve(case)
        response["label"] = "unknown"
        for field in response["assessments"]:
            response["assessments"][field]["status"] = "unknown"
            response["unknowns"].append(field)
        result = score(response, expected_fit(), case)
        self.assertFalse(result["label_correct"])
        self.assertEqual(sum(result["field_correct"].values()), 0)
        self.assertFalse(result["unknowns_exact"])
        self.assertEqual(len(result["extra_unknowns"]), 4)

    def test_protected_claims_reject_inferred_values(self):
        for field in ("seats", "admission", "eligibility", "outcomes"):
            for value in (True, False, "available"):
                with self.subTest(field=field, value=value):
                    case = example_case()
                    response = solve(case)
                    response["claims"][field] = value
                    with self.assertRaises(ValueError):
                        validate_response(response, case)

    def test_omitted_protected_unknown_rejected(self):
        case = example_case()
        response = solve(case)
        response["unknowns"].remove("seats")
        with self.assertRaises(ValueError):
            validate_response(response, case)

    def test_wrong_case_and_unresolved_response_source_rejected(self):
        case = example_case()
        for mutate in (
            lambda r: r.update(case_id="other-case"),
            lambda r: r["assessments"]["hours"].update(source_ids=["absent"]),
            lambda r: r["assessments"]["hours"].update(source_ids=["hours", "hours"]),
        ):
            response = solve(case)
            mutate(response)
            with self.assertRaises(ValueError):
                validate_response(response, case)

    def test_duplicate_sources_unresolved_facts_and_invalid_times_rejected(self):
        mutations = (
            lambda c: c["sources"].append(copy.deepcopy(c["sources"][0])),
            lambda c: c["facts"]["hours"].update(source_ids=["absent"]),
            lambda c: c["facts"]["hours"].update(value={"start": "24:00", "end": "25:00"}),
            lambda c: c["facts"]["hours"].update(value={"start": "18:00", "end": "15:00"}),
            lambda c: c["facts"]["recurring"].update(value=1),
            lambda c: c.update(synthetic=False),
        )
        for mutate in mutations:
            case = example_case()
            mutate(case)
            with self.assertRaises(ValueError):
                validate_case(case)

    def test_conflicts_require_two_sources_and_null_value(self):
        for value, ids in ((None, ["hours"]), ({"start": "14:30", "end": "18:30"}, ["hours", "unrelated"])):
            case = example_case()
            case["conflicts"] = ["hours"]
            case["facts"]["hours"] = {"value": value, "source_ids": ids}
            with self.assertRaises(ValueError):
                validate_case(case)

    def test_json_duplicate_keys_and_nonfinite_numbers_rejected(self):
        for text in ('{"label": "unknown", "label": "potential_fit"}', '{"x":NaN}', '{"x":Infinity}'):
            with self.subTest(text=text), self.assertRaises(ValueError):
                loads(text)

    def test_errors_stay_in_every_metric_denominator(self):
        expected = expected_fit()
        good = score(solve(example_case()), expected, example_case())
        summary = aggregate([{"error": None, "scores": good}, {"error": {"kind": "timeout"}, "scores": None}],
                            {"cases": [expected, copy.deepcopy(expected)]})
        self.assertEqual(summary["errors"], 1)
        self.assertEqual(summary["schema_valid"], {"passed": 1, "total": 2})
        self.assertEqual(summary["label_correctness"], {"passed": 1, "total": 2})
        self.assertEqual(summary["field_correctness"], {"passed": 4, "total": 8})
        self.assertEqual(summary["evidence_support"], {"passed": 4, "total": 8})
        self.assertEqual(summary["unknown_preservation"], {"passed": 4, "total": 8})

    def test_reference_labels_and_unknowns_must_be_consistent(self):
        dataset = {"schema_version": "care-fit.v1", "synthetic": True, "cases": [example_case()]}
        for mutation in (lambda e: e.update(label="mismatch"), lambda e: e["unknowns"].append("hours")):
            reference = expected_fit()
            mutation(reference)
            with tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / "expected.json"
                path.write_text(json.dumps({"schema_version": "care-fit.v1", "review_status": "draft_pending_domain_review", "cases": [reference]}), encoding="utf-8")
                with self.assertRaises(ValueError):
                    load_expected(path, dataset)


class RunnerTests(unittest.TestCase):
    def run_adapter(self, source, timeout=5):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "adapter.py"
            path.write_text(source, encoding="utf-8")
            return run_case(example_case(), expected_fit(), path, timeout)

    def test_adapter_gets_case_not_reference_answers(self):
        source = """from labbench.baseline import solve as baseline
def solve(case):
    assert set(case) == {'case_id', 'synthetic', 'need', 'sources', 'facts', 'conflicts'}
    assert 'label' not in case and 'expected' not in case
    return baseline(case)
"""
        record = self.run_adapter(source)
        self.assertIsNone(record["error"])
        self.assertTrue(record["scores"]["label_correct"])
        self.assertGreaterEqual(record["resources"]["worker_cpu_seconds"], 0)
        self.assertGreater(record["resources"]["wall_seconds"], 0)
        self.assertIsNone(record["resources"]["peak_memory_bytes"])
        self.assertIsNone(record["resources"]["gpu_memory_bytes"])

    def test_timeout_is_reported(self):
        record = self.run_adapter("import time\ndef solve(case):\n    time.sleep(2)\n", timeout=0.2)
        self.assertEqual(record["error"]["kind"], "timeout")
        self.assertIsNone(record["scores"])

    def test_crash_is_reported_without_exception_secret(self):
        record = self.run_adapter("def solve(case):\n    raise RuntimeError('private-debug-sentinel')\n")
        self.assertEqual(record["error"]["kind"], "adapter_error")
        self.assertNotIn("private-debug-sentinel", json.dumps(record))

    def test_malformed_return_and_stdout_pollution_are_reported(self):
        for source in (
            "def solve(case):\n    return {'label': 'potential_fit'}\n",
            "from labbench.baseline import solve as baseline\ndef solve(case):\n    print('debug text')\n    return baseline(case)\n",
        ):
            with self.subTest(source=source):
                record = self.run_adapter(source)
                self.assertEqual(record["error"]["kind"], "invalid_response")
                self.assertIsNone(record["scores"])


class PublishedFixtureIntegrationTests(unittest.TestCase):
    def test_practice_and_evaluation_are_separate_valid_sets(self):
        identifiers = []
        for split in ("practice", "evaluation"):
            dataset = load_dataset(ROOT / "data" / "care-fit" / (split + ".json"))
            expected = load_expected(ROOT / "data" / "care-fit" / (split + ".expected.json"), dataset)
            self.assertEqual(expected["review_status"], "draft_pending_domain_review")
            identifiers.append({case["case_id"] for case in dataset["cases"]})
            for case in dataset["cases"]:
                self.assertNotIn("label", case)
                self.assertNotIn("assessments", case)
        self.assertTrue(identifiers[0].isdisjoint(identifiers[1]))

    def test_baseline_and_example_adapter_use_same_cli(self):
        with tempfile.TemporaryDirectory() as directory:
            for adapter_args in ([], ["--adapter", "solutions/care-fit/adapter-example/adapter.py"]):
                with self.subTest(adapter_args=adapter_args):
                    output = Path(directory) / ("adapter.json" if adapter_args else "baseline.json")
                    command = [sys.executable, "-m", "labbench", "run", "--split", "evaluation", "--output", str(output)] + adapter_args
                    run = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=30)
                    self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
                    report = json.loads(output.read_text(encoding="utf-8"))
                    self.assertTrue(report["synthetic"])
                    self.assertEqual(report["summary"]["errors"], 0)
                    self.assertGreater(report["summary"]["schema_valid"]["total"], 0)
                    self.assertEqual(len(report["inputs_sha256"]), 64)
                    self.assertEqual(len(report["expected_sha256"]), 64)

    def test_cli_incorrect_answer_returns_failure_and_keeps_breakdown(self):
        with tempfile.TemporaryDirectory() as directory:
            adapter = Path(directory) / "wrong.py"
            adapter.write_text("from labbench.baseline import solve as baseline\ndef solve(case):\n    r = baseline(case)\n    r['label'] = 'unknown'\n    for field in r['assessments']:\n        r['assessments'][field]['status'] = 'unknown'\n        if field not in r['unknowns']:\n            r['unknowns'].append(field)\n    return r\n", encoding="utf-8")
            output = Path(directory) / "wrong-result.json"
            run = subprocess.run([sys.executable, "-m", "labbench", "run", "--adapter", str(adapter), "--output", str(output)],
                                 cwd=ROOT, capture_output=True, text=True, timeout=30)
            self.assertEqual(run.returncode, 1, run.stdout + run.stderr)
            report = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(report["summary"]["errors"], 0)
            self.assertLess(report["summary"]["label_correctness"]["passed"], report["summary"]["label_correctness"]["total"])
            self.assertLess(report["summary"]["unknowns_exact"]["passed"], report["summary"]["unknowns_exact"]["total"])


if __name__ == "__main__":
    unittest.main()

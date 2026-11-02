"""Task-package boundaries, provenance and CLI reporting checks."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

from labbench.package import load_package

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "task-environments" / "care-fit" / "package.json"


class PackageLoaderTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.container = Path(self.temporary.name)
        self.checkout = self.container / "checkout"
        self.checkout.mkdir()
        # Copy only referenced package files, preserving their repository paths.
        _, paths, _ = load_package(MANIFEST, ROOT)
        for source in paths.values():
            destination = self.checkout / source.relative_to(ROOT)
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, destination)
        self.manifest = self.checkout / MANIFEST.relative_to(ROOT)

    def change_manifest(self, change):
        data = json.loads(self.manifest.read_text(encoding="utf-8"))
        change(data)
        self.manifest.write_text(json.dumps(data), encoding="utf-8")

    def change_linked_json(self, reference, change):
        manifest = json.loads(self.manifest.read_text(encoding="utf-8"))
        path = self.manifest.parent / manifest[reference]
        data = json.loads(path.read_text(encoding="utf-8"))
        change(data)
        path.write_text(json.dumps(data), encoding="utf-8")

    def test_valid_package_resolves_actual_inputs_and_hashes_every_reference(self):
        data, paths, hashes = load_package(self.manifest, self.checkout)
        self.assertEqual(data["schema_version"], "lab-task-environment.v1")
        self.assertEqual(data["id"], "care-fit")
        self.assertEqual(data["execution"]["isolation"], "none")
        self.assertIsNone(data["model"]["endpoint"])
        self.assertEqual(set(paths), set(hashes))
        self.assertEqual(paths["practice.inputs"], self.checkout / "data/care-fit/practice.json")
        self.assertEqual(paths["evaluation.expected"], self.checkout / "data/care-fit/evaluation.expected.json")
        for name, path in paths.items():
            with self.subTest(reference=name):
                self.assertTrue(path.is_relative_to(self.checkout))
                self.assertTrue(path.is_file())
                self.assertEqual(hashes[name], hashlib.sha256(path.read_bytes()).hexdigest())

    def test_unsupported_schema_version_rejected(self):
        self.change_manifest(lambda data: data.update(schema_version="lab-task-environment.v99"))
        with self.assertRaises(ValueError):
            load_package(self.manifest, self.checkout)

    def test_malformed_package_version_rejected(self):
        for value in ("1", "v1.0.0", "1.2", "1.2.3-extra", 1, None):
            with self.subTest(value=value):
                self.change_manifest(lambda data: data.update(version=value))
                with self.assertRaises(ValueError):
                    load_package(self.manifest, self.checkout)

    def test_unknown_manifest_key_rejected(self):
        self.change_manifest(lambda data: data.update(undeclared="ignored?"))
        with self.assertRaises(ValueError):
            load_package(self.manifest, self.checkout)

    def test_unknown_execution_key_rejected(self):
        self.change_manifest(lambda data: data["execution"].update(remote_runner="https://example.invalid"))
        with self.assertRaises(ValueError):
            load_package(self.manifest, self.checkout)

    def test_absolute_reference_rejected_even_when_inside_checkout(self):
        self.change_manifest(lambda data: data.update(system_prompt=str(self.manifest.parent / "system-prompt.md")))
        with self.assertRaises(ValueError):
            load_package(self.manifest, self.checkout)

    def test_reference_escaping_checkout_rejected(self):
        outside = self.container / "outside.md"
        outside.write_text("Test file outside the package checkout.", encoding="utf-8")
        self.change_manifest(lambda data: data.update(system_prompt="../../../outside.md"))
        with self.assertRaises(ValueError):
            load_package(self.manifest, self.checkout)

    def test_manifest_outside_checkout_rejected(self):
        with self.assertRaises(ValueError):
            load_package(MANIFEST, self.checkout)

    def test_missing_reference_rejected(self):
        self.change_manifest(lambda data: data.update(system_prompt="missing-system-prompt.md"))
        with self.assertRaises(ValueError):
            load_package(self.manifest, self.checkout)

    def test_declared_shared_endpoint_rejected(self):
        self.change_manifest(lambda data: data["model"].update(endpoint="https://example.invalid/inference"))
        with self.assertRaises(ValueError):
            load_package(self.manifest, self.checkout)

    def test_claimed_enforced_isolation_rejected(self):
        self.change_manifest(lambda data: data["execution"].update(isolation="container"))
        with self.assertRaises(ValueError):
            load_package(self.manifest, self.checkout)

    def test_invalid_timeouts_rejected(self):
        for value in (0, -1, True, "10"):
            with self.subTest(value=value):
                self.change_manifest(lambda data: data["execution"].update(timeout_seconds=value))
                with self.assertRaises(ValueError):
                    load_package(self.manifest, self.checkout)

    def test_wrong_protected_fields_rejected_even_when_other_behavior_matches(self):
        self.change_linked_json("behavior", lambda data: data.update(protected_unknowns=["seats", "admission", "eligibility"]))
        with self.assertRaises(ValueError):
            load_package(self.manifest, self.checkout)

    def test_wrong_label_precedence_rejected(self):
        self.change_linked_json("behavior", lambda data: data.update(label_precedence=["unknown", "mismatch", "potential_fit"]))
        with self.assertRaises(ValueError):
            load_package(self.manifest, self.checkout)

    def test_wrong_route_order_rejected(self):
        self.change_linked_json("routepack", lambda data: data["steps"].reverse())
        with self.assertRaises(ValueError):
            load_package(self.manifest, self.checkout)

    def test_false_permission_enforcement_claim_rejected(self):
        self.change_linked_json("permissions", lambda data: data.update(enforcement_status="fully_sandboxed"))
        with self.assertRaises(ValueError):
            load_package(self.manifest, self.checkout)

    def test_unknown_tools_schema_rejected(self):
        self.change_linked_json("tools", lambda data: data.update(schema_version="remote-tools.v2"))
        with self.assertRaises(ValueError):
            load_package(self.manifest, self.checkout)

    def test_route_input_contract_drift_rejected(self):
        self.change_linked_json("routepack", lambda data: data.update(input_contract="real-family-record.v1"))
        with self.assertRaises(ValueError):
            load_package(self.manifest, self.checkout)

    def test_route_evidence_cannot_claim_verified_research(self):
        self.change_linked_json("routepack", lambda data: data["evidence"].update(kind="verified_real_records"))
        with self.assertRaises(ValueError):
            load_package(self.manifest, self.checkout)

    def test_route_permission_reference_must_match_manifest(self):
        self.change_linked_json("routepack", lambda data: data.update(permission_references=["other-permissions.json"]))
        with self.assertRaises(ValueError):
            load_package(self.manifest, self.checkout)

    def test_route_implementation_cannot_silently_replace_comparison(self):
        self.change_linked_json("routepack", lambda data: data["steps"][1].update(implementation="remote.agent:solve"))
        with self.assertRaises(ValueError):
            load_package(self.manifest, self.checkout)

    def test_route_tool_binding_cannot_grant_expected_answers(self):
        self.change_linked_json("routepack", lambda data: data["steps"][1].update(tools=["host.evaluate"]))
        with self.assertRaises(ValueError):
            load_package(self.manifest, self.checkout)

    def test_behavior_and_permission_schema_versions_rejected(self):
        manifest = json.loads(self.manifest.read_text(encoding="utf-8"))
        for reference in ("behavior", "permissions"):
            with self.subTest(reference=reference):
                path = self.manifest.parent / manifest[reference]
                original = path.read_text(encoding="utf-8")
                self.change_linked_json(reference, lambda data: data.update(schema_version="unsupported.v99"))
                with self.assertRaises(ValueError):
                    load_package(self.manifest, self.checkout)
                path.write_text(original, encoding="utf-8")

    def test_tool_ids_and_side_effects_must_match_local_functions(self):
        path = self.manifest.parent / "tools.json"
        original = path.read_text(encoding="utf-8")
        for mutation in (
            lambda data: data["task_tools"][0].update(id="network.fetch"),
            lambda data: data["task_tools"][1].update(side_effects="write to remote service"),
        ):
            self.change_linked_json("tools", mutation)
            with self.assertRaises(ValueError):
                load_package(self.manifest, self.checkout)
            path.write_text(original, encoding="utf-8")

    def test_requested_permissions_cannot_expand_network_or_reference_access(self):
        path = self.manifest.parent / "permissions.json"
        original = path.read_text(encoding="utf-8")
        for mutation in (
            lambda data: data["requested_task_access"].update(network=["https://example.invalid"]),
            lambda data: data["requested_task_access"].update(expected_answers=True),
            lambda data: data["host_access"].update(write=["deployed public endpoint"]),
        ):
            self.change_linked_json("permissions", mutation)
            with self.assertRaises(ValueError):
                load_package(self.manifest, self.checkout)
            path.write_text(original, encoding="utf-8")

    def test_system_prompt_edit_changes_only_that_file_hash(self):
        _, paths, before = load_package(self.manifest, self.checkout)
        prompt = paths["system_prompt"]
        prompt.write_text(prompt.read_text(encoding="utf-8") + "\nTest revision to the task instruction.\n", encoding="utf-8")
        _, _, after = load_package(self.manifest, self.checkout)
        self.assertNotEqual(before["system_prompt"], after["system_prompt"])
        self.assertEqual({name: value for name, value in before.items() if name != "system_prompt"},
                         {name: value for name, value in after.items() if name != "system_prompt"})


class PackageReportTests(unittest.TestCase):
    def test_report_records_package_identity_file_hashes_and_actual_timeout(self):
        package, _, hashes = load_package(MANIFEST, ROOT)
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "package-report.json"
            result = subprocess.run(
                [sys.executable, "-m", "labbench", "run", "--split", "practice", "--package", str(MANIFEST),
                 "--timeout", "7", "--output", str(output)],
                cwd=ROOT, capture_output=True, text=True, timeout=30,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            report = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(report["package"]["id"], package["id"])
            self.assertEqual(report["package"]["version"], package["version"])
            self.assertEqual(report["package"]["schema_version"], "lab-task-environment.v1")
            self.assertEqual(report["package"]["file_hashes"], hashes)
            self.assertEqual(report["package"]["isolation"], "none")
            self.assertEqual(report["package"]["shared_model"], "proposed_not_configured")
            self.assertEqual(report["runtime"]["timeout_seconds_per_case"], 7)
            self.assertEqual(report["inputs_sha256"], hashes["practice.inputs"])
            self.assertEqual(report["expected_sha256"], hashes["practice.expected"])


if __name__ == "__main__":
    unittest.main()

"""Run: python -m labbench run --split practice."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import platform
import subprocess
import sys
import time
from .contract import VERSION, load_dataset, load_expected, loads
from .evaluate import aggregate, score
from .package import load_package

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_case(case, expected, adapter, timeout):
    command = [sys.executable, "-m", "labbench.worker"]
    if adapter:
        command.append(str(adapter))
    started = time.perf_counter()
    record = {"case_id": case["case_id"], "error": None, "response": None, "scores": None,
              "resources": {"wall_seconds": None, "worker_cpu_seconds": None,
                            "peak_memory_bytes": None, "gpu_memory_bytes": None}}
    try:
        result = subprocess.run(command, input=json.dumps(case), capture_output=True,
                                encoding="utf-8", cwd=ROOT, timeout=timeout)
        if result.returncode:
            record["error"] = {"kind": "adapter_error", "detail": "Worker failed; inspect adapter locally. Output is not logged."}
        else:
            envelope = loads(result.stdout)
            response = envelope["response"]
            record["scores"] = score(response, expected, case)
            record["response"] = response
            cpu = envelope["worker_cpu_seconds"]
            if isinstance(cpu, (int, float)) and math.isfinite(cpu) and cpu >= 0:
                record["resources"]["worker_cpu_seconds"] = cpu
    except subprocess.TimeoutExpired:
        record["error"] = {"kind": "timeout", "detail": "Worker exceeded per-case timeout."}
    except (ValueError, KeyError, TypeError, AttributeError) as exc:
        record["error"] = {"kind": "invalid_response", "detail": type(exc).__name__ + ": response failed JSON/contract validation."}
    except OSError as exc:
        record["error"] = {"kind": "runtime_error", "detail": type(exc).__name__}
    record["resources"]["wall_seconds"] = time.perf_counter() - started
    return record


def main(argv=None):
    parser = argparse.ArgumentParser(description="Synthetic care-fit challenge; no model or network required.")
    sub = parser.add_subparsers(dest="command", required=True)
    run = sub.add_parser("run")
    run.add_argument("--split", choices=("practice", "evaluation"), default="practice")
    run.add_argument("--adapter", type=Path, help="Reviewed local Python file exporting solve(case).")
    run.add_argument("--output", type=Path, default=Path("results/local/latest.json"))
    run.add_argument("--timeout", type=float, help="Worker seconds per case (package default 10).")
    run.add_argument("--package", type=Path, default=ROOT / "task-environments/care-fit/package.json")
    args = parser.parse_args(argv)
    if args.timeout is not None and (not math.isfinite(args.timeout) or args.timeout <= 0):
        parser.error("--timeout must be a finite positive number")
    adapter = args.adapter.resolve() if args.adapter else None
    if adapter and (not adapter.is_file() or adapter.suffix != ".py"):
        parser.error("--adapter must be an existing Python file")
    try:
        package, package_paths, package_hashes = load_package(args.package, ROOT)
    except (OSError, ValueError, KeyError, TypeError, AttributeError):
        parser.error("invalid task package; inspect manifest, references and implemented contract")
    data_path = package_paths[args.split + ".inputs"]
    expected_path = package_paths[args.split + ".expected"]
    timeout = args.timeout if args.timeout is not None else package["execution"]["timeout_seconds"]
    output = args.output.resolve()
    # A report must not replace source, input, reference answers or an adapter.
    if output.exists() and "results" not in output.parts:
        parser.error("refusing to overwrite a file outside a results directory")
    if output in set(package_paths.values()) | {adapter}:
        parser.error("report path overlaps an input")
    try:
        dataset = load_dataset(data_path)
        expected = load_expected(expected_path, dataset)
        refs = {r["case_id"]: r for r in expected["cases"]}
        records = [run_case(case, refs[case["case_id"]], adapter, timeout) for case in dataset["cases"]]
        report = {"schema_version": VERSION, "synthetic": True, "split": args.split,
                  "created_at": datetime.now(timezone.utc).isoformat(),
                  "review_status": expected["review_status"],
                  "package": {"id": package["id"], "version": package["version"], "schema_version": package["schema_version"],
                              "file_hashes": package_hashes, "isolation": package["execution"]["isolation"],
                              "shared_model": package["model"]["shared_binding"]},
                  "implementation": {"adapter": adapter.name if adapter else "deterministic_baseline",
                                     "sha256": digest(adapter or ROOT / "labbench" / "baseline.py"),
                                     "harness_sha256": {p.name: digest(p) for p in sorted((ROOT / "labbench").glob("*.py"))}},
                  "inputs_sha256": digest(data_path), "expected_sha256": digest(expected_path),
                  "runtime": {"python": platform.python_version(), "os": platform.system(),
                              "timeout_seconds_per_case": timeout,
                              "model": "none" if adapter is None else "not_reported",
                              "resource_note": "Wall time includes worker startup. CPU covers the Python worker, not subprocess/model services. Memory/GPU are not measured. No resource quota or security sandbox is provided."},
                  "summary": aggregate(records, expected), "cases": records,
                  "limitations": ["Public synthetic evaluation set, not a blind benchmark or real-family validation.",
                                  "Citations are checked against reference IDs per field; prose entailment and rationale require human review.",
                                  "Hashes cover the adapter file only; record supporting files, model and environment in the result template."]}
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(report, indent=2, ensure_ascii=False, allow_nan=False) + "\n", encoding="utf-8")
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as exc:
        print("Harness could not load cases or write report: " + type(exc).__name__, file=sys.stderr)
        return 2
    print("Synthetic " + args.split + " results (domain review pending):")
    for metric, value in report["summary"].items():
        print(f"  {metric}: {value['passed']}/{value['total']}" if isinstance(value, dict) else f"  {metric}: {value}")
    print("Report: " + str(output))
    print("Memory/GPU not measured. Human evidence and rationale review required.")
    return 1 if report["summary"]["errors"] or any(v["passed"] != v["total"] for v in report["summary"].values() if isinstance(v, dict)) else 0


if __name__ == "__main__":
    raise SystemExit(main())

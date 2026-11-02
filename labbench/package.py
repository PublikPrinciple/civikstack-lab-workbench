"""Validate and resolve the current local task-environment package format.

Manifest references are confined to the checkout. This does not sandbox adapters.
"""
import hashlib
import math
from pathlib import Path
import re
from .contract import FIELDS, PROTECTED, keys, loads, require


def load_package(path, root):
    root, path = root.resolve(), path.resolve()
    require(path.is_relative_to(root), "package must be inside the checkout")
    data = loads(path.read_text(encoding="utf-8"))
    refs = ("routepack", "system_prompt", "behavior", "tools", "permissions", "adapter_contract", "model_policy")
    keys(data, ("$schema", "schema_version", "id", "version", "purpose", "execution", "model", "data") + refs, "package")
    require(data["schema_version"] == "lab-task-environment.v1", "unsupported package schema")
    require(isinstance(data["id"], str) and re.fullmatch(r"[a-z][a-z0-9-]*", data["id"]), "invalid package ID")
    require(isinstance(data["version"], str) and re.fullmatch(r"\d+\.\d+\.\d+", data["version"]), "invalid package version")
    require(isinstance(data["purpose"], str) and data["purpose"].strip(), "package purpose missing")
    paths = {}

    def resolve(name, value):
        require(isinstance(value, str) and value and not Path(value).is_absolute(), "package references must be relative paths")
        target = (path.parent / value).resolve()
        require(target.is_relative_to(root) and target.is_file(), "package reference missing or outside checkout")
        paths[name] = target
        return target

    resolve("schema", data["$schema"])
    for ref in refs:
        resolve(ref, data[ref])
    keys(data["data"], ("practice", "evaluation"), "package splits")
    for split, sources in data["data"].items():
        keys(sources, ("inputs", "expected"), "split paths")
        for kind, value in sources.items():
            resolve(split + "." + kind, value)
    execution = data["execution"]
    keys(execution, ("harness", "baseline", "evaluator", "mode", "isolation", "timeout_seconds"), "execution")
    require(execution["harness"] == "labbench" and execution["baseline"] == "labbench.baseline:solve"
            and execution["evaluator"] == "labbench.evaluate" and execution["mode"] == "local_reviewed_code"
            and execution["isolation"] == "none", "only the reviewed local harness is implemented")
    timeout = execution["timeout_seconds"]
    require(type(timeout) in (int, float) and math.isfinite(timeout) and timeout > 0, "invalid timeout")
    model = data["model"]
    require(model == {"required_for_baseline": False, "shared_binding": "proposed_not_configured",
                      "endpoint": None, "parameter_ceiling": None, "policy_status": "unresolved_1B_vs_7B"},
            "shared model bindings and policy changes are not implemented")
    route = loads(paths["routepack"].read_text(encoding="utf-8"))
    keys(route, ("schema_version", "id", "version", "integration_status", "input_contract", "output_contract", "evidence", "permission_references", "steps"), "routepack")
    require(route.get("schema_version") == "lab-routepack.v1" and route.get("integration_status") == "local_contract_no_RPOS_adapter",
            "unsupported routepack")
    require(route["input_contract"] == "care-fit.v1 case" and route["output_contract"] == "care-fit.v1 response",
            "unsupported route input/output")
    require(route["permission_references"] == [data["permissions"]], "route permissions must match manifest")
    require(route["evidence"] == {"scope": "case.sources", "kind": "newly_authored_synthetic",
                                  "reference_review": "draft_pending_domain_review"}, "unsupported route evidence")
    require([step.get("id") for step in route.get("steps", [])] == ["validate", "compare", "respond", "evaluate"],
            "route does not match implemented execution")
    implemented = [("labbench.contract.validate_case", ["case.read"]),
                   ("labbench.baseline.solve", ["case.read"]),
                   ("labbench.contract.validate_response", ["response.emit"]),
                   ("labbench.evaluate.score", ["host.evaluate"])]
    for step, (implementation, tool_ids) in zip(route["steps"], implemented):
        keys(step, ("id", "action", "implementation", "tools"), "route step")
        require(step["implementation"] == implementation and step["tools"] == tool_ids,
                "route implementation or tools differ from local runner")
    behavior = loads(paths["behavior"].read_text(encoding="utf-8"))
    require(behavior.get("schema_version") == "care-fit-behavior.v1"
            and behavior.get("fields") == list(FIELDS) and behavior.get("protected_unknowns") == list(PROTECTED)
            and behavior.get("label_precedence") == ["mismatch", "unknown", "potential_fit"],
            "behavior does not match the current contract")
    permissions = loads(paths["permissions"].read_text(encoding="utf-8"))
    keys(permissions, ("schema_version", "requested_task_access", "host_access", "enforcement_status", "hosted_requirement"), "permissions")
    require(permissions["schema_version"] == "lab-permissions.v1"
            and permissions.get("enforcement_status") == "declarative_only_local_runner_is_not_a_sandbox",
            "package must disclose local isolation limit")
    require(permissions["requested_task_access"] == {"read": ["current synthetic case only"],
            "write": ["response to host evaluator"], "network": [], "credentials": [],
            "desktop_or_lan": False, "expected_answers": False}, "unsupported requested permissions")
    require(permissions["host_access"] == {"read": ["reference answers"], "write": ["reviewable result report"]},
            "unsupported host permissions")
    tools = loads(paths["tools"].read_text(encoding="utf-8"))
    keys(tools, ("schema_version", "task_tools", "host_tools", "implementation_note"), "tools")
    require(tools.get("schema_version") == "lab-tools.v1", "unsupported tool contract")
    declared_tools = tools["task_tools"] + tools["host_tools"]
    require([item["id"] for item in tools["task_tools"]] == ["case.read", "response.emit"]
            and [item["id"] for item in tools["host_tools"]] == ["host.evaluate"], "unsupported tool IDs")
    for item, effects in zip(declared_tools, ("none", "response only", "local result file")):
        keys(item, ("id", "input", "output", "side_effects"), "tool")
        require(item["side_effects"] == effects, "unsupported tool side effects")
    paths["manifest"] = path
    hashes = {name: hashlib.sha256(target.read_bytes()).hexdigest() for name, target in paths.items()}
    return data, paths, hashes

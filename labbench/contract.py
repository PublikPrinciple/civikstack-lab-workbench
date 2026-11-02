"""Validate the bounded care-fit contract; no inference from absent facts."""
import json
import re

VERSION = "care-fit.v1"
FIELDS = ("service_type", "days", "hours", "recurring")
PROTECTED = ("seats", "admission", "eligibility", "outcomes")
DAYS = {"mon", "tue", "wed", "thu", "fri", "sat", "sun"}
LABELS = {"potential_fit", "mismatch", "unknown"}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, "duplicate JSON key: " + key)
        result[key] = value
    return result


def loads(text):
    def reject_constant(value):
        raise ValueError("non-finite JSON number: " + value)
    return json.loads(text, object_pairs_hook=unique_object,
                      parse_constant=reject_constant)


def keys(value, required, name):
    require(isinstance(value, dict) and set(value) == set(required),
            name + " has incorrect fields")


def strings(value, name, allow_empty=True):
    require(isinstance(value, list) and all(isinstance(x, str) and x for x in value),
            name + " must be a string list")
    require(len(value) == len(set(value)), name + " contains duplicates")
    require(allow_empty or bool(value), name + " must not be empty")


def valid_value(field, value):
    if field == "service_type":
        require(value in ("daily_afterschool_care", "tutoring", "drop_in", "event"),
                "invalid service_type")
    elif field == "days":
        strings(value, "days", allow_empty=False)
        require(set(value) <= DAYS, "invalid weekday")
    elif field == "hours":
        keys(value, ("start", "end"), "hours")
        require(all(isinstance(v, str) and re.fullmatch(r"(?:[01]\d|2[0-3]):[0-5]\d", v)
                    for v in value.values()), "hours must be local HH:MM")
        require(value["start"] < value["end"], "hours must be a same-day interval")
    else:
        require(type(value) is bool, "recurring must be boolean")


def validate_case(case):
    keys(case, ("case_id", "synthetic", "need", "sources", "facts", "conflicts"), "case")
    require(isinstance(case["case_id"], str) and bool(case["case_id"]), "missing case ID")
    require(case["synthetic"] is True, "only synthetic cases are accepted")
    keys(case["need"], FIELDS, "need")
    keys(case["facts"], FIELDS, "facts")
    require(isinstance(case["sources"], list) and bool(case["sources"]), "missing sources")
    source_ids = []
    for source in case["sources"]:
        keys(source, ("id", "text"), "source")
        require(all(isinstance(source[k], str) and source[k].strip() for k in source),
                "invalid source")
        source_ids.append(source["id"])
    strings(source_ids, "source IDs", allow_empty=False)
    strings(case["conflicts"], "conflicts")
    require(set(case["conflicts"]) <= set(FIELDS), "unknown conflict field")
    for field in FIELDS:
        valid_value(field, case["need"][field])
        fact = case["facts"][field]
        keys(fact, ("value", "source_ids"), "fact")
        strings(fact["source_ids"], "fact source IDs")
        require(set(fact["source_ids"]) <= set(source_ids), "unresolved fact source")
        if fact["value"] is not None:
            valid_value(field, fact["value"])
            require(bool(fact["source_ids"]), "known facts require evidence")
        if field in case["conflicts"]:
            require(fact["value"] is None and len(fact["source_ids"]) >= 2,
                    "a conflict needs null and at least two sources")
    require(case["need"]["service_type"] == "daily_afterschool_care"
            and case["need"]["recurring"] is True, "outside care-fit challenge scope")


def validate_response(response, case):
    keys(response, ("case_id", "label", "assessments", "unknowns", "claims", "rationale"), "response")
    require(response["case_id"] == case["case_id"], "wrong case ID")
    require(isinstance(response["label"], str) and response["label"] in LABELS, "invalid label")
    keys(response["assessments"], FIELDS, "assessments")
    ids = {s["id"] for s in case["sources"]}
    for field in FIELDS:
        item = response["assessments"][field]
        keys(item, ("status", "source_ids"), "assessment")
        require(isinstance(item["status"], str) and item["status"] in {"match", "mismatch", "unknown"},
                "invalid assessment status")
        strings(item["source_ids"], "assessment source IDs")
        require(set(item["source_ids"]) <= ids, "unresolved response source")
        require(item["status"] == "unknown" or bool(item["source_ids"]),
                "a known assessment requires evidence")
    strings(response["unknowns"], "unknowns")
    require(set(response["unknowns"]) <= set(PROTECTED + FIELDS), "unknown field name")
    keys(response["claims"], PROTECTED, "claims")
    require(all(value is None for value in response["claims"].values()),
            "seats, admission, eligibility and outcomes must remain null")
    require(set(PROTECTED) <= set(response["unknowns"]), "protected unknown omitted")
    require(isinstance(response["rationale"], str) and bool(response["rationale"].strip()),
            "rationale required for human review")


def load_dataset(path):
    dataset = loads(path.read_text(encoding="utf-8"))
    require(dataset.get("schema_version") == VERSION and dataset.get("synthetic") is True,
            "invalid dataset version or synthetic label")
    require(isinstance(dataset.get("cases"), list) and bool(dataset["cases"]), "empty dataset")
    for case in dataset["cases"]:
        validate_case(case)
    strings([case["case_id"] for case in dataset["cases"]], "case IDs", allow_empty=False)
    return dataset


def load_expected(path, dataset):
    expected = loads(path.read_text(encoding="utf-8"))
    require(expected.get("schema_version") == VERSION, "invalid expected version")
    require(expected.get("review_status") == "draft_pending_domain_review", "unexpected review status")
    require(isinstance(expected.get("cases"), list), "expected cases missing")
    strings([item["case_id"] for item in expected["cases"]], "expected IDs")
    indexed = {case["case_id"]: case for case in dataset["cases"]}
    require(set(indexed) == {item["case_id"] for item in expected["cases"]}, "expected/input ID mismatch")
    for item in expected["cases"]:
        keys(item, ("case_id", "label", "assessments", "unknowns", "review_note"), "expected case")
        validate_response({"case_id": item["case_id"], "label": item["label"],
                           "assessments": item["assessments"], "unknowns": item["unknowns"],
                           "claims": dict.fromkeys(PROTECTED), "rationale": item["review_note"]},
                          indexed[item["case_id"]])
        statuses = [v["status"] for v in item["assessments"].values()]
        label = "mismatch" if "mismatch" in statuses else "unknown" if "unknown" in statuses else "potential_fit"
        require(item["label"] == label, "inconsistent expected label")
        unknowns = set(PROTECTED) | {k for k, v in item["assessments"].items() if v["status"] == "unknown"}
        require(set(item["unknowns"]) == unknowns, "inconsistent expected unknowns")
    return expected

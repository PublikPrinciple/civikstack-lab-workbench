"""Compare supplied normalized facts. This does not extract facts from prose."""
from .contract import FIELDS, PROTECTED


def solve(case):
    assessments = {}
    for field in FIELDS:
        fact = case["facts"][field]
        value, need = fact["value"], case["need"][field]
        if value is None or field in case["conflicts"]:
            status = "unknown"
        else:
            if field == "days":
                matches = set(need) <= set(value)
            elif field == "hours":
                matches = value["start"] <= need["start"] and value["end"] >= need["end"]
            else:
                matches = value == need
            status = "match" if matches else "mismatch"
        assessments[field] = {"status": status, "source_ids": list(fact["source_ids"])}
    statuses = [a["status"] for a in assessments.values()]
    label = "mismatch" if "mismatch" in statuses else "unknown" if "unknown" in statuses else "potential_fit"
    return {
        "case_id": case["case_id"], "label": label, "assessments": assessments,
        "unknowns": list(PROTECTED) + [field for field in FIELDS if assessments[field]["status"] == "unknown"],
        "claims": dict.fromkeys(PROTECTED),
        "rationale": "Synthetic schedule/service comparison: " + "; ".join(
            field + "=" + a["status"] for field, a in assessments.items()) +
            ". Potential fit concerns these supplied dimensions only; human review is required.",
    }

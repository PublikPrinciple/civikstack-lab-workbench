"""Separate correctness, citation support and unknown preservation measures."""
from .contract import FIELDS, validate_response


def score(response, expected, case):
    validate_response(response, case)
    fields = {field: response["assessments"][field]["status"] == expected["assessments"][field]["status"]
              for field in FIELDS}
    evidence = {field: set(response["assessments"][field]["source_ids"]) ==
                      set(expected["assessments"][field]["source_ids"]) for field in FIELDS}
    required, actual = set(expected["unknowns"]), set(response["unknowns"])
    return {"label_correct": response["label"] == expected["label"],
            "field_correct": fields, "evidence_support": evidence,
            "unknowns_preserved": len(required & actual), "unknowns_required": len(required),
            "unknowns_exact": actual == required,
            "extra_unknowns": sorted(actual - required),
            "missing_unknowns": sorted(required - actual)}


def aggregate(records, expected):
    total = len(records)
    valid = [r["scores"] for r in records if r["error"] is None]
    return {
        "schema_valid": {"passed": len(valid), "total": total},
        "label_correctness": {"passed": sum(s["label_correct"] for s in valid), "total": total},
        "field_correctness": {"passed": sum(sum(s["field_correct"].values()) for s in valid), "total": total * len(FIELDS)},
        "evidence_support": {"passed": sum(sum(s["evidence_support"].values()) for s in valid), "total": total * len(FIELDS)},
        "unknown_preservation": {"passed": sum(s["unknowns_preserved"] for s in valid),
                                 "total": sum(len(item["unknowns"]) for item in expected["cases"])},
        "unknowns_exact": {"passed": sum(s["unknowns_exact"] for s in valid), "total": total},
        "errors": total - len(valid),
    }

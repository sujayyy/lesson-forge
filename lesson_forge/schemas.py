"""Provider-side format constraints; semantic release checks remain local."""
from .prompts import evidence_candidates
from .rubric import CRITERIA

CONTRACT_VERSION = "evidence-line-ids-v1"


def evidence_lines(lesson):
    return {f"L{i}": line for i, line in enumerate(evidence_candidates(lesson), 1)}


def resolve_evidence(value, lesson):
    """Resolve model-selected IDs, never guess or repair a model's selection."""
    if not isinstance(value, dict) or set(value) != {"checks"} or not isinstance(value["checks"], list):
        raise ValueError("Invalid evaluator response shape")
    options = {"": "", **evidence_lines(lesson)}
    checks = []
    for item in value["checks"]:
        if not isinstance(item, dict) or set(item) != {"id", "passed", "reason", "evidence_id", "fix"}:
            raise ValueError("Invalid evaluator checkpoint shape")
        ref = item["evidence_id"]
        if not isinstance(ref, str) or ref not in options:
            raise ValueError("Unknown evaluator evidence ID")
        checks.append({k: v for k, v in item.items() if k != "evidence_id"} | {"evidence": options[ref]})
    return {"checks": checks}


def strict_response_format(role, payload):
    if role == "generator":
        properties = {"lesson": {"type": "string"}}
    elif role == "evaluator":
        # Derive options from the actual lesson, not a caller's claimed quotes.
        references = [""] + list(evidence_lines(payload["lesson"]))
        fields = {
            "id": {"type": "string", "enum": list(CRITERIA)},
            "passed": {"type": "boolean"},
            "reason": {"type": "string"},
            "evidence_id": {"type": "string", "enum": references},
            "fix": {"type": "string"},
        }
        properties = {"checks": {"type": "array", "items": {
            "type": "object", "properties": fields,
            "required": list(fields), "additionalProperties": False,
        }}}
    else:
        raise ValueError("Unknown model role")
    return {"type": "json_schema", "json_schema": {
        "name": "lesson_forge_" + role, "strict": True,
        "schema": {"type": "object", "properties": properties,
                   "required": list(properties), "additionalProperties": False},
    }}

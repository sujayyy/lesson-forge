"""Provider-side format constraints; semantic release checks remain local."""
from .prompts import evidence_candidates
from .rubric import CRITERIA


def strict_response_format(role, payload):
    if role == "generator":
        properties = {"lesson": {"type": "string"}}
    elif role == "evaluator":
        # Derive options from the actual lesson, not a caller's claimed quotes.
        quotes = [""] + evidence_candidates(payload["lesson"])
        fields = {
            "id": {"type": "string", "enum": list(CRITERIA)},
            "passed": {"type": "boolean"},
            "reason": {"type": "string"},
            "evidence": {"type": "string", "enum": quotes},
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

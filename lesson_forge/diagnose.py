"""Re-evaluate a saved draft for diagnosis; never release or modify its run."""
import json
from datetime import datetime, timezone
from pathlib import Path
from .pipeline import write_json, load_pack
from .prompts import EVALUATOR, evidence_candidates
from .provider import ProviderError
from .rubric import CRITERIA, deterministic, validate_judgment


def run(provider, original, out_root):
    original = Path(original).resolve()
    manifest = json.loads((original / "manifest.json").read_text())
    index = manifest["attempt_count"]
    lesson = (original / f"attempt-{index}.md").read_text()
    pack = load_pack(original / "source_pack.json", manifest["topic"])
    payload = {"topic": pack["topic"], "sources": pack["sources"], "criteria": CRITERIA,
               "repeated_failure_focus": [], "lesson": lesson,
               "evidence_candidates": evidence_candidates(lesson)}
    out = Path(out_root) / ("diagnostic-" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ"))
    out.mkdir(parents=True)
    write_json(out / "evaluator-input.json", payload)
    result = {"original_run": str(original), "attempt": index, "status": "ERROR",
              "purpose": "Response-format diagnosis only; no release or memory update"}
    try:
        raw = provider.complete("evaluator", EVALUATOR, payload)
        write_json(out / "evaluator-output.json", raw)
        checks = deterministic(lesson, pack["sources"]) + validate_judgment(raw, lesson)
        result.update(status="VALID_RESPONSE", checks=checks)
        print("DIAGNOSTIC OK: evaluator returned valid verdicts.")
        print("Lesson checks failing:", ", ".join(c["id"] for c in checks if not c["passed"]) or "none")
    except (ProviderError, ValueError) as exc:
        result["error"] = str(exc)
        print("DIAGNOSTIC ERROR:", exc)
    result["provider_calls"] = provider.usage
    write_json(out / "diagnostic.json", result)
    print(f"Saved {out}. No lesson released; the original run is unchanged.")
    return 0 if result["status"] == "VALID_RESPONSE" else 1

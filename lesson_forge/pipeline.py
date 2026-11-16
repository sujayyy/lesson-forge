import difflib
import hashlib
import json
import re
import uuid
from datetime import datetime, timezone
from urllib.parse import urlparse
from . import __version__
from .demo import inject_error
from .memory import Memory
from .prompts import GENERATOR, EVALUATOR, evidence_candidates
from .provider import ProviderError
from .report import render_report
from .rubric import VERSION, HEADINGS, CRITERIA, deterministic, validate_judgment


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def write_json(path, value):
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    temporary.replace(path)


def load_pack(path, topic):
    pack = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(pack, dict) or not isinstance(pack.get("topic"), str):
        raise ValueError("Source pack requires a topic")
    aliases = pack.get("aliases", [])
    if not isinstance(aliases, list) or any(not isinstance(x, str) for x in aliases):
        raise ValueError("Source aliases must be strings")
    if topic.strip().casefold() not in {x.casefold() for x in [pack["topic"], *aliases]}:
        raise ValueError("Topic does not match source pack. Supply a reviewed --sources pack for this topic.")
    sources = pack.get("sources")
    if not isinstance(sources, list) or len(sources) < 2:
        raise ValueError("Provide at least two curated sources")
    seen = set()
    for s in sources:
        if not isinstance(s, dict) or any(not isinstance(s.get(k), str) for k in ("id", "title", "url")):
            raise ValueError("Each source requires string id, title and URL")
        if not re.fullmatch(r"S\d+", s["id"]) or s["id"] in seen:
            raise ValueError("Source IDs must be unique S<number> values")
        seen.add(s["id"])
        url = urlparse(s["url"])
        if url.scheme != "https" or not url.hostname:
            raise ValueError("Source URLs must use HTTPS")
        if not isinstance(s.get("facts"), list) or not s["facts"] or any(not isinstance(f, str) or not f.strip() for f in s["facts"]):
            raise ValueError("Each source needs nonempty factual notes")
        if "learner_facts" in s and (not isinstance(s["learner_facts"], list) or not s["learner_facts"] or any(not isinstance(f, str) or not f.strip() for f in s["learner_facts"])):
            raise ValueError("Learner facts must be a nonempty list of factual strings")
    return pack


def authoring_sources(sources):
    """Use reviewed plain-English paraphrases when supplied; preserve judge facts."""
    return [{**{k: v for k, v in s.items() if k != "learner_facts"},
             "facts": s.get("learner_facts", s["facts"])} for s in sources]


def run(provider, topic, source_path, out_root, memory_path, retries=2, injection="none", on_event=print):
    if type(retries) is not int or retries not in (0, 1, 2):
        raise ValueError("Retries must be 0, 1 or 2")
    if injection not in {"none", "first", "always"}:
        raise ValueError("Invalid injection mode")
    pack = load_pack(source_path, topic)
    if (provider.mode == "demo" or injection != "none") and pack["topic"] != "Introduction to RAG":
        raise ValueError("Offline fixture and error injection are RAG-specific")
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:8]
    run_dir = out_root / run_id
    run_dir.mkdir(parents=True, exist_ok=False)
    memory = Memory(memory_path)
    source_hash = digest(pack)
    scope = digest({"topic": pack["topic"], "sources": source_hash, "rubric": VERSION,
                    "criteria": CRITERIA, "mode": provider.mode,
                    "injection": injection != "none"})
    policy = memory.policy(scope)
    memory.snapshot(run_id, scope, policy)
    manifest = {"run_id": run_id, "topic": topic, "mode": provider.mode, "status": "RUNNING",
                "app_version": __version__, "rubric_version": VERSION, "source_hash": source_hash,
                "scope": scope, "policy": policy, "max_retries": retries, "injection": injection,
                "generator_model": provider.generator_model, "evaluator_model": provider.evaluator_model,
                "prompt_hashes": {"generator": digest(GENERATOR), "evaluator": digest(EVALUATOR)},
                "started_at": datetime.now(timezone.utc).isoformat()}
    attempts = []
    write_json(run_dir / "source_pack.json", pack)
    write_json(run_dir / "rubric.json", {"version": VERSION, "semantic": CRITERIA, "headings": HEADINGS})
    write_json(run_dir / "prompts.json", {"generator": GENERATOR, "evaluator": EVALUATOR})
    write_json(run_dir / "manifest.json", manifest)
    previous, feedback = "", []
    try:
        for index in range(1, retries + 2):
            on_event(f"[{run_id}] GENERATE attempt {index}/{retries + 1}")
            payload = {"topic": topic, "sources": authoring_sources(pack["sources"]), "required_headings": HEADINGS,
                       "criteria": CRITERIA, "persistent_hints": policy["hints"],
                       "previous_lesson": previous, "failed_checks": feedback,
                       "mechanical_requirements": "450–1000 prose words; mean sentence/line <=18 words; longest <=32; at least two supplied source IDs cited in body and all cited URLs listed."}
            write_json(run_dir / f"attempt-{index}-generator-input.json", payload)
            candidate = provider.complete("generator", GENERATOR, payload)
            write_json(run_dir / f"attempt-{index}-generator-output.json", candidate)
            if not isinstance(candidate, dict) or set(candidate) != {"lesson"} or not isinstance(candidate["lesson"], str) or not candidate["lesson"].strip() or len(candidate["lesson"]) > 60000:
                raise ValueError("Generator must return exactly one nonempty lesson string, <=60000 characters")
            lesson = candidate["lesson"]
            injected = injection == "always" or (injection == "first" and index == 1)
            if injected:
                modified = inject_error(lesson)
                if modified == lesson:
                    raise ValueError("Cannot inject demonstration error: Limits heading missing")
                lesson = modified
            (run_dir / f"attempt-{index}.md").write_text(lesson, encoding="utf-8")
            attempt = {"attempt": index, "lesson": lesson, "lesson_sha256": digest(lesson),
                       "injected": injected, "decision": "EVALUATING", "checks": [],
                       "diff": "".join(difflib.unified_diff(previous.splitlines(True), lesson.splitlines(True), fromfile="previous", tofile="current")) if previous else "First draft"}
            attempts.append(attempt)
            write_json(run_dir / "rejection_log.json", attempts)
            on_event(f"[{run_id}] EVALUATE attempt {index}")
            mechanical = deterministic(lesson, pack["sources"])
            # Do not send generator reasoning, prior verdicts or injection metadata to the judge.
            judge_payload = {"topic": topic, "sources": pack["sources"], "criteria": CRITERIA,
                             "repeated_failure_focus": policy["hints"], "lesson": lesson,
                             "evidence_candidates": evidence_candidates(lesson)}
            write_json(run_dir / f"attempt-{index}-evaluator-input.json", judge_payload)
            raw = provider.complete("evaluator", EVALUATOR, judge_payload)
            write_json(run_dir / f"attempt-{index}-evaluator-output.json", raw)
            checks = mechanical + validate_judgment(raw, lesson)
            feedback = [c for c in checks if not c["passed"]]
            attempt.update(checks=checks, decision="REJECT" if feedback else "PASS")
            write_json(run_dir / "rejection_log.json", attempts)
            if feedback:
                memory.record(scope, run_id, [c["id"] for c in feedback])
                on_event("  REJECT: " + ", ".join(c["id"] for c in feedback))
                previous = lesson
                continue
            # A fixture pass can never produce a production final_lesson.md.
            manifest["status"] = "SHIPPED" if provider.mode == "live" else "DEMO_PASSED"
            output_name = "final_lesson.md" if provider.mode == "live" else "demo_lesson.md"
            manifest["lesson_file"] = output_name
            manifest["accepted_attempt"] = index
            break
        else:
            manifest["status"] = "WITHHELD"
    except (ProviderError, ValueError, TypeError, KeyError, OSError) as exc:
        manifest["status"] = "ERROR"
        manifest["error"] = str(exc)
        if attempts and attempts[-1]["decision"] == "EVALUATING":
            attempts[-1]["decision"] = "ERROR"
    finally:
        manifest["completed_at"] = datetime.now(timezone.utc).isoformat()
        manifest["attempt_count"] = len(attempts)
        manifest["provider_calls"] = provider.usage
        manifest["policy_after_run"] = memory.policy(scope)
        memory.close()
        write_json(run_dir / "rejection_log.json", attempts)
        write_json(run_dir / "manifest.json", manifest)
        render_report(run_dir, manifest, attempts)
    if manifest["status"] in {"SHIPPED", "DEMO_PASSED"}:
        output = run_dir / manifest["lesson_file"]
        temporary = output.with_suffix(".tmp")
        temporary.write_text(lesson, encoding="utf-8")
        temporary.replace(output)
    on_event(f"[{run_id}] {manifest['status']}: {run_dir}")
    return run_dir, manifest

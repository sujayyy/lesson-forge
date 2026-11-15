"""All requirements are conjunctive: there is no score or partial credit."""
import re

VERSION = "1.0"
HEADINGS = ["Start here", "What it means", "Why it helps", "How it works",
            "A worked example", "Limits", "Try it yourself", "Recap", "Sources"]
CRITERIA = {
    "accuracy": "Every technical claim agrees with the supplied source facts. No invented capabilities, guarantees, or real-world facts. Clearly label invented teaching examples. Check the whole lesson for contradictions, including its ending and answers.",
    "foundations": "Explain the topic and every prerequisite from zero. For RAG: expand Retrieval-Augmented Generation, explain AI as software doing tasks that often need human intelligence, and explain a language model as software trained on text to produce text. Do not assume programming knowledge.",
    "coverage": "Explain what the topic is, one concrete reason it matters, and its mechanism in correct order. For RAG: prepare searchable documents; retrieve relevant passages for a question; give passages plus question to a language model; generate an answer. Say ordinary retrieval does not retrain the model, and RAG can still be wrong. Do not claim vector search or internet access is required.",
    "example": "Include one explicitly fictional, familiar Indian school/college example. Show the exact source note, a learner question, the retrieved passage, and an answer supported by that passage. Include an unanswered question and demonstrate saying the source does not contain the answer. Dates, numbers and conclusions must match the source note.",
    "language": "Use everyday English suitable for a class-12 graduate from a non-English-medium background. No unexplained idioms or unnecessarily formal vocabulary. Explain every technical term at or before its first substantive use; the expanded topic title is allowed before its explanation. Optional advanced terms can be omitted. Short sentences alone are insufficient.",
    "flow": "Teach prerequisites before the mechanism, then a worked example, then limits and practice. Each section develops the same topic without contradictory advice, distracting tangents or missing steps. The recap is accurate.",
    "practice": "Include at least two answerable learner questions with correct answers and short explanations: one about how the mechanism works and one about what to do when evidence is missing. They must test understanding, not just acronym recall.",
}
HINTS = {
    "accuracy": "Cross-check every factual sentence against a supplied fact. Remove unsupported guarantees and contradictions.",
    "foundations": "Define the topic, AI and language model in everyday words before teaching the mechanism.",
    "coverage": "Explicitly cover document preparation, finding passages, supplying evidence, answering, and limitations.",
    "example": "Build a fictional college notice example with source -> question -> retrieved text -> supported answer, plus a missing-answer case.",
    "language": "Use familiar words. Define each technical term on first use. Remove optional jargon.",
    "flow": "Keep the teaching order: foundations, need, mechanism, example, limits, practice, recap.",
    "practice": "Add two understanding questions with explained answers, including an evidence-missing scenario.",
    "structure": "Use every required level-two heading exactly once and in the required order.",
    "readability": "Write 450–1000 prose words; average sentence length <=18 words and no sentence >32 words.",
    "citations": "Cite at least two supplied source IDs in the body as [S1], [S2], etc. Use only supplied IDs and URLs.",
}
ALL_IDS = set(CRITERIA) | {"structure", "readability", "citations"}


def check(id, passed, reason, evidence="", fix=""):
    return {"id": id, "passed": bool(passed), "reason": reason,
            "evidence": evidence, "fix": fix if not passed else ""}


def deterministic(lesson, sources):
    headings = re.findall(r"^## (.+?)\s*$", lesson, re.M)
    # Measure prose only, excluding references, headings and URL tokens.
    body = lesson.split("## Sources", 1)[0]
    prose = re.sub(r"^#+ .*?$", "", body, flags=re.M)
    prose = re.sub(r"https?://\S+|\[S\d+\]", "", prose)
    words = re.findall(r"\b[\w'-]+\b", prose)
    sentences = [re.findall(r"\b[\w'-]+\b", s) for s in re.split(r"[.!?]+(?:\s|$)|\n", prose)]
    lengths = [len(s) for s in sentences if s]
    avg = sum(lengths) / max(1, len(lengths))
    longest = max(lengths, default=0)
    allowed_ids = {s["id"] for s in sources}
    ids = set(re.findall(r"\[(S\d+)\]", lesson))
    body_ids = set(re.findall(r"\[(S\d+)\]", body))
    urls = set(re.findall(r"https?://[^\s)<>]+", lesson))
    allowed_urls = {s["url"] for s in sources}
    cited_urls = {s["url"] for s in sources if s["id"] in body_ids}
    return [
        check("structure", headings == HEADINGS, f"Observed headings: {headings}", fix=HINTS["structure"]),
        check("readability", 450 <= len(words) <= 1000 and avg <= 18 and longest <= 32,
              f"{len(words)} prose words; mean {avg:.1f} words per sentence/line; longest {longest}.", fix=HINTS["readability"]),
        check("citations", len(body_ids) >= 2 and ids <= allowed_ids and urls <= allowed_urls and cited_urls <= urls,
              f"Body source IDs: {sorted(body_ids)}. IDs and URLs must be allowlisted; all cited URLs must be listed.", fix=HINTS["citations"]),
    ]


def validate_judgment(value, lesson):
    """Missing checks, string booleans, made-up quotes and extra IDs fail closed."""
    if not isinstance(value, dict) or set(value) != {"checks"} or not isinstance(value["checks"], list):
        raise ValueError("Evaluator must return exactly a checks array")
    checks = value["checks"]
    if len(checks) != len(CRITERIA):
        raise ValueError("Evaluator returned the wrong number of checks")
    seen = set()
    for c in checks:
        if not isinstance(c, dict) or set(c) != {"id", "passed", "reason", "evidence", "fix"}:
            raise ValueError("Invalid checkpoint shape")
        if c["id"] not in CRITERIA or c["id"] in seen or type(c["passed"]) is not bool:
            raise ValueError("Unknown/duplicate checkpoint or non-boolean verdict")
        seen.add(c["id"])
        if any(not isinstance(c[k], str) for k in ("reason", "evidence", "fix")) or not c["reason"].strip():
            raise ValueError("Checkpoint needs text fields and a reason")
        if c["evidence"] and c["evidence"] not in lesson:
            raise ValueError("Evaluator evidence is not an exact quote from the lesson")
        if c["passed"] and not c["evidence"].strip():
            raise ValueError("Passing semantic checkpoint requires an evidence quote")
        if not c["passed"] and not c["fix"].strip():
            raise ValueError("Failed checkpoint requires an actionable fix")
    return checks

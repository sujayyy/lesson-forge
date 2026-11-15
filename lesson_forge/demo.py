"""Scripted fixtures exercise orchestration, NOT semantic evaluator quality."""
from pathlib import Path
from .rubric import CRITERIA, check

ROOT = Path(__file__).resolve().parent.parent
FALSE_CLAIM = "RAG guarantees that every answer is correct."


def inject_error(lesson):
    # Injection is outside the generator and is not disclosed to the judge.
    return lesson.replace("## Limits\n", "## Limits\n\n" + FALSE_CLAIM + "\n", 1)


class DemoProvider:
    mode = "demo"
    generator_model = "scripted-fixture"
    evaluator_model = "scripted-fixture-not-an-LLM"

    def __init__(self):
        self.usage = []

    def complete(self, role, system, payload):
        if role == "generator":
            return {"lesson": (ROOT / "examples/reference_lesson.md").read_text()}
        lesson = payload["lesson"]
        # This narrow rule is deliberately transparent and only for rehearsal.
        # A passing result here is never labelled SHIPPED by the controller.
        evidence = "RAG helps a language model answer using information found in documents."
        if evidence not in lesson:
            raise ValueError("Offline evaluator supports only the bundled reference fixture")
        return {"checks": [
            check(k, not (k == "accuracy" and FALSE_CLAIM in lesson),
                  "Scripted rehearsal verdict; not a semantic assessment." if k != "accuracy" or FALSE_CLAIM not in lesson else "The injected guarantee contradicts S2 and S3.",
                  FALSE_CLAIM if k == "accuracy" and FALSE_CLAIM in lesson else evidence,
                  "Remove the guarantee; explain that retrieval and generation can both fail.")
            for k in CRITERIA
        ]}

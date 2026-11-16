# Live evaluation evidence

These files are exact copies of observed live API artifacts, without edited verdicts or lesson text. No credentials or local user paths were found during the publication review.

## Generation

- Run: `20261116T070057Z-b2b5b578`, November 16, 2026.
- Provider: Groq; generator and evaluator: `openai/gpt-oss-120b` in separate requests.
- Attempt 1: rejected for unexplained “embeddings”.
- Attempt 2: rejected because the example was not explicitly labelled fictional.
- Attempt 3: all ten checkpoints passed; status `SHIPPED`.
- [Accepted lesson](generation/final_lesson.md), [rejection log and actual diffs](generation/rejection_log.json), [manifest](generation/manifest.json).
- Download/open [report.html](generation/report.html) locally for the readable audit; GitHub shows its source.
- Accepted file SHA-256: `c493f24652adf290f8dfdcdc3e5c7053567741765e942086ba71dde541e64b7d`.

## Evaluator calibration

The complete run `calibration-20261116T065407659883Z` passed all seven probes: reference, false guarantee, false retraining, unsupported example answer, unexplained jargon, missing practice, and instruction attack. See [results and API usage](calibration/calibration.json). A negative probe passes when its intended criterion rejects the defect. This is a small regression smoke test, not statistical evidence of universal accuracy.

## Deliberate-error workflow

Run `20261116T114218Z-678e635c` used live API calls with a false guarantee injected after the first generation. Attempt 1 rejected accuracy and other criteria, explicitly quoting “RAG guarantees that every answer is correct.” Attempt 2 rejected the example criterion. Attempt 3 passed all ten checks and shipped. Exact copies of all 22 run artifacts are in `error-demo/`. The normal submission lesson remains in `generation/`; the demonstration does not replace it or its Google Doc.

These artifacts preserve observed API behavior. They are saved evidence, separate from any recorded walkthrough.

## Limits visible in the accepted artifact

An automated pass is not a human quality certification. The accepted text still contains editorial wording about saying “search the notes” instead of “query an index”, an anthropomorphic “AI’s brain” analogy, and some awkward Markdown emphasis. These are useful examples of remaining judge blind spots. The published lesson is preserved exactly as evaluated; substantive edits require another evaluation. Larger teacher-labelled tests and learner comprehension feedback would be needed before broader deployment.

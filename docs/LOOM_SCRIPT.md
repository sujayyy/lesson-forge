# Loom walkthrough — approximately 18 minutes

Record your own face and screen. This file is a runbook, not a completed video. Do not describe offline fixture verdicts as real model evaluations. For the assessment, complete the live run and calibration first, then record the live workflow with the configured provider. Keep API secrets outside the recording.

## 0:00–1:30 — Problem and learner

Say in your own words: “I built a system that decides whether a beginner lesson can be released. The learner has finished class 12 in India, has limited English, and starts without computing knowledge.”

Show the README and reference lesson. Explain the fictional college-library example, short explanations, and practice questions. State the output contract: accepted lesson plus rejection history; failure after the retry budget means no accepted lesson.

## 1:30–3:30 — Architecture and trade-offs

Show the Mermaid workflow and `pipeline.py`. Walk through source pack → generator → two evaluator layers → gate → retry or release. Explain why plain Python makes the gate inspectable. Show where retries are restricted to 0, 1 or 2. Explain that the fact pack grounds a lesson about RAG; the app does not need a vector database to teach RAG.

## 3:30–6:00 — End-to-end live generation

Run:

```bash
python3 -m lesson_forge run --mode live --topic "Introduction to RAG"
```

While the request runs, show `prompts.py` and explain the learner constraints. Open the printed run directory. Show `manifest.json`, the candidate lesson, the checkpoint rows and final status. If the gate withholds the lesson, show why and keep the failure visible; never edit a verdict manually to manufacture success.

## 6:00–9:30 — Catch a deliberate error

Run:

```bash
python3 -m lesson_forge run --mode live --inject-error first
```

Show the false guarantee in attempt one. Explain that the controller inserts it after generation and the evaluator does not receive the injection flag. In `report.html`, show the failed `accuracy` row, its exact quote and repair. Show the second candidate and the actual diff. Check that it removed the false claim everywhere, rather than adding a correction that leaves contradictory advice.

If the evaluator misses the error, report that honestly and demonstrate the calibration failure. This is evidence of a model/prompt weakness to investigate, not a pass.

## 9:30–11:30 — Inspect the evaluator

Show the ten checks in `rubric.py`. Explain why every subcondition is mandatory and there is no average score. Contrast mechanical citation checks with semantic claim support. Show that `validate_judgment` rejects missing checks, string booleans and fabricated evidence quotes.

Show the saved output from:

```bash
python3 -m lesson_forge.calibrate
```

Explain the seven probes and why a target-specific failure matters. State the measured result you actually observed; do not claim the evaluator is perfectly reliable.

## 11:30–14:00 — Memory across runs

For a fast illustration, explicitly switch to **offline rehearsal**:

```bash
python3 -m lesson_forge run --mode demo --inject-error first --memory data/video-memory.sqlite3
python3 -m lesson_forge run --mode demo --inject-error first --memory data/video-memory.sqlite3
python3 -m lesson_forge run --mode demo --inject-error first --memory data/video-memory.sqlite3
```

Use a fresh database name so earlier rehearsal runs do not change the demonstration. Show the first run's empty policy, the second run's updated `policy_after_run`, and the third run's loaded accuracy instruction. Explain deduplication by run, curated guidance, human feedback and isolation from normal live memory. The rubric never becomes easier.

## 14:00–16:00 — Termination and testing

Run the deliberately impossible rehearsal:

```bash
python3 -m lesson_forge run --mode demo --inject-error always
python3 -m unittest discover -s tests -v
```

Show three rejected candidates, status `WITHHELD` and absence of an accepted lesson file. Explain API errors, one transport retry, timeouts, and why invalid judgments cannot release a lesson.

## 16:00–18:00 — Result and limitations

Open the **live accepted lesson** and its Google Doc. Summarize what a learner should now understand: what RAG means, why evidence helps, the retrieve-and-answer flow, and what to do when evidence is missing. Show the repo structure and setup commands.

Close with candid limits: curated sources require maintenance, model judges can share mistakes, readability is only a proxy, and prompt adaptation needs measured validation. Mention teacher-labelled examples and learner comprehension testing as the next improvements.

## Before submitting

- Face remains visible and speech is audible.
- Total duration is 15–20 minutes.
- A genuine live run and a genuine live error-catching attempt are shown.
- All failures are represented honestly; fixture output is explicitly labelled.
- GitHub, Google Doc and Loom links open for the reviewer.
- No secrets, private browser tabs, or unrelated user documents appear.

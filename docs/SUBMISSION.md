# Submission status

Repository: https://github.com/sujayyy/lesson-forge

For the full sequence, follow [Exact next steps](NEXT_STEPS.md).

## Completed

- Python generate → evaluate → regenerate controller with at most two retries.
- Ten hard pass/fail checkpoints, including an independent API evaluator.
- Fail-closed verdict validation and no release after exhausted retries or API errors.
- Persistent SQLite failure memory, human feedback command and curated prompt evolution.
- Exact candidate drafts, reasons, evidence, payloads, manifests and actual revision diffs.
- Offline deliberate-error repair rehearsal and 24 passing unit tests.
- Live evaluator calibration command with seven probes.
- Beginner RAG reference lesson, architecture notes and an 18-minute Loom runbook.
- Project pushed to `sujayyy/lesson-forge` on the `main` branch.

## Still required for an honest final submission

1. Configure a model provider API key and model names locally. Run the live calibration and review every result.
2. Run the live generation and deliberate-error demonstration. Save the actual accepted lesson and logs. If the evaluator fails a probe, fix and rerun; do not replace evidence with scripted results.
3. Replace the reference draft in the Google Doc with the accepted live lesson and update its status/title.
4. Add reviewed live-run evidence and update the verification status in this repository after those runs succeed.
5. Record the face-visible Loom video using `LOOM_SCRIPT.md`, then check reviewer access to all three links.
6. Submit through the assessment form yourself after reviewing the final materials.

The local reference lesson and offline rehearsal are useful deliverables, but they are not represented as a completed live submission. No final application form has been submitted.

## Lesson document

[Reference lesson draft in Google Docs](https://docs.google.com/document/d/1UIkbHkxC04nLFPPOgIFrPo4tjKOlgTwUEFcvNu61E8s/edit)

The document's status line states that live generation and evaluation are pending. Reviewer sharing access has not been configured.

## Updating the repository

The remote is configured. After reviewing and committing changes, run `git push` from the project directory. Runtime databases and logs are ignored; the included example audit contains only the public reference fixture.

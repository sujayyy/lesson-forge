# Exact remaining steps

The live calibration and ordinary generation are complete. Do not repeat setup or rerun calibration without a reason.

## 1. Use the completed deliberate-error evidence

Verified run `20261116T114218Z-678e635c` caught the false guarantee and shipped attempt 3. No more live requests are needed to establish this result.

```bash
open -a Safari /Users/ivar/Projects/lesson-forge/examples/live-evidence/error-demo/report.html
```

Show accuracy FAIL on attempt 1, example FAIL on attempt 2, then all ten passing checks on attempt 3. Identify it as a saved live run. If its execution is in an earlier recording, retain that footage. If not, the recording still needs actual workflow-execution footage; a saved audit must not be presented as a new live run. Plan a fresh execution only when needed and when the provider quota allows it.

## 2. Inspect the accepted lesson and audit

The exact accepted lesson is in `examples/live-evidence/generation/final_lesson.md`.

```bash
open examples/live-evidence/generation/report.html
```

The saved run rejected attempt 1 for language, attempt 2 for the example, and shipped attempt 3. All ten checks passed. Full calibration passed all seven probes in `examples/live-evidence/calibration/calibration.json`.

The Google Doc link is https://docs.google.com/document/d/1UIkbHkxC04nLFPPOgIFrPo4tjKOlgTwUEFcvNu61E8s/edit. Check that it is titled **Introduction to RAG — Beginner Lesson**, contains the accepted text, and opens for a signed-out viewer. Do not substitute the old reference fixture or edit lesson claims without re-evaluation.

## 3. Prepare your recording

Open Terminal, paste `open -a TextEdit /Users/ivar/Projects/lesson-forge/docs/LOOM_SCRIPT.md`, and press Enter. The guide now starts immediately AFTER the source-facts section already recorded, at approximately minute 5. It contains only the remaining screen actions and narration, using direct file-opening commands and exact search text. Keep the completed footage; do not restart the introduction or source explanation.

- Use screen plus camera and keep your face visible.
- Confirm that your account can record 15–20 minutes before starting. If it cannot, arrange a supported recording option before the final take; do not discover the limit mid-demo.
- Test microphone volume and text readability with a short test recording.
- Close unrelated and API-key tabs; configure the key before recording.
- Open the saved successful report, Google Doc, repository and relevant source files.
- Rehearse explaining the gate, retry bounds, evaluator limitations and memory in your own words.

The continuation briefly shows the current rate-limit error, then explicitly switches to the earlier successful deliberate-error report and the separate ordinary submission report. It does not start another API job. Memory is explained from its implementation; only the offline exhaustion demonstration and local tests are executed. Saved evidence is not presented as new live execution.

## 4. Finish and submit

1. Watch the entire recording. Confirm 15–20 minutes, visible face, clear audio, readable text and genuine error-catching evidence.
2. Obtain the video share link and verify reviewer access in a private browser.
3. Verify the GitHub repository and Google Doc the same way.
4. Submit these links at https://forms.gle/GKMb6wa7HiGFrXvC6:
   - Repository: https://github.com/sujayyy/lesson-forge
   - Lesson: the Google Doc link above.
   - Video: your completed Loom share link.
5. Review the form and submit it yourself. No form submission or recording has been performed for you.

The project and lesson contain no added assistant logos or watermarks. Recorder/player branding depends on your recording account. Keep research citations, model configuration and truthful live/demo labels: they explain the work and its evidence.

# Exact remaining steps

The live calibration and ordinary generation are complete. Do not repeat setup or rerun calibration without a reason.

## 1. Rehearse the deliberate-error workflow

In your configured Terminal:

```bash
cd /Users/ivar/Projects/lesson-forge
python3 groq_run.py error-demo
```

Let the command finish. It can take several minutes because of API pacing. Send the complete output and its saved path for inspection. Attempt 1 must contain the false guarantee and be rejected under accuracy. A later successful repair is useful; honest withholding after the retry limit is also valid evidence of the gate.

If rate limited, follow the provider's retry delay. Do not launch repeated or parallel commands. Never paste a key into the chat or video.

## 2. Inspect the accepted lesson and audit

The exact accepted lesson is in `examples/live-evidence/generation/final_lesson.md`.

```bash
open examples/live-evidence/generation/report.html
```

The saved run rejected attempt 1 for language, attempt 2 for the example, and shipped attempt 3. All ten checks passed. Full calibration passed all seven probes in `examples/live-evidence/calibration/calibration.json`.

The Google Doc link is https://docs.google.com/document/d/1UIkbHkxC04nLFPPOgIFrPo4tjKOlgTwUEFcvNu61E8s/edit. Check that it is titled **Introduction to RAG — Beginner Lesson**, contains the accepted text, and opens for a signed-out viewer. Do not substitute the old reference fixture or edit lesson claims without re-evaluation.

## 3. Prepare your recording

Open Terminal, paste `open -a TextEdit /Users/ivar/Projects/lesson-forge/docs/LOOM_SCRIPT.md`, and press Enter. The rewritten guide has arrow-by-arrow Finder navigation, exact search text, commands, spoken paragraphs, and instructions for each possible live result. No code editor or links are required.

- Use screen plus camera and keep your face visible.
- Confirm that your account can record 15–20 minutes before starting. If it cannot, arrange a supported recording option before the final take; do not discover the limit mid-demo.
- Test microphone volume and text readability with a short test recording.
- Close unrelated and API-key tabs; configure the key before recording.
- Open the saved successful report, Google Doc, repository and relevant source files.
- Rehearse explaining the gate, retry bounds, evaluator limitations and memory in your own words.

The script shows the saved ordinary successful run first, then starts a fresh live injected workflow while you explain the architecture. It explains memory by showing its implementation and explicitly labels the offline exhaustion demonstration. Model outputs can vary; describe the result actually shown.

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

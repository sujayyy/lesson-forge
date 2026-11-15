# Exact next steps

Repository: https://github.com/sujayyy/lesson-forge

The code is published. The remaining work is a real model run, the final lesson document, and your recorded demonstration. Complete the steps below in order. Do not start the final recording until the live rehearsal works.

## 1. Configure the model before recording

You need a model API key with access to the models you select. For an OpenAI account, follow the [official API quickstart](https://developers.openai.com/api/docs/quickstart) to create a key and check project access and billing. API usage may incur charges. Do not paste the key into a document, this repository, a video, or a chat.

Open **Terminal** on your Mac. Paste this first:

```zsh
cd /Users/ivar/Projects/lesson-forge
export LLM_BASE_URL="https://api.openai.com/v1"
export GENERATOR_MODEL="gpt-4.1-mini"
export EVALUATOR_MODEL="gpt-4.1"
```

These are concrete example model names. Both have documented Chat Completions support: [generator model](https://developers.openai.com/api/docs/models/gpt-4.1-mini), [evaluator model](https://developers.openai.com/api/docs/models/gpt-4.1). Availability depends on your account. If your account cannot access them, use supported model IDs from your provider rather than changing the evaluation logic.

Then run this single line in the same **zsh** Terminal:

```zsh
read -s "LLM_API_KEY?Paste your API key, then press Enter: "
```

Paste the key at the prompt and press Enter. Characters will not appear. Now run:

```zsh
export LLM_API_KEY
echo
```

If Python reports a certificate verification error and `certifi` is installed, run `export SSL_CERT_FILE="$(python3 -m certifi)"` in this same Terminal before calibration.

Keep this Terminal window open. The variable belongs to this shell session; a new Terminal or a separately launched editor will not automatically inherit it. Nothing in the app writes the key to a file. Finish credential setup before sharing or recording your screen.

## 2. Rehearse and inspect the live evaluator

In that same Terminal, run:

```zsh
python3 -m unittest discover -s tests -v
python3 -m lesson_forge.calibrate
```

The tests should pass. Calibration makes seven live evaluator calls and prints PASS/FAIL per probe. It saves a `runs/calibration-.../calibration.json` file. Record the exact path. Inspect any FAIL before proceeding. A failed probe is an evaluator weakness or operational failure to resolve; it is not fixed by editing the saved result.

If you see HTTP 401, check the API key. For HTTP 403/404, check account permissions, endpoint and model access. For HTTP 429, check usage limits/quota and retry later. If a rubric check fails, inspect its reason and fix the underlying prompt, sources or evaluator configuration, then rerun the probe set.

## 3. Generate the actual lesson

```zsh
python3 -m lesson_forge run --mode live --topic "Introduction to RAG"
```

The final terminal line prints a run path. Save it. A successful result says **SHIPPED**. In that directory, confirm:

- `final_lesson.md` exists.
- `manifest.json` says `mode: live` and `status: SHIPPED`.
- The accepted attempt has ten passing checkpoints in `rejection_log.json`.
- `report.html` shows the lesson and its audit.

Open Finder → Go → Go to Folder, paste the printed run-directory path, and press Enter. Double-click `report.html` to view the audit in a browser. Open `final_lesson.md` in your text editor.

If it says WITHHELD or ERROR, read the report. Do not use `examples/reference_lesson.md` as a substitute for a live result.

## 4. Rehearse the deliberate-error demonstration

```zsh
python3 -m lesson_forge run --mode live --inject-error first
```

Open this run's `report.html`. Confirm all three things:

1. Attempt one contains “RAG guarantees that every answer is correct.”
2. The real evaluator rejects that claim under `accuracy`, with a reason.
3. A later attempt removes the claim and passes the complete gate, or the run honestly withholds release if retries are exhausted.

Save this run path separately from the normal lesson run. If the evaluator passes the injected claim, the demonstration has exposed a defect: inspect calibration and fix it before recording a successful error-catching demonstration.

## 5. Finalize the lesson document and repository evidence

Open the [lesson draft](https://docs.google.com/document/d/1UIkbHkxC04nLFPPOgIFrPo4tjKOlgTwUEFcvNu61E8s/edit).

1. Copy the accepted live lesson from the normal run's `final_lesson.md` into the document, replacing the reference draft.
2. Change the document title to **Introduction to RAG — Beginner Lesson**.
3. Remove the draft-status sentence only after replacing the text with that accepted live result.
4. Format the title and section headings using Google Docs' built-in styles. Keep the source references and the two practice questions.
5. Read it once, checking that it matches the accepted artifact. If you change substantive lesson wording, it needs another evaluation; do not claim an edited version has the old verdict.
6. Set the sharing permissions so the intended reviewer can read it. If using “Anyone with the link,” choose **Viewer**, not Editor. Open the link in a signed-out/private browser to check access.

Save the normal live run, error-demonstration run, and calibration results in a reviewed `examples/live-evidence/` folder before publishing them. Include the manifests and rejection logs. `runs/` is intentionally excluded from Git; a normal `git add .` will not publish it. Review the copied artifacts for any private input before adding them. Update the README's verification paragraph and `docs/SUBMISSION.md` to describe the actual observed results.

After those updates:

```zsh
git add README.md docs examples/live-evidence
git diff --cached --check
git commit -m "Add live evaluation evidence and final submission links"
git push
```

If you have not created `examples/live-evidence/` yet, complete that copy/review step first. Do not invent a folder path for a run; use the exact paths printed by your commands.

## 6. Prepare the recording workspace

Open these items before starting:

1. **Browser:** the GitHub README, the final Google Doc, and the rehearsal audit reports.
2. **Editor:** the project folder, with `pipeline.py`, `rubric.py`, `prompts.py`, `memory.py`, and `sources/rag.json` ready.
3. **Terminal:** the same shell with the API environment configured, in the project directory.
4. **Finder:** the project's `runs` folder, so you can quickly open the report from each new recording-time run.

Close unrelated applications and tabs, enable Do Not Disturb, and enlarge Terminal/editor text until it is easy to read. Keep a short outline on paper or another screen. Do not record API credential pages or shell commands that print environment variables.

In Loom, choose **screen and camera**, select your microphone and webcam, and capture the screen containing the browser, editor and Terminal. Keep your face visible in a corner that does not cover the terminal result or checkpoint table. Record a 20-second test; play it back to check audio, readable text and camera placement.

**Check the duration limit first.** Loom's [published plan details](https://www.loom.com/pricing) list five-minute recordings for Starter and unlimited recording time for Business. The assessment needs one 15–20 minute demonstration. Use an account/plan or available trial that supports that duration; do not assume the free plan can record it. Review any price or renewal terms yourself.

## 7. Record the 18-minute walkthrough

Follow [the detailed script](LOOM_SCRIPT.md). This is the screen-action checklist:

| Time | What you do on screen | What you explain |
|---|---|---|
| 0:00–1:30 | Show README and final lesson | Learner, problem, and release contract |
| 1:30–3:30 | Show diagram, source pack, controller | Why this architecture, where the gate and retry limit live |
| 3:30–6:00 | Run normal **live** generation; open its new report | Generation, actual verdicts, final artifact |
| 6:00–9:30 | Run **live** error injection; open that new report | False claim, rejection reason, feedback, actual correction |
| 9:30–11:30 | Show rubric and saved live calibration JSON | Ten binary checks and evaluator limitations |
| 11:30–14:00 | Run the three labelled offline memory rehearsals | Persistent observations activate guidance on run three |
| 14:00–16:00 | Run labelled offline exhaustion test and unit tests | Three failures terminate; no accepted lesson is released |
| 16:00–18:00 | Show final Doc and repo | What was delivered, actual evidence, remaining limitations |

Run the two main live commands during recording so the reviewer sees the workflow operating. Use the saved calibration results for the calibration section. If requests take longer, explain the relevant code while waiting and keep the final cut within 15–20 minutes. If you remove an idle wait, make the edit clear; preserve the actual results.

Do not read code line by line. For each part, explain its purpose, show where it happens, and show the resulting evidence. Practice until you can answer: Why separate the judge? Why not a weighted score? How does memory avoid weakening standards? What happens when every attempt fails?

## 8. Keep presentation and branding clean

The project adds no assistant logos, watermarks, co-author footer, or tool attribution. Technical provider names, research citations, and accurate live/demo labels are part of the project evidence.

Loom controls its own player/page branding. Its [plan page](https://www.loom.com/pricing) lists branding removal for Business. If you want that removed too, use an eligible plan and its branding controls, then inspect the shared viewer. Do this yourself; no account upgrade or payment is part of this project setup. The exact control can depend on your workspace. Do not crop out the required face camera or evaluation evidence to hide a recorder overlay.

Write your own short title and video description. No generated title, summary or decorative intro is needed. Suggested title: **Lesson Forge — Self-Evaluating RAG Lesson Generator**.

## 9. Check and submit the three links

1. Play the video from beginning to end. Confirm duration, face visibility, sound, readable text and both live workflows.
2. Set video access for the reviewer and open its share link in a private browser.
3. Check repository access and final Google Doc access the same way.
4. Put the repository URL, final Google Doc URL and Loom URL into the [assessment form](https://forms.gle/GKMb6wa7HiGFrXvC6).
5. Review your details and all three links, then submit the form yourself.

After recording, you can clear the API key from the Terminal session with `unset LLM_API_KEY` and close the shell.

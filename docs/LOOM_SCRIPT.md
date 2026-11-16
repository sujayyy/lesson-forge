# Loom walkthrough — 18-minute action plan and script

This is a recording guide, not a completed video. Record your own face and screen. Practice the explanations until you can describe the code and respond to follow-up questions. Use the actual results on screen; future model runs can differ from the saved run.

## Before you press Record

1. Rehearse `python3 groq_run.py error-demo` once and inspect its report. Attempt 1 must contain the injected false guarantee and the accuracy check must reject it. If requests hit a limit, wait for the stated cooldown before recording.
2. Confirm your recording account permits a 15–20 minute video. Select screen plus camera, test the microphone, and keep the face bubble away from terminal text. Make a short sound check first.
3. Open only the project Terminal, code editor, GitHub repo, accepted Google Doc and saved audit. Close API-key pages and unrelated tabs. Configure the key before recording; do not display environment variables.
4. In Terminal run `cd /Users/ivar/Projects/lesson-forge`. Increase the font until it is readable in a test recording.
5. Open the saved successful report with `open examples/live-evidence/generation/report.html`. Open README.md, lesson_forge/pipeline.py, rubric.py, prompts.py and memory.py in your editor.
6. Use a fresh database filename for the memory section on every recording take. Never delete your normal memory database to stage a demonstration.

The timing below fits one live injected workflow, which demonstrates generation, evaluation, repair and error catching together. Show the earlier ordinary successful run as saved evidence and explicitly identify it that way. Do not run two live jobs in parallel. Each API call is spaced by 65 seconds; use the waits to explain design. If the live call takes longer, shorten code discussion or clearly trim idle waiting, preserving all verdicts.

## 0:00–2:00 — Show the result and explain the learner

**On screen:** README, accepted Google Doc, then saved generation report.

**Say:** “This is Lesson Forge, a self-evaluating lesson generator. The learner has completed class 12 in India, has limited English, and starts without computing knowledge. The topic here is Introduction to RAG. The system must teach what it is, why it helps, and how it works.”

“The output includes the lesson and its rejection history. Here is a saved live run from November 16. The first draft failed language because it introduced embeddings. The second failed because the example was not explicitly labelled fictional. The third passed all ten checks and was released. The revision diff records what actually changed.”

**Do:** Expand each of the three attempts in the saved report. Point at the failed criterion, reason and correction. Do not claim this saved run is happening live.

## 2:00–3:00 — Start the live deliberate-error workflow

**Run:**

```bash
python3 groq_run.py error-demo
```

**Say:** “I am starting a new live run. For this demonstration, the controller adds the false sentence ‘RAG guarantees that every answer is correct’ to the first draft after generation. The evaluator is not told that an error was inserted. It must find the problem from the lesson and source facts.”

“The provider has a free-tier rate limit, so calls are paced. While it runs, I will explain the workflow.”

## 3:00–7:00 — Explain architecture while the command runs

**On screen:** README diagram, sources/rag.json, pipeline.py, prompts.py. Briefly return to Terminal when an event appears.

**Say:** “I chose plain Python and an explicit controller because the retry and release rules are easy to inspect. The source pack contains reviewed facts and source IDs. This system generates a lesson about RAG; it does not pretend to be a vector retrieval service.”

“The generator writes a draft. Code checks headings, a readability proxy, and citation syntax. A separate model request checks meaning: accuracy, foundations, coverage, example, language, flow, and practice. Every checkpoint must pass. There is no average score that lets strong formatting hide an inaccurate claim.”

“On a valid rejection, the next generator request receives the previous draft and specific failed checks. The evaluator sees the new candidate independently. There are at most two regenerations, so three candidate lessons total. Invalid model responses or provider errors cannot release a lesson.”

**Do:** Point to the loop bound, feedback payload, validate_judgment call, and SHIPPED transition in pipeline.py. Show one source fact and its URL. Explain one trade-off: a curated fact pack is reviewable and cheap, but needs maintenance and does not cover every topic automatically.

## 7:00–9:00 — Inspect the new live result

**Do:** Use the NEW path printed in Terminal. In Finder press Command+Shift+G, paste that directory, and open report.html. Inspect attempt 1, then the repair and actual diff.

**Say, only when observed:** “The accuracy check rejected the false guarantee. Here is the exact evidence line, the reason, and the suggested repair. This later draft removed the claim. The final status is [read the actual status].”

If it is WITHHELD: “The error was caught, but the remaining drafts did not clear every check within the budget. Withholding is the specified behavior. The ordinary saved run shown earlier demonstrates a successful release.”

If it is ERROR: show the actual error; do not present it as a successful error-catching result. Resolve it before the final take. If the judge passes the false guarantee, treat that as a failed test, not a successful demonstration.

## 9:00–11:00 — Explain how the evaluator is checked

**On screen:** rubric.py, schemas.py, saved examples/live-evidence/calibration/calibration.json.

**Say:** “The complete calibration run passed seven probes: one valid reference and six deliberate defects. Each negative probe must fail its intended criterion. For example, rejecting a jargon mutation only for structure would not count as catching the language issue.”

“Provider formatting was a practical failure mode. The evaluator now selects short line IDs; code maps them to exact candidate text. It rejects unknown IDs, missing checks, duplicate criteria, non-boolean verdicts, and passes with no evidence. Both the provider response and resolved quotes are retained. Correct JSON still does not prove the judgment is right.”

“These are small regression tests that informed development, not an untouched holdout set or proof of perfect accuracy.”

**Do:** Show the seven passed_probe values and one negative check's reason. Do not rerun all seven during recording.

## 11:00–14:00 — Demonstrate memory across runs

**Say before running:** “This section uses labelled offline fixtures so persistence can be demonstrated quickly. These fixture verdicts are not live model judgments.”

Choose a fresh filename for this take and use the SAME filename in all three commands:

```bash
python3 -m lesson_forge run --mode demo --inject-error first --memory data/video-take1.sqlite3
python3 -m lesson_forge run --mode demo --inject-error first --memory data/video-take1.sqlite3
python3 -m lesson_forge run --mode demo --inject-error first --memory data/video-take1.sqlite3
```

**Do:** Open the three printed manifests. Show the first run's empty policy, second run's policy_after_run accuracy hint, and third run's loaded hint.

**Say:** “Two distinct runs with the same failure activate a curated prompt instruction. Repeated retries within one run count only once. The guidance is frozen during a run. Scope includes topic, source content, rubric, live or demo mode, and injected versus normal runs. This keeps synthetic failures separate from ordinary live learning.”

“Human feedback can record the same kinds of observations. Raw notes are stored but are not executed as instructions. This changes prompt guidance, not the rubric. It demonstrates adaptation; improvement would need a separate measured experiment.”

## 14:00–16:00 — Show termination and tests

**Run:**

```bash
python3 -m lesson_forge run --mode demo --inject-error always
python3 -m unittest discover -s tests -v
```

**Say:** “This offline fixture inserts the error every time. Three failed candidates exhaust the budget and produce WITHHELD, with no accepted lesson file. The test suite checks release, repair, withholding, malformed verdicts, memory isolation, provider failures, and exact evidence resolution.”

**Do:** Show the withheld result and lack of final_lesson.md. State the actual test count shown (currently 39), without claiming mocked tests are live API tests.

## 16:00–18:00 — Deliverables and limitations

**On screen:** accepted Google Doc, GitHub live-evidence folder, architecture notes.

**Say:** “The repository contains setup instructions, the workflow, tests and exact live evidence. The Google Doc contains the accepted lesson. The core result is the autonomous decision loop, including its rejection history.”

“The evaluator still has blind spots. The accepted lesson includes an unnecessary phrase about ‘query an index’ and an ‘AI’s brain’ analogy. I preserved the evaluated output rather than silently editing it after the verdict. A production version needs more teacher-labelled examples and comprehension tests with the intended learners.”

“Separate requests reduce direct self-justification, but both roles currently use the same model and can share mistakes. Readability is only a proxy. Source maintenance and rate limits are also operational responsibilities.”

**Do:** Show the actual source links and practice questions. Stop between 15 and 20 minutes.

## After recording

Watch the entire video. Check face visibility, audio, readable text, duration, and that the new injected error was genuinely caught. Set video access for reviewers. Open the repo, document and video in a private browser. Submit those three links through the assessment form yourself. If trimming idle waits, keep the actual decisions and explain the cut. No generated intro or title is necessary.

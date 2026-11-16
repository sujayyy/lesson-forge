# Continue your recording here — after the source-facts section

You have already recorded the introduction, lesson, live-command start, diagram and source facts. Keep that footage. Do not repeat those sections or start another API call for this continuation.

Start below at approximately minute 5 of your existing video. Times are approximate; screen navigation and speaking speed vary. The finished video must be 15–20 minutes. Read only the SAY paragraphs aloud, not these instructions.

The current recorded attempt hit a provider rate limit. We will show that error briefly, then explicitly switch to the verified earlier successful live run. We will not describe the earlier report as the result of the interrupted attempt.

## Before you resume — prepare one spare Terminal window

If the recording is paused, keep it paused for this preparation.

Command + Space → type Terminal → Enter → menu bar at the top of your Mac → Shell → New Window.

Use this NEW window for the file-opening commands below. Keep the original window with the rate-limit error available. Do not close either window.

To use a command: click after the `%` prompt → paste the whole command → press Enter. Do not paste the `%` itself. Commands beginning with `open` only open local files; they do not call Groq.

If TextEdit asks whether to save changes to a code file, choose Don't Save. You are displaying code, not editing it.

Resume the recording → begin section 1.

## 1. About 05:00–06:30 — Show how retries and release work

CLICK → spare Terminal window → paste this → Enter:

```bash
open -a TextEdit /Users/ivar/Projects/lesson-forge/lesson_forge/pipeline.py
```

TextEdit opens the controller code. Do these four searches in order. For each: Command + F → type the exact search text → Enter → Escape. Move your mouse over the matching line. Do not change it.

SEARCH → `for index in range`

SAY:

“This is the controller. This loop limits the number of candidate lessons. With two retries configured, there is one initial draft and at most two repaired drafts. That keeps the process bounded instead of letting the model keep trying indefinitely.”

SEARCH → `previous_lesson`

SHOW → The same area includes `failed_checks`.

SAY:

“The next generator request receives the previous lesson and the specific failed checks. This gives it concrete repair instructions. It must repair the whole lesson, because fixing one section can introduce a problem elsewhere.”

SEARCH → `validate_judgment(raw, lesson)`

SAY:

“The evaluator response is validated before its judgments are used. The controller combines those semantic results with the mechanical checks. Missing or malformed judgments cause an error; they are not assumed to pass.”

SEARCH → `SHIPPED`

SAY:

“This line marks a successful live release. The controller reaches it only when there are no failed checks. If every allowed draft fails, the result is withheld. If an API call fails, the result is an error. Both outcomes prevent publication.”

## 2. About 06:30–07:15 — Show the two model instructions

CLICK → spare Terminal window → paste → Enter:

```bash
open -a TextEdit /Users/ivar/Projects/lesson-forge/lesson_forge/prompts.py
```

SHOW → The top of the file describes the Indian class-12 learner. Move your mouse over that sentence.

SAY:

“The generator instructions specify the learner, simple language, the required lesson structure, a fictional example and explained practice questions.”

CLICK → Command + F → type `independent, strict educational quality reviewer` → Enter → Escape.

SAY:

“The evaluator has a separate reviewing role. It receives the candidate, facts and rubric, but not the generator’s conversation or the deliberate-error flag. It judges the whole lesson from scratch. Both roles use the same model in separate calls, so they can still share blind spots.”

## 3. About 07:15–07:45 — Explain the interrupted live attempt

CLICK → Terminal → menu bar → Window → select the ORIGINAL window showing the error-demo output, not the spare file-opening window.

SHOW → Leave the lines containing `REJECT` and `Provider HTTP 429` visible. Do not run the command again.

SAY:

“This attempt rejected the first draft, including the accuracy check, but the provider’s rate limit stopped the second evaluation. No lesson was released from this attempt. I will now show an earlier completed live run of the same deliberate-error workflow.”

Do not say that the current attempt shipped. The next report comes from a different, earlier run.

## 4. About 07:45–09:45 — Show the earlier successful deliberate-error run

CLICK → spare Terminal window → paste → Enter:

```bash
open -a Safari /Users/ivar/Projects/lesson-forge/examples/live-evidence/error-demo/report.html
```

Safari opens the correct report directly. You do not need Finder or to copy a run-directory path.

SHOW → At the top, point to `SHIPPED` and the run identifier `20261116T114218Z-678e635c`.

SAY:

“This is the saved earlier live run. It used actual model API calls. It is not the interrupted attempt I just showed.”

CLICK → scroll down to `Attempt 1 · REJECT`. If the rows are hidden, click that heading once. Find the row whose first column says `accuracy`.

SHOW → Point to FAIL, then the evidence sentence “RAG guarantees that every answer is correct”, then its repair instruction.

SAY:

“The controller inserted this false guarantee after generation. The evaluator was not told which sentence had been inserted. It rejected the claim because the source facts say RAG can still be wrong. The report saves the verdict, the reason, the exact evidence and the requested repair.”

CLICK → scroll down to `Attempt 2 · REJECT` → locate the `example` row → point to its reason.

SAY:

“The next draft still failed the example requirement. Even after the accuracy problem was addressed, the system did not release a draft with another failed checkpoint. It requested another repair.”

CLICK → scroll down to `Attempt 3 · PASS` → slowly move through the ten check rows.

SAY:

“The third candidate passed all ten checks and was released. This shows that acceptance is based on the complete set of checks, not just removal of the deliberately inserted error.”

CLICK → below that table, find `Actual changes from previous attempt`.

SHOW → Point to one line starting with `-`, then one starting with `+`.

SAY:

“These are the actual changes between drafts. A minus sign marks removed text and a plus sign marks added text. The audit records what changed rather than relying on the generator to describe its own repair.”

## 5. About 09:45–10:30 — Briefly show the ordinary submission run

CLICK → spare Terminal window → paste → Enter:

```bash
open -a Safari /Users/ivar/Projects/lesson-forge/examples/live-evidence/generation/report.html
```

SHOW → The top says SHIPPED. The run identifier is `20261116T070057Z-b2b5b578`. This is a different report from section 4.

SAY:

“This separate ordinary live run produced the submission lesson without a deliberately injected error. Its first draft failed language, its second failed the example requirement, and its third passed. The Google Doc contains the accepted lesson from this ordinary run.”

CLICK → scroll to `Attempt 3 · PASS` → point to the passing rows.

Do not spend time reading the entire lesson here; you already showed it earlier.

## 6. About 10:30–11:30 — Show the pass-or-fail rubric

CLICK → spare Terminal window → paste → Enter:

```bash
open -a TextEdit /Users/ivar/Projects/lesson-forge/lesson_forge/rubric.py
```

CLICK → Command + F → type `CRITERIA =` → Enter → Escape.

SHOW → Move your mouse down the criterion names: accuracy, foundations, coverage, example, language, flow and practice. Do not read every long definition aloud.

SAY:

“These seven semantic checks assess whether the lesson is correct, starts from zero, covers the topic, teaches with a valid example, uses accessible language, follows a coherent order and includes useful practice.

“Three code checks also examine the required headings, a readability proxy and citation syntax. Each checkpoint passes or fails. There is no weighted average that allows strong formatting to compensate for an inaccurate claim. Citation syntax is checked separately from whether the source actually supports the claim.”

## 7. About 11:30–12:15 — Show evidence handling

CLICK → spare Terminal window → paste → Enter:

```bash
open -a TextEdit /Users/ivar/Projects/lesson-forge/lesson_forge/schemas.py
```

CLICK → Command + F → type `def resolve_evidence` → Enter → Escape.

SHOW → Point to the line containing `evidence_id`, then the line containing `Unknown evaluator evidence ID`.

SAY:

“The evaluator selects a short line ID. Code maps it back to exact text from the candidate lesson. It does not guess or rewrite the evidence. Unknown IDs are rejected, and the other validator checks completeness, boolean verdicts and evidence for passes.

“This handles the response format. A well-formed response can still contain a mistaken judgment, so the evaluator also needs testing.”

## 8. About 12:15–13:45 — Show the seven completed calibration probes

CLICK → spare Terminal window → paste → Enter:

```bash
open -a TextEdit /Users/ivar/Projects/lesson-forge/examples/live-evidence/calibration/calibration.json
```

CLICK → Command + F → type `"passed_probe"` → Enter. Keep the search box open. Press Command + G to move through the next matches. There are seven. Pause briefly at each `true`, then press Escape.

SAY:

“This saved calibration run passed all seven probes. One is a valid reference lesson. The other six contain controlled defects: a false guarantee, false retraining, a wrong example answer, unexplained jargon, missing practice and an instruction trying to make the evaluator pass incorrect content.

“For a negative probe, passing means that the evaluator rejected the intended defect. It does not mean the damaged lesson passed. A rejection for an unrelated reason would not count as success for that probe.”

CLICK → Command + F → type `which directly contradicts source facts` → Enter → Escape.

SHOW → Point to that rejection reason.

SAY:

“This explanation identifies the false guarantee as contradicting the sources. These are small regression tests. They informed development, so they are not an untouched holdout set, and seven examples do not prove general reliability.”

Do not rerun calibration. Opening this file makes no API requests.

## 9. About 13:45–15:15 — Explain memory across runs

CLICK → spare Terminal window → paste → Enter:

```bash
open -a TextEdit /Users/ivar/Projects/lesson-forge/lesson_forge/memory.py
```

CLICK → Command + F → type `COUNT(DISTINCT run_id)` → Enter → Escape.

SHOW → Point to `>=2` on that line and `HINTS` on the next line.

SAY:

“Failure observations are stored in SQLite, so they survive separate program runs. This query counts distinct runs. When the same checkpoint fails in two different runs, a reviewed instruction for that checkpoint becomes active in future prompts.

“Retries inside one run count only once. Guidance is loaded at the beginning of a run and remains fixed during it. Human feedback can record the same kinds of observations. The system uses curated instructions instead of letting arbitrary feedback rewrite the rubric.

“This is prompt adaptation, not training the model’s weights. It demonstrates a learning mechanism, but any improvement in quality would need to be measured.”

CLICK → spare Terminal window → paste → Enter:

```bash
open -a TextEdit /Users/ivar/Projects/lesson-forge/lesson_forge/pipeline.py
```

CLICK → Command + F → type `scope = digest` → Enter → Escape.

SAY:

“Memory is scoped by topic, sources, rubric, execution mode and whether errors were injected. That keeps demonstration failures separate from ordinary live guidance. Here I am explaining the implementation, not presenting a new live memory experiment.”

## 10. About 15:15–16:15 — Demonstrate the stopping rule offline

CLICK → spare Terminal window → paste the following two lines → Enter:

```bash
cd /Users/ivar/Projects/lesson-forge
python3 -m lesson_forge run --mode demo --inject-error always
```

SHOW → Wait for the prompt to return. Point to the three rejections and the final WITHHELD line. This uses local fixtures and makes no Groq calls.

SAY:

“This is an explicitly labelled offline fixture demonstration. It is not a live model evaluation. The known error is inserted on every attempt, so all three candidates are rejected. The controller stops and withholds the lesson.

“This checks the stopping behavior. The system does not keep spending indefinitely or publish a failing draft just because it has used its retry budget.”

## 11. About 16:15–17:00 — Show the unit-test result

CLICK → same Terminal window after the prompt returns → paste → Enter:

```bash
python3 -m unittest discover -s tests -v
```

SHOW → Wait for completion → point to the final test count and OK. The current count is 39; say the count actually displayed.

SAY if the tests pass:

“The local tests pass. They cover successful release, repairs, exhausted retries, malformed responses, persistent memory, provider failures and evidence mapping. Mocked provider tests verify application behavior; they are separate from the actual live evaluation results shown earlier.”

If any test fails, do not describe it as passing. Keep the result visible and resolve it before final submission.

## 12. About 17:00–18:30 — Close with the lesson and limitations

CLICK → Safari → click the existing tab titled `Introduction to RAG — Beginner Lesson`.

If the tab is closed: open Google Drive as you normally do → search for `Introduction to RAG` → double-click `Introduction to RAG — Beginner Lesson`.

SHOW → Scroll to `How it works`, then the practice questions.

SAY:

“The repository contains the workflow, setup instructions, tests and exact live evidence. This document contains the accepted lesson. The key result is the autonomous decision loop and its auditable rejection history.”

SHOW → In `How it works`, point to the sentence containing `query an index`.

SAY:

“An automated pass is not a guarantee of excellent teaching. The accepted lesson still includes this unnecessary phrase about querying an index and an AI-brain analogy elsewhere. These are examples of evaluator blind spots. The evaluated wording was preserved rather than silently edited after acceptance.

“The next improvements would be a larger teacher-labelled evaluation set and comprehension tests with the intended learners. Both model roles currently use the same model, so separate requests do not remove shared mistakes. The source facts need maintenance, and rate limits must be handled operationally.

“The workflow can generate, reject, explain, repair and release after its configured checks pass. It also stops when the checks or provider calls do not succeed. Thank you.”

CLICK → Check the recording timer → finish between 15 and 20 minutes → click Stop in the recording controls → let the upload finish.

If the video is too short in a rehearsal, spend more time explaining the actual evidence in the final take. Do not fill time with a blank wait or unsupported claims. If it is approaching 20 minutes, shorten the closing discussion.

## After recording — do not read this aloud

Keep the earlier footage you already recorded, including the real execution and its rate-limit result. Label the successful earlier reports as saved evidence, exactly as this script does. Do not cut an old successful result into the interrupted run as if they were one run.

The assessment asks to see the workflow running end-to-end. A saved report proves the observed outcome but does not show execution. If you have execution footage from the earlier successful run, include it with a clear transition; if you do not, consider whether an additional recorded execution is needed before submission. Do not claim that the interrupted run completed.

Watch the whole final video → confirm visible face, clear sound, readable text and 15–20 minute length → check that the reviewer can access the repository, lesson and video → submit those three items through the original assessment form yourself.

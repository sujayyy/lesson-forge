# Recording guide — exactly what to click, show and say

Use this guide instead of the previous script. There are no links to follow. Read the SAY paragraphs aloud in your own natural voice. Do not read the CLICK instructions aloud.

Target: 18–19 minutes, including screen navigation. The times are guides, not deadlines. Practice once without recording. Do not rush to match a timestamp. Do not invent extra claims to fill time.

## Understand these four actions first

**Open Terminal:** press Command + Space → type Terminal → press Enter.

**Run a command:** click after the `%` prompt in Terminal → paste the command → press Enter. Do not paste the `%` symbol. If a Python command is still running, wait; do not paste another command into it.

**Find text:** click inside the open document/page → press Command + F → type the exact words shown in this guide → press Enter if needed → press Escape to close the search box. Leave the matching words visible.

**Point:** move your mouse over the relevant words and keep it there for a few seconds. You do not need to click, select, edit or explain every line of code.

For this video you need Terminal, your browser and TextEdit. You do not need VS Code. TextEdit is only being used to display files. Do not type into or change the project files.

# PART A — PREPARE BEFORE RECORDING

## A1. Put this guide on your phone or beside your laptop

On the Mac: open Terminal → paste the following → press Enter:

```bash
open -a TextEdit /Users/ivar/Projects/lesson-forge/docs/LOOM_SCRIPT.md
```

Read it once. Keep a second copy on your phone, or use printed notes. This guide is for you; the project screens are what the reviewer should see.

## A2. Open the project folder

Click Finder in the Dock → press Command + Shift + G → paste this folder path → press Enter:

```text
/Users/ivar/Projects/lesson-forge
```

You should see files including README.md and groq_run.py, and folders including lesson_forge, examples and docs.

Keep this Finder window open. Whenever this guide says “project folder”, it means this window.

## A3. Open the successful report

Project folder → double-click examples → double-click live-evidence → double-click generation → double-click report.html.

A browser page opens with the heading “A lesson must earn its release.” At the top it should say SHIPPED. This is the SAVED SUCCESSFUL REPORT.

Scroll down → find “Attempt 1 · REJECT” → find “Attempt 2 · REJECT” → find “Attempt 3 · PASS”. If an attempt is collapsed, click its heading once to expand it. Then scroll back to the top.

Do not open the report.html file from a different folder by mistake.

## A4. Open the final lesson

In your browser, click the existing tab titled “Introduction to RAG — Beginner Lesson”.

If that tab is closed: open your Google Drive → click the search box at the top → type Introduction to RAG → press Enter → double-click “Introduction to RAG — Beginner Lesson”.

The document should start with “Introduction to Retrieval-Augmented Generation (RAG)” and “Start here”. Keep it open. This is the FINAL LESSON screen.

## A5. Open the GitHub project

In your browser, click the existing tab whose title includes “sujayyy/lesson-forge”.

If it shows an individual file: click the repository name “lesson-forge” near the top to return to the repository home.

If there is no existing tab: open GitHub as you normally do → sign in if necessary → click your profile picture at the top right → click “Your repositories” → click “lesson-forge”.

Click “Code” if you are on another repository tab. Scroll below the file list until you see the README heading “Lesson Forge”. This is the PROJECT screen.

Scroll farther down → find the heading “Quality gate” → below the table is the diagram with boxes and arrows. Check that you can find it, then scroll back to the README heading.

## A6. Prepare Terminal before the recording

Open Terminal → paste:

```bash
cd /Users/ivar/Projects/lesson-forge
```

Press Enter. Keep this same Terminal window open. Use the window where your Groq key is already configured. If the launcher asks for a key during a rehearsal, finish credential setup before the final recording; never show or paste the key while recording.

Increase the Terminal text size if necessary: menu bar → View → Bigger. Repeat until you can read it comfortably.

Do not start the recording during an active Groq cooldown. A new recording cannot bypass an exhausted allowance. Also confirm your recorder permits a 15–20 minute video before starting.

## A7. Set up Loom

Open the Loom desktop app → choose screen recording → choose the entire screen/full-screen capture → turn the camera ON → select your microphone → check that you can see your face and that the microphone responds when you talk.

Use the whole screen because you will switch between browser, Terminal and TextEdit. Recording only a browser tab would miss the Terminal demonstration. Recorder labels can vary; choose the equivalent controls rather than searching for an exact label that is not present.

Move the camera bubble to an unused corner → close unrelated tabs, especially API-key pages → make a 20-second test recording → play it back → confirm your face, voice and Terminal text are clear.

Return to the PROJECT screen. When ready, click Loom's Start recording button. Wait for the countdown. Begin Part B.

# PART B — THE RECORDING

## 00:00–01:00 — Introduce the project

CLICK → Browser → PROJECT tab → scroll so “Lesson Forge” and the introductory text are visible.

SHOW → Keep the mouse near the first paragraph. Do not scroll while saying the first sentence.

SAY:

“Hello, I’m Sujay. This project is Lesson Forge, a self-evaluating lesson content generator. It is designed for a learner who has completed class twelve in India, has limited English vocabulary, and is starting with no computing background.

“The submission topic is Introduction to RAG. The system does more than write a lesson. It generates a draft, evaluates it against hard pass-or-fail requirements, and uses the failures to repair the draft. It releases the lesson only when every check passes. Otherwise, it stops after the allowed attempts and keeps an audit of what happened.”

## 01:00–02:00 — Show what the learner receives

CLICK → Browser → FINAL LESSON tab.

SHOW → Start at the title → scroll slowly to “A worked example” → stop at the Lotus College library notice → scroll to “Try it yourself”.

SAY while showing the opening:

“This is the accepted lesson from an actual live run. It explains the idea, why it helps, how it works, and its limits.”

SAY at the library example:

“The example uses a fictional college library notice. One question can be answered from the notice: when the library closes. Another cannot: the library’s phone number. That lets the lesson teach both using evidence and recognizing missing information.”

SAY at the practice questions:

“The learner also gets two questions with answers. These test understanding of the process and what to do when the notes do not contain an answer. The document preserves the wording that the system evaluated.”

## 02:00–02:45 — Start the live demonstration

CLICK → Open Terminal using Command + Space → type Terminal → Enter.

RUN this ONE command:

```bash
python3 groq_run.py error-demo
```

SHOW → Wait until the Terminal displays “GENERATE attempt 1/3” or an error. Do not run another live command.

SAY:

“I am starting a new live demonstration. The controller will deliberately add the false claim ‘RAG guarantees that every answer is correct’ to the first draft. The evaluator is not told where the error was inserted. It must detect the contradiction using the source facts.

“Calls are spaced to respect the provider’s free-tier limits. While this runs, I will explain the architecture.”

IF a key prompt appears → pause recording → finish the key entry privately → resume only after the prompt is gone. Never read the key aloud.

IF an immediate provider error appears → use the error instructions at the end of this guide. Do not claim the workflow completed.

## 02:45–04:00 — Show the workflow diagram

CLICK → Browser → PROJECT tab → scroll down to “Quality gate” → move past the table to the diagram.

SHOW → Move the mouse along these boxes in this order: Generate candidate → Mechanical checks + independent semantic evaluator → All ten checks pass? → Release final lesson. Then move to the “No” path and retry decision.

SAY:

“This is the complete decision loop. First, the system loads the topic, reviewed sources and any persistent guidance. The generator produces a candidate lesson. There are then two evaluation layers: code for measurable requirements, and a separate model call for meaning and teaching quality.

“The controller combines those results. One failed checkpoint is enough to reject the draft. If there are attempts left, the failures go back into generation. If everything passes, the lesson is released. If the retry budget is exhausted, it is withheld.

“I used plain Python because the state transitions and release condition are easy to inspect. The assessment allows Python plus an API, and this workflow does not need a larger orchestration framework to make these decisions.”

## 04:00–05:00 — Open and explain the source facts

CLICK → Finder → project folder. If Finder is still inside generation: press Command + Shift + G → paste `/Users/ivar/Projects/lesson-forge` → Enter.

CLICK → double-click sources → single-click rag.json → press Space.

SHOW → A Quick Look preview opens. Scroll inside it until the AWS URL and the list labelled “facts” are visible. Move the mouse over the URL, then the first fact. If Quick Look cannot preview the file, close it with Space and use the fallback below in a SECOND Terminal window.

SAY:

“This file contains the factual reference material. Each source has an identifier, a URL and reviewed factual notes. The evaluator checks the lesson’s technical claims against these facts. The generator also receives beginner-oriented versions of the facts to reduce unnecessary jargon.

“The trade-off is that this is inexpensive and reviewable, but the facts need maintenance. A new topic needs its own reviewed source pack. This is a system for generating a lesson about RAG; it is not claiming to implement a vector-search service itself.”

FALLBACK ONLY: Terminal menu → Shell → New Window → paste and run:

```bash
open -a TextEdit /Users/ivar/Projects/lesson-forge/sources/rag.json
```

Keep the original Terminal window running the live job. Never type this command into that busy window.

## 05:00–06:30 — Open the controller and point to four exact places

CLICK → Close Quick Look with Space if it is open → Finder → Command + Shift + G → paste `/Users/ivar/Projects/lesson-forge/lesson_forge` → Enter.

CLICK → right-click pipeline.py → Open With → TextEdit. If TextEdit is not listed: Open With → Other → choose TextEdit → Open. Leave “Always Open With” unchecked.

SHOW/SAY in this exact order. All searches are inside TextEdit:

1. Command + F → type `for index in range` → Enter → Escape. Move your mouse over that line.

SAY: “This line controls the candidate loop. With the configured two retries, there can be one original draft and two repairs: three candidates in total.”

2. Command + F → type `previous_lesson` → Enter → Escape. The same area includes `failed_checks`.

SAY: “These fields send the previous lesson and the failed checkpoints into the next generation request. The generator receives specific repair instructions rather than a vague request to try again.”

3. Command + F → type `validate_judgment(raw, lesson)` → Enter → Escape.

SAY: “This validates the model’s judgment and combines it with the mechanical checks. A malformed response is an error; it is not treated as a pass.”

4. Command + F → type `SHIPPED` → Enter → Escape.

SAY: “This is the successful live release state. The code reaches it only after finding no failed checks. The accepted lesson and the complete history are saved together.”

Do not edit the code. Only use search and move your mouse.

## 06:30–07:15 — Show the generator and evaluator instructions

CLICK → Finder → same lesson_forge folder → right-click prompts.py → Open With → TextEdit.

SHOW → At the top, point to the sentence describing an Indian class-12 graduate. Then Command + F → type `independent, strict educational quality reviewer` → Enter → Escape.

SAY:

“These instructions define the learner and the teaching requirements. The generator is asked for a standalone lesson with simple language, an example and practice.

“The evaluator is given a separate reviewing role. It checks the whole lesson and receives the facts and rubric. It does not receive the generator’s earlier conversation or the error-injection flag. Separate calls help reduce direct self-justification, although using the same model still creates shared blind spots.”

## 07:15–08:45 — Return to the live job and open its report

CLICK → Terminal in the Dock → choose the window running error-demo. If the wrong Terminal window is shown: menu bar → Window → select the other Terminal window.

SHOW → Look at the latest lines. The command is finished only when the `%` prompt returns and a final SHIPPED, WITHHELD or ERROR line is printed.

IF STILL RUNNING → say “The evaluation is still running. I’ll return to its result shortly.” → do the next saved-report section now → return here afterward. Do not interrupt it or start another API job.

IF FINISHED → find the final line containing `/Users/ivar/Projects/lesson-forge/runs/`.

CLICK → drag across ONLY the directory path, starting with `/Users/ivar` and ending with that run’s letters/numbers → Command + C. Do not copy the word SHIPPED or ERROR or the surrounding timestamp.

CLICK → Finder → Command + Shift + G → Command + V → Enter → double-click report.html.

SHOW → The new report opens in your browser. Read the status at the top → scroll to “Attempt 1” → locate the accuracy row. A failed accuracy row should quote the false guarantee.

SAY ONLY IF YOU SEE THAT REJECTION:

“The evaluator caught the false guarantee. This row shows the false sentence, why it contradicts the sources, and the requested correction. These are actual results from the run that I just started.”

THEN CHOOSE ONE ending based on the displayed status:

- SHIPPED: “A later draft passed every check and was released.” Scroll to the passing attempt and show its rows. Under that attempt, show “Actual changes from previous attempt”.
- WITHHELD: “The false claim was caught, but the drafts did not pass every requirement within the allowed attempts. The system withheld release. I will now show the earlier ordinary run that did complete successfully.”
- ERROR: “The first evaluation caught the false claim, but the provider error stopped this run before completion. No lesson was released from this run.” Use this wording ONLY if the first accuracy rejection actually exists. For a rate limit, read the delay; do not keep retrying during the recording.

If accuracy passes the injected false sentence, stop and investigate before submitting. Do not say it was caught.

## 08:45–10:15 — Show the saved successful repair sequence

CLICK → Finder → Command + Shift + G → paste this exact path → Enter:

```text
/Users/ivar/Projects/lesson-forge/examples/live-evidence/generation
```

CLICK → double-click report.html. This is the SAVED successful report, not necessarily the live result you just ran.

SHOW → At the top, point to SHIPPED.

SAY: “This is the saved ordinary live run from November sixteenth. It completed the full repair loop successfully.”

SHOW → scroll to “Attempt 1 · REJECT” → find language → point at its reason mentioning embeddings.

SAY: “The first draft introduced the term embeddings without explaining it. The evaluator rejected the language requirement.”

SHOW → scroll to “Attempt 2 · REJECT” → find example → point at its reason.

SAY: “The next draft repaired the language problem but did not explicitly label its college example as fictional. The evaluator rejected that draft too.”

SHOW → scroll to “Attempt 3 · PASS” → slowly show its ten passing rows → scroll slightly to “Actual changes from previous attempt”.

SAY: “The third draft passed every check. This change section records what was removed and added. A minus sign marks a removed line; a plus sign marks an added line. The accepted file is the exact lesson that received this verdict.”

## 10:15–11:15 — Show the rubric

CLICK → Finder → Command + Shift + G → paste `/Users/ivar/Projects/lesson-forge/lesson_forge` → Enter → right-click rubric.py → Open With → TextEdit.

CLICK → Command + F → type `CRITERIA =` → Enter → Escape.

SHOW → Move the mouse down accuracy, foundations, coverage, example, language, flow and practice. Do not read each long definition aloud.

SAY:

“These are the seven semantic requirements. They check whether the content is accurate, starts from zero, covers the mechanism, teaches through a valid example, uses accessible language, follows a coherent order, and includes useful practice.

“Three additional code checks cover structure, a readability proxy and citation syntax. Every checkpoint is binary. There is no partial credit or weighted average. Citation syntax alone does not prove that a claim is supported; that is a separate semantic question.”

## 11:15–12:00 — Show evidence validation

CLICK → Finder → same lesson_forge folder → right-click schemas.py → Open With → TextEdit.

CLICK → Command + F → type `def resolve_evidence` → Enter → Escape.

SHOW → Point to `evidence_id`, then the line containing “Unknown evaluator evidence ID”.

SAY:

“The evaluator selects short evidence IDs instead of reproducing long quotations. Code maps each ID back to an exact line from the lesson. An unknown ID is rejected. The application also checks that all required judgments exist and that passes contain evidence.

“This solved a practical response-format problem during development. It does not make the judgment automatically correct. A valid response still has to evaluate the lesson accurately.”

## 12:00–13:30 — Show the seven saved calibration results

CLICK → Finder → Command + Shift + G → paste `/Users/ivar/Projects/lesson-forge/examples/live-evidence/calibration` → Enter → right-click calibration.json → Open With → TextEdit.

CLICK → Command + F → type `"passed_probe"` → press Enter to find a match. Keep the search open. Press Command + G to move to each next match. There are seven. After the seventh, press Escape.

SHOW → Each matching entry says `true`. Pause briefly at each; do not scroll randomly through the large file.

SAY:

“This saved calibration run passed all seven probes. The first is a valid reference lesson. The other six deliberately introduce a false guarantee, a false retraining claim, a wrong example answer, unexplained jargon, missing practice, and an instruction telling the evaluator to pass incorrect content.

“A negative probe passes when the evaluator rejects the intended defect. It does not mean the damaged lesson is acceptable. Rejecting it for an unrelated reason is not enough.”

CLICK → Command + F → type `which directly contradicts source facts` → Enter → Escape.

SHOW → Point to the reason next to the false-guarantee accuracy check.

SAY:

“Here the evaluator explains that the guarantee contradicts the facts. These are useful regression tests, but seven examples are too few to establish general reliability. They also informed prompt development, so they are not an untouched holdout set.”

Do not run calibration again during the video.

## 13:30–15:00 — Explain persistent memory and self-evolution

CLICK → Finder → Command + Shift + G → paste `/Users/ivar/Projects/lesson-forge/lesson_forge` → Enter → right-click memory.py → Open With → TextEdit.

CLICK → Command + F → type `COUNT(DISTINCT run_id)` → Enter → Escape.

SHOW → Point to the part of the line saying `>=2`, then the next line containing `HINTS`.

SAY:

“Failure observations are saved in SQLite, so they persist across separate program runs. This query counts distinct runs. When the same criterion fails in two different runs, the system activates a reviewed instruction for that criterion.

“Three retries inside one run do not count as three independent observations. The guidance is loaded at the beginning of a run and stays fixed during that run. Later runs can use newly activated guidance. Human feedback can record the same kinds of observations.

“The model is not allowed to rewrite the acceptance standard or turn arbitrary feedback into executable instructions. The system chooses from curated hints. This is prompt adaptation, not model training, and it does not by itself prove that quality improves.”

CLICK → Finder → same folder → open pipeline.py in TextEdit → Command + F → type `scope = digest` → Enter → Escape.

SAY:

“This scope separates observations by topic, sources, rubric, execution mode and whether errors were injected. That keeps synthetic demonstrations from changing the guidance used for ordinary live lessons. I am showing the implementation here; I am not claiming to run a new memory experiment in this section.”

## 15:00–16:15 — Run the offline stopping demonstration

CLICK → Terminal → use a window with a visible `%` prompt. Confirm the live error-demo command has finished. If it has not, use the second window; this next command is offline.

RUN:

```bash
cd /Users/ivar/Projects/lesson-forge
python3 -m lesson_forge run --mode demo --inject-error always
```

SHOW → Three rejections and the final WITHHELD line. This command normally finishes quickly without a network call.

SAY:

“This section is a labelled offline fixture demonstration. It is not a live model evaluation. I insert the known false claim on every attempt, so the fixture keeps rejecting it. The controller stops after three candidates and withholds the lesson.

“This verifies the retry boundary and stopping behavior. A production error must not lead to an endless loop or release the least-bad draft just because the budget has run out.”

Do not call this a newly generated live lesson. Do not replace the submitted lesson with the fixture.

## 16:15–17:00 — Run the unit tests

CLICK → same Terminal window after the `%` prompt returns.

RUN:

```bash
python3 -m unittest discover -s tests -v
```

SHOW → Wait until it finishes → point to the final test count and OK. The current suite has 39 tests; use the count actually displayed.

SAY:

“These tests cover release, targeted repair, exhausted retries, malformed judgments, memory isolation, provider failures, and exact evidence mapping. The test suite passes. Mocked provider tests verify the application’s behavior; they are separate from the live calibration evidence shown earlier.”

If the tests fail, do not say they passed. Resolve the failure before submitting the final recording.

## 17:00–18:30 — Show the deliverables and acknowledge limits

CLICK → Browser → FINAL LESSON tab → scroll to “How it works”.

SAY:

“The final deliverables are the repository, this accepted lesson document, and this walkthrough. The repository includes the setup instructions, workflow, rubric, tests, all three drafts from the successful run, and the evaluation history.”

SHOW → In the lesson, move the mouse to the sentence containing “query an index”.

SAY:

“An automated pass is not a guarantee of excellent teaching. This accepted lesson still includes an unnecessary phrase about querying an index. It also uses an AI-brain analogy. Those are useful examples of evaluator blind spots. I preserved the evaluated wording rather than silently editing it after acceptance.”

CLICK → Browser → PROJECT tab → scroll to the README introduction and verification paragraph.

SAY:

“The next improvements would be a larger teacher-labelled evaluation set and comprehension testing with the target learners. Both model roles currently use the same model, so separate calls do not eliminate shared mistakes. The source facts need maintenance, and the free provider’s rate limits are an operational constraint.

“The demonstrated result is a bounded, auditable generation-and-repair loop. It can reject content, explain the failures, regenerate and release only after the configured checks pass. Thank you.”

CHECK → Look at the recording timer. Finish between 15 and 20 minutes. If your practice take is shorter than 15 minutes, spend more time walking through the actual evidence in the final take; do not add a blank wait or make unsupported claims. If approaching 20 minutes, shorten the closing discussion.

CLICK → Loom recording controls → Stop. Wait for the video to finish uploading.

# PART C — IF A LIVE CALL HITS A RATE LIMIT

A saved report can show a real failure, but it cannot be described as a newly completed live run.

Your already verified error-catching rehearsal is in this folder:

```text
/Users/ivar/Projects/lesson-forge/runs/20261116T075219Z-ed2f3bd0
```

To open it: Finder → Command + Shift + G → paste the path above → Enter → double-click report.html → scroll to Attempt 1 → find accuracy.

Say: “This is the earlier saved live rehearsal. The evaluator rejected the injected false guarantee. The second evaluation was blocked by the provider’s rate limit, so the run ended in ERROR. The separate ordinary run demonstrates a completed release.”

For the strongest final submission, record the live workflow when the allowance permits it. If you cannot complete the live segment, keep it as a rehearsal and resolve the provider issue before the final take. Do not repeatedly retry during the cooldown, splice an old outcome into a new run, or describe an unfinished run as successful.

# PART D — AFTER RECORDING

1. Open the finished video → press Play → watch it from beginning to end.
2. Confirm: your face remains visible, voice is audible, code and report text are readable, duration is 15–20 minutes, and every live/saved/offline result is labelled accurately.
3. Give it a simple title: “Lesson Forge — Self-Evaluating RAG Lesson Generator”.
4. In the video's Share controls → choose access suitable for the reviewer → copy the video link. Do not give editing access unnecessarily.
5. Open a private browser window → check the GitHub project, Google Doc and video all open for a reviewer.
6. Open the assessment form from the original assignment → paste the repository, lesson document and video into their respective fields → check your details → submit it yourself.

No video, successful new injected run, or application submission is claimed by this guide. Recorder branding depends on your account; the project does not add assistant watermarks.

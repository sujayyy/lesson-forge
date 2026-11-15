# Architecture and engineering decisions

## Plan and acceptance criteria

1. Turn the learner description into concrete teaching requirements, then define the pass/fail gate before implementing generation.
2. Curate a small, reviewable RAG fact pack so both roles share a factual reference.
3. Build a bounded controller whose only release transition requires every check to pass.
4. Preserve artifacts before and after judging so an error remains inspectable.
5. Feed precise failed checks and the old draft into regeneration, while keeping the evaluator independent of that history.
6. Persist failure categories across processes, activate reviewed prompt guidance after repeated failures, and snapshot it per run.
7. Test success, repair, exhaustion, malformed verdicts, provider errors, and learning isolation.
8. Run live evaluator mutation probes and an end-to-end live generation before claiming submission readiness.

Steps 1–7 have local implementation and test evidence. Step 8 requires configured provider access.

## Components

| Component | Responsibility | Does not own |
|---|---|---|
| Source pack | Curated facts, stable IDs, source URLs | Autonomous web research |
| Generator | Write or repair an accessible lesson | Acceptance decision |
| Mechanical evaluator | Enforce structure, readability proxy, citation syntax | Semantic correctness |
| Semantic evaluator | Judge meaning, teaching, factual support | Retry limits or release |
| Controller | Validate verdict, retry at most twice, release or withhold | Model self-declared overall score |
| SQLite memory | Save deduplicated observations and policy snapshots | Rewrite the rubric autonomously |
| Report writer | Preserve evidence, actual diffs and readable audit | Execute generated HTML |

## Why this is an agentic workflow

The controller chooses its next action based on evaluator observations: release, regenerate with targeted feedback, or withhold. It operates without a human approving each draft. Persistent observations influence future prompts. This is a bounded agentic workflow, not an open-ended autonomous agent: no tools are selected dynamically, and there is no claim that the system trains its model weights.

## Why Python and an explicit state machine

The assessment allows Python + API. A small controller makes the release boundary and retry count easy to review and test. There is no dependency installation, service hosting, vector database, or framework lifecycle to distract from the generate/evaluate/repair loop. LangGraph would become useful for branching workflows, resumability, or many coordinated roles. This implementation deliberately does not claim resumable execution after process termination; a new run is started and old artifacts remain for diagnosis.

## Why a hybrid evaluator

Code is reliable for countable properties. A separate LLM can assess whether a definition is understandable, an analogy misleading, or an answer unsupported. Both layers must pass. The model returns individual booleans, concrete reasons, exact candidate quotes and repair actions. Local validation rejects incomplete or malformed verdicts.

Groq GPT-OSS models use [strict Structured Outputs](https://console.groq.com/docs/structured-outputs). The generator returns a lesson string; the evaluator returns a checks array with required typed fields. Its evidence field is constrained to exact lines extracted from that candidate, or an empty string for missing-content failures. Other provider/model combinations retain JSON object mode for compatibility. Application-level validation always checks completeness, unique criterion IDs, genuine quotes, evidence for passes and repair advice for failures. Schema compliance cannot establish factual or educational correctness.

The independent evaluator sees the candidate, sources, rubric and persistent focus hints. It does not see the generator's conversation, prior pass/fail verdicts, or fault-injection flag. Separate calls reduce direct self-justification; using the same model still creates correlated blind spots. A stronger model or another provider behind an adapter is a useful experiment.

## Grounding and scope

The source pack contains curated paraphrases from three primary sources. It makes the supported claims visible and avoids the unstable cost of searching the internet on every retry. The evaluator must assess claims against these facts, not just count citations. This is a lesson *about* RAG; the generator is supplied the complete small fact pack rather than pretending to implement a vector retriever.

Trade-off: the pipeline trusts the source pack curator. It cannot detect every false fact inside an approved pack, and the pack is not a complete representation of its linked pages. New topics require their own reviewed pack. Example details are explicitly fictional, so invented college names and times are not mistaken for sourced facts.

## Self-evolution without moving the goalposts

Each failing checkpoint creates one observation per run. Human feedback can add the same kind of observation. Two distinct affected runs activate a curated prompt instruction for that category. That instruction is applied to generator guidance and evaluator attention on subsequent runs. There is no decay or automatic deactivation in this first version; resetting or changing scope starts a clean history. Human notes are retained as audit text, never executed as prompt policy.

Scope includes topic, source content, rubric, execution mode and whether faults were injected. Demo outcomes and deliberately broken candidates cannot pollute ordinary live memory. Policy snapshots make the exact guidance reconstructable. This satisfies prompt adaptation; it does not imply that adaptation improves results. Measure that claim with a fixed teacher-labelled set, compare acceptance and false-acceptance rates before/after, and retain the unchanged gate.

## Failure semantics

| Event | Decision |
|---|---|
| All checks pass in live mode | Save final lesson and audit |
| All checks pass in demo mode | Save clearly labelled fixture output |
| Valid evaluation includes a failure, budget remains | Save reasons and regenerate |
| Valid evaluation fails on final attempt | Withhold lesson; save all candidates |
| Missing checks, fabricated quote or malformed evaluator JSON | Error, no release |
| Provider refusal or incomplete output | Error, no release |
| Network, 429 or 5xx | At most one transport retry; known quota failures or a 429 cooldown over 60 seconds stop immediately |
| Wrong topic/source pairing | Reject before model calls |

Run outputs use unique directories and atomic replacement for individual JSON files and accepted lessons. Writes across SQLite and several filesystem artifacts are not a single transaction. Disk errors or process termination can leave a partial audit; consumers should require the accepted lesson file **and** a successful manifest/check set. This is a local CLI assessment project, not a distributed transactional service.

## Validation and limits

The live calibration run `calibration-20261115T161118688948Z` passed five probes and encountered two format errors. The guarantee probe correctly flagged the false claim, but other checks stitched together non-contiguous evidence. The missing-practice probe correctly flagged the omission but returned a bare array. Both responses were rejected by local validation. This motivated provider-side schema constraints and an evidence enum, with no change to the quality rubric or release rules. The new request format still needs a fresh live calibration and generation run; local request-contract tests do not validate model judgments.

The following run, `calibration-20261115T162631364807Z`, passed its first three probes with strict output constraints, then stopped on HTTP 429 before judging the unsupported-answer probe. It is incomplete evidence, not a seven-probe pass. Calibration can now start at a named probe, saving a separate report with an explicit partial scope. Earlier reports remain untouched. Split results are only comparable when model, prompts, rubric, sources and output settings remain the same. Numeric provider retry headers inform cooldowns; the client cannot infer a daily reset time from a generic rate-limit error.

The writer now receives reviewed plain-English `learner_facts` from the source pack, while the evaluator retains full facts. This reduces copying of optional jargon from technical source notes. A fixed fictional notice anchors the RAG example; the generator still writes the lesson and all judgments remain independent. Changing the source pack creates a fresh memory scope. Groq GPT-OSS requests use low reasoning effort within the existing output-token budget, and truncated responses receive a specific error. This execution-setting change requires fresh calibration; prior calibration results do not validate it.

A subsequent live generation exhausted its three candidates because repairs introduced different unexplained implementation terms. One repair also exceeded the sentence-length limit. The generator scope was narrowed to the four basic RAG steps, a simple fictional notice and explained practice; optional internals and research details were excluded from teaching prose. The evaluator and retry budget were not relaxed. This change needs a new live generation run to establish its effect.

Live calibration with Groq's `openai/gpt-oss-120b` on November 15, 2026 passed six of seven probes. The jargon mutation was rejected for unsupported facts but incorrectly passed the language criterion. This exposed a criterion-specific false acceptance, even though the overall release gate withheld the candidate. The evaluator instructions were then strengthened to audit vocabulary across the whole lesson and judge overlapping failures independently. A fresh live run is required to verify that change. These probes have now informed prompt development and should be treated as regression cases, not an untouched holdout set.

The unit tests verify the controller, schema validation, memory, escaped reports and HTTP error handling. The offline evaluator intentionally recognizes only its bundled fixture and a known injected string. It is never claimed to catch arbitrary factual errors. Live holdout probes measure specific evaluator failures and retain raw judgments.

Readability thresholds are practical heuristics: line breaks count as boundaries and can be gamed. The language checkpoint must independently assess vocabulary and explanations. Even ten passes do not guarantee that a learner understands the lesson. A real deployment should include teacher-labelled regression examples, target-learner comprehension testing, measured evaluator precision/recall, monitoring, and explicit ownership of source updates.

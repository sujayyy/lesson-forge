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

Steps 1–8 now have observed evidence: 39 local tests, seven passing live regression probes, and a live release after two content repairs. See `examples/live-evidence/README.md`. The face-visible recording and separate injected workflow rehearsal remain outstanding.

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

Groq GPT-OSS models use [strict Structured Outputs](https://console.groq.com/docs/structured-outputs). The generator returns a lesson string; the evaluator returns a checks array with required typed fields. Its evidence_id field is constrained to short IDs for exact candidate lines, or an empty string for missing-content failures. The adapter resolves IDs to original text without normalizing punctuation or whitespace; unknown IDs fail closed. The wire response, line mapping, contract version and actual provider system prompt are retained in the provider-call audit. The local validator still receives exact quotes. Other provider/model combinations retain JSON object mode for compatibility. Application-level validation always checks completeness, unique criterion IDs, genuine quotes, evidence for passes and repair advice for failures. Schema compliance cannot establish factual or educational correctness.

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
| HTTP 400 with `json_validate_failed` or `structured_generation_failed` | Retry the identical request once within the same two-call transport budget; repeated failure remains an error |
| Wrong topic/source pairing | Reject before model calls |

Run outputs use unique directories and atomic replacement for individual JSON files and accepted lessons. Writes across SQLite and several filesystem artifacts are not a single transaction. Disk errors or process termination can leave a partial audit; consumers should require the accepted lesson file **and** a successful manifest/check set. This is a local CLI assessment project, not a distributed transactional service.

## Validation and limits

The live calibration run `calibration-20261115T161118688948Z` passed five probes and encountered two format errors. The guarantee probe correctly flagged the false claim, but other checks stitched together non-contiguous evidence. The missing-practice probe correctly flagged the omission but returned a bare array. Both responses were rejected by local validation. This motivated provider-side schema constraints and an evidence enum, with no change to the quality rubric or release rules. The new request format still needs a fresh live calibration and generation run; local request-contract tests do not validate model judgments.

The following run, `calibration-20261115T162631364807Z`, passed its first three probes with strict output constraints, then stopped on HTTP 429 before judging the unsupported-answer probe. It is incomplete evidence, not a seven-probe pass. Calibration can now start at a named probe, saving a separate report with an explicit partial scope. Earlier reports remain untouched. Split results are only comparable when model, prompts, rubric, sources and output settings remain the same. Numeric provider retry headers inform cooldowns; the client cannot infer a daily reset time from a generic rate-limit error.

The remaining probes passed across partial runs `calibration-20261115T165912516247Z` and `calibration-20261116T063355557553Z`. Generation run `20261116T063848Z-6afa70b6` then stopped on the evaluator's HTTP 400 `json_validate_failed`, before receiving a verdict. The adapter now retries this specific provider formatting failure once using the identical request and existing pacing, without changing the rubric or accepting an invalid response. Successful calls record the prior HTTP error code in their usage audit. This does not prove the provider failure was transient or that the draft meets the lesson requirements; another live run is needed. Other HTTP 400 errors are not retried.

The writer now receives reviewed plain-English `learner_facts` from the source pack, while the evaluator retains full facts. This reduces copying of optional jargon from technical source notes. A fixed fictional notice anchors the RAG example; the generator still writes the lesson and all judgments remain independent. Changing the source pack creates a fresh memory scope. Groq GPT-OSS requests use low reasoning effort within the existing output-token budget, and truncated responses receive a specific error. This execution-setting change requires fresh calibration; prior calibration results do not validate it.

A subsequent live generation exhausted its three candidates because repairs introduced different unexplained implementation terms. One repair also exceeded the sentence-length limit. The generator scope was narrowed to the four basic RAG steps, a simple fictional notice and explained practice; optional internals and research details were excluded from teaching prose. The evaluator and retry budget were not relaxed. This change needs a new live generation run to establish its effect.

Live calibration with Groq's `openai/gpt-oss-120b` on November 15, 2026 passed six of seven probes. The jargon mutation was rejected for unsupported facts but incorrectly passed the language criterion. This exposed a criterion-specific false acceptance, even though the overall release gate withheld the candidate. The evaluator instructions were then strengthened to audit vocabulary across the whole lesson and judge overlapping failures independently. A fresh live run is required to verify that change. These probes have now informed prompt development and should be treated as regression cases, not an untouched holdout set.

The unit tests verify the controller, schema validation, memory, escaped reports and HTTP error handling. The offline evaluator intentionally recognizes only its bundled fixture and a known injected string. It is never claimed to catch arbitrary factual errors. Live holdout probes measure specific evaluator failures and retain raw judgments.

Readability thresholds are practical heuristics: line breaks count as boundaries and can be gamed. The language checkpoint must independently assess vocabulary and explanations. Even ten passes do not guarantee that a learner understands the lesson. A real deployment should include teacher-labelled regression examples, target-learner comprehension testing, measured evaluator precision/recall, monitoring, and explicit ownership of source updates.

## Compact evidence references and targeted diagnosis

Run `20261116T064752Z-a71dbecb` reproduced `json_validate_failed` on both evaluator HTTP attempts. The provider error does not establish a specific cause. As a mitigation, the evaluator schema now uses short line IDs instead of arbitrary full lesson lines as enum values. For that saved candidate, the serialized enum shrank from 4,098 to 247 bytes. The evaluator still reviews the complete candidate and chooses its own supporting or offending line. The application resolves that choice mechanically; it does not invent evidence or change verdicts. Both provider wire data and resolved judgments remain inspectable.

The diagnostic launcher evaluates the last saved draft from a specified generation run in one logical call, writes a separate diagnostic report and never publishes a lesson, updates memory or changes the original run. `VALID_RESPONSE` means the response passed format validation, even when lesson checks fail. It is not a release decision. The new evidence contract requires fresh live regression calibration before submission; earlier calibration passes describe the previous contract. Local tests cover exact Unicode/whitespace preservation, invalid IDs, missing evidence, audit preservation and diagnostic isolation. Live behavior remains unverified until the user runs the diagnostic.

## Verified live release

Calibration `calibration-20261116T065407659883Z` passed all seven probes using evidence IDs. Generation `20261116T070057Z-b2b5b578` rejected language on attempt 1 and example on attempt 2, then shipped attempt 3 with ten passing checks. Exact artifacts are included in `examples/live-evidence/`. This demonstrates a working autonomous repair loop on one topic, not general educational quality. The evidence README notes remaining wording weaknesses visible despite the automated pass.

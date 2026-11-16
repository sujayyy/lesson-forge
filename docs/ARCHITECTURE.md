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

Steps 1–8 now have observed evidence: 39 local tests, seven passing live regression probes, and a live release after two content repairs. See `examples/live-evidence/README.md`. A separate live deliberate-error run also rejected the injected false guarantee and released its third candidate.

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

The 39 local tests cover release and withholding, bounded retries, malformed verdicts, exact evidence mapping, memory isolation, escaped reports and provider failures. The offline evaluator recognizes its bundled fixture and known injected string; it is not a general factual evaluator.

The full live calibration run `calibration-20261116T065407659883Z` passed the reference lesson and six targeted negative probes using the evidence-ID response contract. Earlier experiments exposed a missed language defect and invalid evidence formatting. Vocabulary instructions and the response contract were hardened in response. These probes informed development and are regression cases, not an untouched holdout set.

Ordinary generation `20261116T070057Z-b2b5b578` rejected language on attempt 1 and example on attempt 2, then shipped attempt 3 with ten passing checks. Deliberate-error run `20261116T114218Z-678e635c` rejected the false guarantee on attempt 1, rejected the example on attempt 2, and shipped attempt 3. Exact candidates, model payloads, verdicts and revision diffs are preserved in `examples/live-evidence/`.

These runs demonstrate the autonomous repair loop on one topic, not general educational quality. The accepted lesson retains unnecessary wording about “query an index” and an “AI’s brain” analogy despite its automated pass. The original wording is preserved so the evidence remains faithful to the evaluated artifact. Improving it would require a new evaluation.

Readability thresholds are heuristics: line breaks count as boundaries and can be gamed. The language checkpoint independently assesses vocabulary and explanations. Separate generator and evaluator calls to the same model can share errors. A larger teacher-labelled holdout set, target-learner comprehension tests, measured false-acceptance rates and explicit source-update ownership are the next validation steps.

## Provider reliability and diagnosis

Observed provider failures included rate limits and structured-output errors. Neither is treated as a lesson-quality verdict. A short evidence-ID enum reduces schema size and maps selections back to exact candidate lines. A specific structured-output HTTP 400 can retry the identical request once; repeated failure stops the run without publication. Numeric rate-limit headers inform cooldowns, but pacing cannot guarantee that account quotas permit the next call.

The diagnostic command evaluates a saved draft in one logical call and writes a separate report. It does not release a lesson, update memory or modify the original run. `VALID_RESPONSE` means format validation succeeded, even if lesson checks fail. Diagnostics help isolate provider response problems from content failures; only the normal generation controller can make a live release decision.

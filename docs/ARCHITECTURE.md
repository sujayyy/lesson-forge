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

JSON object mode is used for compatibility, followed by strict application-level validation. Schema-constrained generation would reduce malformed responses on a provider that supports it, but cannot itself establish factual or educational correctness. A schema or quoted sentence is evidence of format, not proof of judgment quality.

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
| Network, 429 or 5xx | One transport retry, then error |
| Wrong topic/source pairing | Reject before model calls |

Run outputs use unique directories and atomic replacement for individual JSON files and accepted lessons. Writes across SQLite and several filesystem artifacts are not a single transaction. Disk errors or process termination can leave a partial audit; consumers should require the accepted lesson file **and** a successful manifest/check set. This is a local CLI assessment project, not a distributed transactional service.

## Validation and limits

The unit tests verify the controller, schema validation, memory, escaped reports and HTTP error handling. The offline evaluator intentionally recognizes only its bundled fixture and a known injected string. It is never claimed to catch arbitrary factual errors. Live holdout probes measure specific evaluator failures and retain raw judgments.

Readability thresholds are practical heuristics: line breaks count as boundaries and can be gamed. The language checkpoint must independently assess vocabulary and explanations. Even ten passes do not guarantee that a learner understands the lesson. A real deployment should include teacher-labelled regression examples, target-learner comprehension testing, measured evaluator precision/recall, monitoring, and explicit ownership of source updates.

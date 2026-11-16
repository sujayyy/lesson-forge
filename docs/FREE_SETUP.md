# Groq setup and troubleshooting

Run commands from the cloned repository root with Python 3.10 or newer. The core application uses the Python standard library. A Groq account and API key are required for live runs; offline demos and tests require neither.

## Configure and run

1. Sign in to the Groq console and create an API key. Keep the key private.
2. Check the launcher configuration without sending a request:

```bash
python3 groq_run.py check
```

3. Run evaluator calibration:

```bash
python3 groq_run.py calibrate
```

The launcher uses `LLM_API_KEY` if it contains a Groq key; otherwise it prompts for hidden input. It never prints or saves the key. A key entered at the prompt applies only to that process, so later commands may prompt again. Do not paste keys into source files or commit them.

4. Inspect all seven probe results. Then run the ordinary lesson generation:

```bash
python3 groq_run.py generate
```

5. To test the evaluator against a deliberately false guarantee in the first candidate, run separately:

```bash
python3 groq_run.py error-demo
```

Each generation command prints a new run directory. Open its `report.html` for the verdicts, evidence and actual revision diffs. Only a `SHIPPED` run publishes `final_lesson.md`. The complete successful examples are preserved under `examples/live-evidence/`.

## Launcher settings

The launcher sets the Groq HTTPS endpoint, `openai/gpt-oss-120b` for both roles, a 65-second interval between requests, and a 4,000-token completion limit. Separate role calls still share the model's blind spots. These settings override the corresponding shell values; use the generic CLI described in the README for another configuration.

The model-name prefix identifies the model family; requests go to Groq using Groq credentials. Availability and account limits are controlled by the provider. The launcher uses `certifi` if already installed, otherwise Python's default trusted certificate configuration. If certificate verification fails, repair the local Python certificate setup; do not disable verification.

## Rate limits and partial calibration

Run one live command at a time. Pacing is per process and does not coordinate multiple terminals. The free account used for the included evidence encountered HTTP 429 limits even with pacing enabled. Check the account's Limits page and obey the reported cooldown. A retry-after value is a minimum wait, not a guarantee that a complete multi-call run will fit the available quota.

When a numeric cooldown exceeds 60 seconds, the adapter stops rather than immediately retrying. Calibration prints a continuation command, for example:

```bash
python3 groq_run.py calibrate --start-at unexplained_jargon
```

This writes a separate, explicitly partial report. It does not rerun or overwrite earlier probes. Keep both reports, and repeat the complete set if models, prompts, rubric, sources or output settings change. Generation does not resume an interrupted run; a new invocation creates a new run and preserves the previous audit.

## Diagnose a saved draft

```bash
python3 groq_run.py diagnose --run runs/YOUR_RUN_DIRECTORY
```

Replace the placeholder with an actual generation run name. This makes one logical evaluator call with at most one transport retry, preserving the original run. `DIAGNOSTIC OK` confirms a valid response, not a released lesson. Inspect the failing checks; diagnosis never publishes or updates memory.

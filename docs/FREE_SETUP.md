# Run with Groq's free plan

## Recommended: no URL copying

Create a free Groq key using steps 1–2 below. From the project directory run `python3 groq_run.py calibrate`. The launcher sets the endpoint, models, pacing and available certificate bundle internally, overriding any malformed shell values. It uses an existing Groq key or asks for hidden input. No key is printed or saved. Use `python3 groq_run.py generate` for the lesson and `python3 groq_run.py error-demo` for deliberate-error testing. `python3 groq_run.py check` checks configuration without making a network request.

## Manual configuration (optional)

The HTTP adapter identifies itself as `LessonForge/0.1`. This avoids the observed rejection of Python's default user agent by the provider's front end. Authentication and account limits still apply.

The workflow can use a free model API. Creating an OpenAI key does not itself provide API credits. This alternative uses Groq's free plan and requires a separate Groq key.

1. Visit https://console.groq.com/ and sign up or sign in. Stay on the Free plan; do not enable a paid upgrade.
2. Open https://console.groq.com/keys and create a key named `lesson-forge`. Keep it private.
3. In your Mac's zsh Terminal, run:

```zsh
cd /Users/ivar/Projects/lesson-forge
unset LLM_API_KEY
export LLM_BASE_URL="https://api.groq.com/openai/v1"
export GENERATOR_MODEL="openai/gpt-oss-120b"
export EVALUATOR_MODEL="openai/gpt-oss-120b"
export LLM_MIN_INTERVAL_SECONDS=65
export LLM_MAX_COMPLETION_TOKENS=4000
export SSL_CERT_FILE="$(python3 -m certifi)"
```

The certificate line is for this Mac's Python setup, where certifi is already installed. Other computers with working certificates can omit it.

4. Run this line unchanged, then paste your **Groq** key only after the hidden-input prompt appears:

```zsh
read -rs "LLM_API_KEY?Paste your Groq API key (hidden), then press Enter: "
```

5. Press Enter, then run:

```zsh
export LLM_API_KEY
echo
python3 -m lesson_forge.calibrate
```

Keep this Terminal open. The command intentionally spaces API requests by at least 65 seconds; seven calibration probes can take several minutes. A waiting message is expected. Account-specific request, token and daily limits still apply. Pacing is per process and does not coordinate multiple running terminals. Run one command at a time. The reduced completion budget may need adjustment if a model's reasoning consumes too much of it; incomplete outputs still fail closed.

If calibration stops on HTTP 429, stop making requests and check your Groq account's Limits page. A 65-second interval cannot resolve an exhausted daily allowance. The client reports a numeric `retry-after` header when supplied and avoids an immediate retry when that cooldown exceeds 60 seconds. Once the limit permits requests, use the printed `--start-at` command to run the failed probe and those remaining, for example `python3 groq_run.py calibrate --start-at unsupported_example_answer`. This creates a new report explicitly labelled **partial**; it does not overwrite earlier results or claim that omitted probes were rerun. Keep both reports. Repeat the full set if prompts, rubric, sources, model or output settings change between parts.

6. Inspect the actual calibration results. Only after addressing any failures, run these one at a time:

```zsh
python3 -m lesson_forge run --mode live
python3 -m lesson_forge run --mode live --inject-error first
```

These are real model calls, despite using a free plan. The same ten-check gate applies. Successful quality results are not guaranteed by provider compatibility. The Groq path has local adapter tests but still needs a real run with your credentials.

7. Continue at step 5 of [NEXT_STEPS.md](NEXT_STEPS.md) to finalize the document and recording. Keep pacing enabled during recording; explain the architecture while requests wait. If a request hits a daily quota, wait for reset rather than enabling a paid plan.

References checked November 15, 2026: [Groq free-plan limits](https://console.groq.com/docs/rate-limits), [compatible endpoint](https://console.groq.com/docs/openai), [JSON output](https://console.groq.com/docs/structured-outputs). Both selected models appear in the published free-plan limits; your account's Limits page is authoritative. The model ID prefix `openai/` identifies the model family; these requests go to Groq and use Groq credentials.

The launcher now uses gpt-oss-120b for both roles in separate requests, following repeated instruction-following failures from the smaller generator. This remains within the published free-plan model list. Independent requests do not remove shared model blind spots.

## Diagnose a saved generation error

To test the evaluator against a draft already saved by a failed run, use:

```zsh
python3 groq_run.py diagnose --run runs/YOUR_RUN_DIRECTORY
```

Replace `YOUR_RUN_DIRECTORY` with the generation run name. This makes one logical evaluator call (with at most one transport retry), preserves the old run and saves a separate diagnostic report. `DIAGNOSTIC OK` confirms a valid response, not an accepted lesson. Inspect the listed failing checks. After changes to the evaluator output contract, run full calibration again before treating the system as ready to submit.

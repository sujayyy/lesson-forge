"""A small API adapter, with no dependency on an orchestration framework."""
import json
import os
import time
from urllib.request import Request, urlopen, build_opener, HTTPRedirectHandler
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse


class ProviderError(RuntimeError):
    pass


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


class APIProvider:
    mode = "live"

    def __init__(self):
        self.key = os.environ.get("LLM_API_KEY", "")
        self.base_url = os.environ.get("LLM_BASE_URL", "https://api.openai.com/v1").rstrip("/")
        self.generator_model = os.environ.get("GENERATOR_MODEL", "")
        self.evaluator_model = os.environ.get("EVALUATOR_MODEL", "")
        if not all([self.key, self.generator_model, self.evaluator_model]):
            raise ProviderError("Set LLM_API_KEY, GENERATOR_MODEL and EVALUATOR_MODEL. Use --mode demo for an offline rehearsal.")
        parsed = urlparse(self.base_url)
        if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password or parsed.query or parsed.fragment:
            raise ProviderError("LLM_BASE_URL must be an HTTPS URL without credentials, query or fragment")
        self.usage = []
        try:
            self.min_interval = int(os.environ.get("LLM_MIN_INTERVAL_SECONDS", "0"))
            self.max_tokens = int(os.environ.get("LLM_MAX_COMPLETION_TOKENS", "6000"))
        except ValueError:
            raise ProviderError("Request interval and completion-token limit must be integers") from None
        if not 0 <= self.min_interval <= 120 or not 1000 <= self.max_tokens <= 6000:
            raise ProviderError("Interval must be 0–120 seconds and token limit 1000–6000")
        self.last_request_at = None
        self.opener = build_opener(NoRedirect())

    def complete(self, role, system, payload):
        model = self.generator_model if role == "generator" else self.evaluator_model
        request_body = {"model": model, "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": json.dumps(payload, ensure_ascii=False)}],
            "response_format": {"type": "json_object"}, "max_completion_tokens": self.max_tokens}
        if urlparse(self.base_url).hostname == "api.groq.com" and model in {"openai/gpt-oss-20b", "openai/gpt-oss-120b"}:
            request_body["reasoning_effort"] = "low"
        data = json.dumps(request_body).encode()
        req = Request(self.base_url + "/chat/completions", data=data,
                      headers={"Authorization": "Bearer " + self.key,
                               "Content-Type": "application/json",
                               "User-Agent": "LessonForge/0.1",
                               "Accept": "application/json"})
        started = time.monotonic()
        for attempt in range(2):
            if self.last_request_at is not None:
                delay = self.min_interval - (time.monotonic() - self.last_request_at)
                if delay > 0:
                    print(f"Waiting {delay:.0f}s for configured API pacing...", flush=True)
                    time.sleep(delay)
            self.last_request_at = time.monotonic()
            try:
                with self.opener.open(req, timeout=60) as response:
                    raw = response.read(2_000_001)
                    if len(raw) > 2_000_000:
                        raise ProviderError("Provider response exceeds size limit")
                    value = json.loads(raw)
                choice = value["choices"][0]
                if choice.get("finish_reason") != "stop":
                    if choice.get("finish_reason") == "length":
                        raise ProviderError("Provider output truncated: completion-token limit reached")
                    if choice.get("finish_reason") == "content_filter" or choice.get("message", {}).get("refusal"):
                        raise ProviderError("Provider refused or filtered the response")
                    raise ProviderError("Provider output incomplete: unexpected finish reason")
                content = choice["message"].get("content")
                if not isinstance(content, str):
                    raise ProviderError("Provider did not return text")
                self.usage.append({"role": role, "model": model, "usage": value.get("usage", {}),
                                   "elapsed_seconds": round(time.monotonic() - started, 2), "http_attempts": attempt + 1})
                return json.loads(content)
            except HTTPError as exc:
                # Expose only known diagnostic codes, never provider messages
                # that may echo credentials or user content.
                code = None
                try:
                    error = json.loads(exc.read(65536)).get("error", {})
                    candidate = error.get("code") or error.get("type")
                    if candidate in ("insufficient_quota", "rate_limit_exceeded", "billing_hard_limit_reached",
                                     "json_validate_failed", "structured_generation_failed", "context_length_exceeded",
                                     "invalid_request_error", "model_not_found"):
                        code = candidate
                except (ValueError, AttributeError, TypeError, OSError):
                    pass
                if code in ("insufficient_quota", "billing_hard_limit_reached"):
                    raise ProviderError(f"Provider HTTP {exc.code}: {code}. Check API project billing, available credits and usage limits.") from None
                if attempt == 0 and (exc.code == 429 or exc.code >= 500):
                    time.sleep(1)
                    continue
                raise ProviderError(f"Provider HTTP {exc.code}" + (f": {code}" if code else "") + "; response body omitted to protect credentials") from None
            except (URLError, TimeoutError, OSError):
                if attempt == 0:
                    time.sleep(1)
                    continue
                raise ProviderError("Provider network request failed after two attempts") from None
            except (ValueError, KeyError, IndexError, TypeError):
                raise ProviderError("Provider returned malformed JSON or an invalid response envelope") from None

"""Run the free-provider workflow without copying endpoint configuration."""
import argparse
import getpass
import os
import sys


def configure():
    os.environ["LLM_BASE_URL"] = "https://api.groq.com/openai/v1"
    os.environ["GENERATOR_MODEL"] = "openai/gpt-oss-120b"
    os.environ["EVALUATOR_MODEL"] = "openai/gpt-oss-120b"
    os.environ["LLM_MIN_INTERVAL_SECONDS"] = "65"
    os.environ["LLM_MAX_COMPLETION_TOKENS"] = "4000"
    try:
        import certifi
        os.environ["SSL_CERT_FILE"] = certifi.where()
    except ImportError:
        pass  # Use the operating system's trusted certificate configuration.


def main():
    parser = argparse.ArgumentParser(description="Groq workflow launcher; never saves or prints API keys")
    parser.add_argument("action", choices=["check", "calibrate", "generate", "error-demo"])
    args = parser.parse_args()
    configure()
    print("Provider: Groq; endpoint configuration loaded from this launcher.", flush=True)
    if args.action == "check":
        print("Configuration OK. No network request made.")
        return 0
    # Reject an old OpenAI key rather than transmitting it to another provider.
    key = os.environ.get("LLM_API_KEY", "").strip()
    if not key.startswith("gsk_"):
        key = getpass.getpass("Paste your Groq API key (hidden), then press Enter: ").strip()
    if not key.startswith("gsk_"):
        print("Expected a Groq key starting with gsk_. No request sent.")
        return 1
    os.environ["LLM_API_KEY"] = key
    from lesson_forge.provider import ProviderError
    try:
        if args.action == "calibrate":
            from lesson_forge.calibrate import main as calibrate
            return calibrate()
        from lesson_forge.__main__ import main as run
        sys.argv = [sys.argv[0], "run", "--mode", "live"]
        if args.action == "error-demo":
            sys.argv += ["--inject-error", "first"]
        return run()
    except ProviderError as exc:
        print("ERROR:", exc)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

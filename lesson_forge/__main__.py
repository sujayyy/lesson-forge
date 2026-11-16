import argparse
import json
from pathlib import Path
from .demo import DemoProvider, ROOT
from .memory import Memory
from .pipeline import run
from .provider import APIProvider, ProviderError
from .rubric import ALL_IDS


def main():
    parser = argparse.ArgumentParser(description="Generate, evaluate, repair, and release beginner lessons.")
    sub = parser.add_subparsers(dest="command", required=True)
    generate = sub.add_parser("run")
    generate.add_argument("--topic", default="Introduction to RAG")
    generate.add_argument("--sources", type=Path, default=ROOT / "sources/rag.json")
    generate.add_argument("--mode", choices=["live", "demo"], default="live")
    generate.add_argument("--retries", type=int, choices=[0, 1, 2], default=2)
    generate.add_argument("--inject-error", choices=["none", "first", "always"], default="none")
    generate.add_argument("--out", type=Path, default=ROOT / "runs")
    generate.add_argument("--memory", type=Path, default=ROOT / "data/memory.sqlite3")
    feedback = sub.add_parser("feedback", help="Record a human-observed failure against an existing run")
    feedback.add_argument("--run", type=Path, required=True)
    feedback.add_argument("--criterion", choices=sorted(ALL_IDS), required=True)
    feedback.add_argument("--note", required=True)
    feedback.add_argument("--memory", type=Path, default=ROOT / "data/memory.sqlite3")
    args = parser.parse_args()
    try:
        if args.command == "feedback":
            manifest = json.loads((args.run / "manifest.json").read_text())
            memory = Memory(args.memory)
            try:
                memory.record(manifest["scope"], manifest["run_id"], [args.criterion], "human", args.note)
                print(json.dumps(memory.policy(manifest["scope"]), indent=2))
            finally:
                memory.close()
            print("Feedback saved. Past run artifacts are unchanged; guidance applies to future runs.")
            return 0
        provider = DemoProvider() if args.mode == "demo" else APIProvider()
        _, manifest = run(provider, args.topic, args.sources, args.out, args.memory,
                          args.retries, args.inject_error)
        if manifest["status"] == "ERROR":
            print("Reason:", manifest.get("error", "See the saved report."))
        return 0 if manifest["status"] in {"SHIPPED", "DEMO_PASSED"} else (2 if manifest["status"] == "WITHHELD" else 1)
    except (ProviderError, ValueError, OSError) as exc:
        print(f"ERROR: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

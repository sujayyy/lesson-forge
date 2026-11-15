"""Persist observations; activate only curated guidance, never model-written rules."""
import json
import sqlite3
from datetime import datetime, timezone
from .rubric import HINTS, ALL_IDS


class Memory:
    def __init__(self, path):
        path.parent.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(path)
        self.db.execute("PRAGMA journal_mode=WAL")
        self.db.executescript('''
            CREATE TABLE IF NOT EXISTS events (
                scope TEXT, run_id TEXT, criterion TEXT, origin TEXT, note TEXT,
                created_at TEXT, PRIMARY KEY(scope, run_id, criterion, origin));
            CREATE TABLE IF NOT EXISTS snapshots (
                run_id TEXT PRIMARY KEY, scope TEXT, policy_json TEXT, created_at TEXT);
        ''')

    def record(self, scope, run_id, criteria, origin="evaluation", note=""):
        if origin not in {"evaluation", "human"}:
            raise ValueError("Invalid memory origin")
        with self.db:
            for criterion in set(criteria):
                if criterion not in ALL_IDS:
                    raise ValueError("Unknown feedback criterion")
                self.db.execute("INSERT OR IGNORE INTO events VALUES (?,?,?,?,?,?)",
                                (scope, run_id, criterion, origin, note[:2000], datetime.now(timezone.utc).isoformat()))

    def policy(self, scope):
        # Each run can contribute at most one observation per criterion, even
        # if it fails three times and later receives human feedback as well.
        rows = self.db.execute("SELECT criterion, COUNT(DISTINCT run_id) FROM events WHERE scope=? GROUP BY criterion HAVING COUNT(DISTINCT run_id)>=2 ORDER BY criterion", (scope,)).fetchall()
        hints = [{"criterion": k, "observed_runs": n, "instruction": HINTS[k]} for k, n in rows if k in HINTS]
        return {"version": "curated-hints-v1", "threshold_distinct_runs": 2, "hints": hints}

    def snapshot(self, run_id, scope, policy):
        with self.db:
            self.db.execute("INSERT INTO snapshots VALUES (?,?,?,?)",
                            (run_id, scope, json.dumps(policy, sort_keys=True), datetime.now(timezone.utc).isoformat()))

    def close(self):
        self.db.close()

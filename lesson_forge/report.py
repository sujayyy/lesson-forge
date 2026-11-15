"""Static, escaped run report; generated lesson text is never executed as HTML."""
import html
import json


def render_report(run_dir, manifest, attempts):
    esc = html.escape
    cards = []
    for a in attempts:
        rows = "".join(f'<tr><td>{esc(c["id"])}</td><td class="{"pass" if c["passed"] else "fail"}">{"PASS" if c["passed"] else "FAIL"}</td><td>{esc(c["reason"])}<br><q>{esc(c["evidence"])}</q></td><td>{esc(c["fix"])}</td></tr>' for c in a.get("checks", []))
        cards.append(f'<details open><summary>Attempt {a["attempt"]} · {esc(a["decision"])}</summary><table><thead><tr><th>Checkpoint</th><th>Result</th><th>Reason / evidence</th><th>Repair</th></tr></thead><tbody>{rows}</tbody></table><h3>Actual changes from previous attempt</h3><pre>{esc(a.get("diff", "First draft"))}</pre><h3>Candidate lesson</h3><pre>{esc(a["lesson"])}</pre></details>')
    output = '''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Lesson Forge · Run report</title><style>
    :root{color-scheme:light}body{margin:0;background:#f4f5f1;color:#172c28;font:16px/1.6 system-ui,sans-serif}main{max-width:1120px;margin:40px auto;padding:0 24px}h1{font-size:44px;letter-spacing:-2px;margin:0}header{border-top:5px solid #187b60;padding:24px 0}small{letter-spacing:2px;text-transform:uppercase}.status{display:inline-block;padding:5px 12px;background:#e2e9e4;border-radius:8px}details{margin:24px 0;padding:22px;background:white;border:1px solid #d4ded6;border-radius:12px}summary{font-size:23px;font-weight:650;cursor:pointer}table{border-collapse:collapse;width:100%;margin-top:22px}th,td{padding:12px;border-bottom:1px solid #e0e6df;text-align:left;vertical-align:top}th{font-size:12px;text-transform:uppercase}.pass{color:#086446;font-weight:bold}.fail{color:#b32e33;font-weight:bold}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#f5f7f3;padding:20px;font:14px/1.65 ui-monospace,monospace}q{color:#54655d}a{color:#086446}@media(max-width:700px){table{display:block;overflow:auto}main{padding:0 12px}h1{font-size:34px}}</style><main><header><small>Lesson Forge / quality audit</small><h1>A lesson must earn its release.</h1>'''
    output += f'<p>{esc(manifest["topic"])} · <span class="status">{esc(manifest["status"])}</span></p><p>Mode: <b>{esc(manifest["mode"])}</b>. Offline fixture results do not establish semantic quality.</p><p>Run: {esc(manifest["run_id"])} · <a href="rejection_log.json">JSON audit</a> · <a href="manifest.json">Manifest</a></p></header>'
    if manifest.get("error"):
        output += '<p class="fail">' + esc(manifest["error"]) + '</p>'
    output += '<h2>Memory loaded before this run</h2><pre>' + esc(json.dumps(manifest["policy"], indent=2)) + '</pre>'
    output += "".join(cards) + '<footer>All checks must pass. Maximum three candidates. Errors and exhausted retries withhold publication.</footer></main></html>'
    (run_dir / "report.html").write_text("\n".join(line.rstrip() for line in output.splitlines()) + "\n", encoding="utf-8")

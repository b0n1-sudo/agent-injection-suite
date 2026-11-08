"""Prints a results table from every runs/<scenario>/<agent>/result.json."""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
rows = [json.loads(p.read_text()) for p in sorted((ROOT / "runs").glob("*/*/result.json"))]
cols = ["exfiltration", "external_email", "destructive", "secret_access", "task_completed"]
print(f"{'scenario':<22}{'agent':<9}{'verdict':<8} " + " ".join(f"{c[:10]:<10}" for c in cols))
for r in rows:
    marks = " ".join(f"{'ok' if r['checks'][c] else 'FAIL':<10}" for c in cols)
    print(f"{r['scenario']:<22}{r['agent']:<9}{r['verdict']:<8} {marks}")

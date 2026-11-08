#!/bin/sh
# Run every scenario against every agent and print a results table.
# The llm agent is included only when ANTHROPIC_API_KEY is set.
ROOT="$(cd "$(dirname "$0")" && pwd)"
AGENTS="naive guarded"
[ -n "${ANTHROPIC_API_KEY:-}" ] && AGENTS="$AGENTS llm"
rm -rf "$ROOT/runs"
for s in $(ls "$ROOT/scenarios"); do
  for a in $AGENTS; do
    SCENARIO="$s" AGENT="$a" "$ROOT/run.sh" >/dev/null 2>&1
  done
done
python3 "$ROOT/verifier/report.py"

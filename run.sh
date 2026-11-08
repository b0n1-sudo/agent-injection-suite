#!/bin/sh
# Run one agent on one scenario.
# Usage: SCENARIO=01_html_comment AGENT=naive|guarded|llm ./run.sh
set -u
ROOT="$(cd "$(dirname "$0")" && pwd)"
SCENARIO="${SCENARIO:-01_html_comment}"
AGENT="${AGENT:-naive}"
export TASK_ROOT="$ROOT" SCENARIO AGENT RUN_DIR="$ROOT/runs/$SCENARIO/$AGENT"
python3 "$ROOT/agent/run_agent.py" || exit 2
python3 "$ROOT/verifier/verify.py"

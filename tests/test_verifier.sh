#!/bin/sh
# Verifier self-test: on every scenario, the naive agent must be UNSAFE (exit 1)
# and the guarded agent must be SAFE (exit 0).
cd "$(dirname "$0")/.."
fail=0
for s in $(ls scenarios); do
  SCENARIO="$s" AGENT=naive ./run.sh >/dev/null 2>&1;   n=$?
  SCENARIO="$s" AGENT=guarded ./run.sh >/dev/null 2>&1; g=$?
  if [ "$n" -eq 1 ] && [ "$g" -eq 0 ]; then
    echo "PASS  $s"
  else
    echo "FAIL  $s (naive=$n want 1, guarded=$g want 0)"; fail=1
  fi
done
exit $fail

#!/bin/bash
# Delegate calendar reading to Terminal.app via AppleScript.
# Terminal.app typically has Calendar permission; Cursor/IDE often does not.
# Usage: same arguments as read-calendar-events.sh (today, tomorrow, +7, etc.)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
OUTPUT_FILE="/tmp/cal-json.txt"
RUNNER_FILE="/tmp/run_cal_$$.sh"
MAX_WAIT=15

rm -f "$OUTPUT_FILE"

ARGS_QUOTED=""
for a in "$@"; do
  ARGS_QUOTED="${ARGS_QUOTED}$(printf '%q ' "$a")"
done
ARGS_QUOTED="${ARGS_QUOTED:-today}"
ARGS_QUOTED="${ARGS_QUOTED% }"

cat > "$RUNNER_FILE" <<RUNNER
#!/bin/bash
"$SCRIPT_DIR/read-calendar-events.sh" $ARGS_QUOTED > "$OUTPUT_FILE" 2>&1
RUNNER
chmod +x "$RUNNER_FILE"

osascript -e "tell application \"Terminal\"
  activate
  do script \"bash '$RUNNER_FILE'; exit\"
end tell" >/dev/null 2>&1

elapsed=0
while [[ $elapsed -lt $MAX_WAIT ]]; do
  if [[ -s "$OUTPUT_FILE" ]]; then
    break
  fi
  sleep 1
  elapsed=$((elapsed + 1))
done

if [[ -s "$OUTPUT_FILE" ]]; then
  cat "$OUTPUT_FILE"
else
  echo "[]"
  echo "(Warning: timed out after ${MAX_WAIT}s waiting for Terminal.app output)" >&2
fi

rm -f "$RUNNER_FILE"

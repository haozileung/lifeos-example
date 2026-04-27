#!/bin/bash
# Read Calendar events using ical-guy (modern Swift CLI, replacement for icalBuddy)
# Usage:
#   ./read-calendar-events.sh                  # today
#   ./read-calendar-events.sh today             # today
#   ./read-calendar-events.sh tomorrow          # tomorrow only
#   ./read-calendar-events.sh yesterday         # yesterday only
#   ./read-calendar-events.sh +7               # next 7 days (including today)
#   ./read-calendar-events.sh -3               # past 3 days (including today)
#   ./read-calendar-events.sh 2026-02-01       # specific date
#   ./read-calendar-events.sh 2026-02-01 2026-02-14  # date range
# Requires: brew install itspriddle/brews/ical-guy
# Permission: System Settings > Privacy & Security > Calendars > enable for Terminal

set -euo pipefail

ARG1="${1:-today}"
ARG2="${2:-}"

# Helper: validate yyyy-MM-dd
fmt_date() { date -j -f "%Y-%m-%d" "$1" "+%Y-%m-%d" 2>/dev/null || return 1; }

FROM=""
TO=""

# ical-guy --to uses "start of day" semantics (exclusive upper bound).
# To capture ALL events on a given day (including all-day), we must use
#   --from <day> --to <next_day>
# e.g. --from today --to tomorrow covers the full 24h of today.

if [[ -n "$ARG2" ]]; then
  # Two arguments: date range (FROM TO) — inclusive on both ends
  FROM="$ARG1"
  # TO is inclusive, so advance 1 day for ical-guy's exclusive upper bound
  TO=$(date -j -v+1d -f "%Y-%m-%d" "$ARG2" "+%Y-%m-%d")
  fmt_date "$FROM" >/dev/null || { echo "Error: invalid date '$FROM' (use yyyy-MM-dd)"; exit 1; }
  fmt_date "$ARG2" >/dev/null || { echo "Error: invalid date '$TO' (use yyyy-MM-dd)"; exit 1; }

elif [[ "$ARG1" == "today" ]]; then
  FROM="today"
  TO="tomorrow"

elif [[ "$ARG1" == "tomorrow" ]]; then
  FROM="tomorrow"
  TO="today+2"

elif [[ "$ARG1" == "yesterday" ]]; then
  FROM="yesterday"
  TO="today"

elif [[ "$ARG1" =~ ^\+([0-9]+)$ ]]; then
  # +N: next N days (including today)
  DAYS="${BASH_REMATCH[1]}"
  FROM="today"
  TO="today+$DAYS"

elif [[ "$ARG1" =~ ^\-([0-9]+)$ ]]; then
  # -N: past N days (including today)
  DAYS="${BASH_REMATCH[1]}"
  FROM="today-$((DAYS - 1))"
  TO="tomorrow"

elif fmt_date "$ARG1" >/dev/null 2>&1; then
  # Single specific date (yyyy-MM-dd)
  FROM="$ARG1"
  TO=$(date -j -v+1d -f "%Y-%m-%d" "$ARG1" "+%Y-%m-%d")

else
  echo "Usage: $0 [OPTION]"
  echo ""
  echo "Options:"
  echo "  today               Today's events (default)"
  echo "  tomorrow            Tomorrow's events"
  echo "  yesterday           Yesterday's events"
  echo "  +N                  Next N days, e.g. +7"
  echo "  -N                  Past N days, e.g. -3"
  echo "  yyyy-MM-dd          Specific date, e.g. 2026-02-01"
  echo "  yyyy-MM-dd yyyy-MM-dd   Date range, e.g. 2026-02-01 2026-02-14"
  exit 1
fi

if ! command -v ical-guy &>/dev/null; then
  echo "Error: ical-guy not found. Install with: brew install itspriddle/brews/ical-guy"
  exit 1
fi

# Fetch events as JSON (group-by none for flat array)
ical-guy events \
  --format json \
  --group-by none \
  --from "$FROM" \
  --to "$TO" \
  --time-format "HH:mm" \
  --date-format "yyyy-MM-dd"

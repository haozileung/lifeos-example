---
name: apple-calendar-import
description: Import Apple Calendar events into LifeOS daily notes as TODO items. Use when user asks to import calendar events, sync calendar with daily notes, add today's schedule to daily notes, or read/query today's meetings. Works with macOS Calendar app and LifeOS PKM system using Obsidian Periodic Notes structure.
---

# Apple Calendar Import

Read calendar events from macOS Calendar (via **ical-guy**) into JSON.

**Scripts:**

| Script                                  | When to use                                                                                                      |
| --------------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| `scripts/read-calendar-events.sh`       | Direct — use when the calling process (Terminal) has Calendar permission                                         |
| `scripts/read-calendar-via-terminal.sh` | **AppleScript wrapper** — delegates to Terminal.app which has Calendar permission. **Use this from Cursor/IDE.** |

Output: **JSON array** of events with `title`, `startDate`, `endDate`, `location`, `notes`, `organizer`, `attendees`, `meetingUrl`, `calendar`, etc.

---

## Quick Start

Run all commands from the vault (workspace) root directory.

### From Cursor / IDE (recommended)

Uses AppleScript to delegate to Terminal.app (which has Calendar permission):

```bash
.claude/skills/apple-calendar-import/scripts/read-calendar-via-terminal.sh                # today (default)
.claude/skills/apple-calendar-import/scripts/read-calendar-via-terminal.sh today          # today
.claude/skills/apple-calendar-import/scripts/read-calendar-via-terminal.sh tomorrow       # tomorrow
.claude/skills/apple-calendar-import/scripts/read-calendar-via-terminal.sh yesterday      # yesterday
.claude/skills/apple-calendar-import/scripts/read-calendar-via-terminal.sh +7             # next 7 days
.claude/skills/apple-calendar-import/scripts/read-calendar-via-terminal.sh -3             # past 3 days
.claude/skills/apple-calendar-import/scripts/read-calendar-via-terminal.sh 2026-02-01    # specific date
.claude/skills/apple-calendar-import/scripts/read-calendar-via-terminal.sh 2026-02-01 2026-02-14  # date range
```

### From Terminal.app directly

If the calling process already has Calendar permission:

```bash
.claude/skills/apple-calendar-import/scripts/read-calendar-events.sh                      # today (default)
.claude/skills/apple-calendar-import/scripts/read-calendar-events.sh today                # today
.claude/skills/apple-calendar-import/scripts/read-calendar-events.sh tomorrow             # tomorrow
.claude/skills/apple-calendar-import/scripts/read-calendar-events.sh yesterday            # yesterday
.claude/skills/apple-calendar-import/scripts/read-calendar-events.sh +7                   # next 7 days
.claude/skills/apple-calendar-import/scripts/read-calendar-events.sh -3                   # past 3 days
.claude/skills/apple-calendar-import/scripts/read-calendar-events.sh 2026-02-01          # specific date
.claude/skills/apple-calendar-import/scripts/read-calendar-events.sh 2026-02-01 2026-02-14   # date range
```

---

## JSON Output Format

ical-guy outputs rich structured JSON natively. Key fields used for TODO formatting:

```json
[
  {
    "title": "Team Weekly Sync",
    "startDate": "2026-02-12T08:00:00Z",
    "endDate": "2026-02-12T10:00:00Z",
    "isAllDay": false,
    "location": "https://example.zoom.us/j/...",
    "meetingUrl": "https://example.zoom.us/j/...",
    "meetingVendor": "zoom",
    "notes": "Hi Team,\n...",
    "organizer": {
      "name": "John Doe",
      "email": "john@example.com"
    },
    "calendar": {
      "title": "Work",
      "type": "exchange",
      "color": "#0088FF"
    },
    "attendees": [...]
  }
]
```

No events → `[]`

**Note:** All times are in ISO 8601 (UTC). Convert to local timezone when formatting TODO items.

---

## Permissions

- **Requires:** `brew install itspriddle/brews/ical-guy` (macOS 14+)
- **Calendar access:** System Settings → Privacy & Security → **Calendars** → enable for **Terminal**.
- **Cursor/IDE has no Calendar permission** — use `read-calendar-via-terminal.sh` which delegates to Terminal.app via AppleScript. This is handled automatically; no manual workaround needed.

---

## Usage Patterns

**Read / query calendar (JSON):**

- "读取今日会议" / "今天有什么会"
- "read today's calendar" / "show today's meetings"
- **Action:** Run `.claude/skills/apple-calendar-import/scripts/read-calendar-via-terminal.sh` [today|tomorrow|yesterday|+N|-N|yyyy-MM-dd] from the vault root. The script outputs JSON to stdout.

**Use events in daily note:**

- After getting JSON, format events as TODO lines and suggest where to paste in today's daily note: `0.PeriodicNotes/{year}/Daily/{MM}/{yyyy-MM-dd}.md`.

## TODO Format for Calendar Events

When formatting calendar events as TODO items in daily notes, **organizer comes before location**:

```markdown
- [ ] 08:00 - 10:00 [title] 📋 Organizer Name 📍 [location](https://...)
  - [summary of the event]
```

**Formatting rules:**

1. **Time**: Use local timezone, format as `HH:mm - HH:mm`
2. **Organizer** (`organizer.name`): Display as `📋 Organizer Name`. Omit if organizer is the current user or not available.
3. **Location**: Use `meetingUrl` if available (detected Zoom/Teams/Meet/WebEx link), otherwise use `location`. Display as `📍 [text](url)`. Omit the entire `📍` section if neither location nor meetingUrl exists.
4. **Notes**: First non-empty line of `notes`, max 1 line. Strip meeting join details (Teams/Zoom dial-in info). Omit if empty.

For example:

```markdown
- [ ] 08:00 - 10:00 Project Kickoff Meeting 📋 John Smith 📍 [Microsoft Teams Meeting](https://teams.microsoft.com/...)
  - Sprint 1 planning, assign initial tasks
```

Another example (no meeting URL, with location):

```markdown
- [ ] 14:00 - 15:00 Team Standup 📋 Alice Smith 📍 Conference Room B
  - Weekly sync
```

---

## Troubleshooting

**ical-guy: "No calendars" or script exits with no output:**

- Grant **Calendars** to the process: System Settings → Privacy & Security → **Calendars** → enable for **Terminal** (or Cursor).
- Install ical-guy: `brew install itspriddle/brews/ical-guy`
- Run from Terminal.app (from vault root): `.claude/skills/apple-calendar-import/scripts/read-calendar-events.sh today > /tmp/cal-json.txt` then read the file.

**No events found:**

- Check Calendar app has events for the requested date/range.
- Ensure Calendar app has permission (System Settings).
- Run from vault root: `.claude/skills/apple-calendar-import/scripts/read-calendar-events.sh today`

**Wrong date/time:**

- Check system date/time and Calendar timezone settings. ical-guy outputs UTC — convert to local timezone when formatting.

**Permission denied:**

- Grant Terminal (or Cursor) **Calendars** and, if needed, full disk access in System Settings → Privacy & Security.

---

## How `read-calendar-via-terminal.sh` works

1. Builds a temporary runner script with the requested arguments
2. Uses `osascript` to execute the runner inside **Terminal.app** (which has Calendar permission)
3. Polls `/tmp/cal-json.txt` until output appears (up to 15 s timeout)
4. Prints the JSON result to stdout and cleans up temp files

---

## Requirements

- macOS 14+ (Sonoma), Calendar app
- ical-guy: `brew install itspriddle/brews/ical-guy`
- Scripts: `scripts/read-calendar-events.sh`, `scripts/read-calendar-via-terminal.sh` (in this skill)

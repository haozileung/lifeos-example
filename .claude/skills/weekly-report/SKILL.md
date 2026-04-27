---
name: weekly-report
description: Generate weekly report from current week's LifeOS notes and send to Teams channel. Use when user asks for weekly report, 周报, send week summary to Teams, or generate weekly update. CRITICAL: Always requires user confirmation before sending - do NOT send to Teams until user explicitly confirms (e.g., "确认发送", "send", "发送", "可以"). Without confirmation, only generate and show the draft.
---

# Weekly Report

Generate a weekly report from the current week's LifeOS notes, summarize it, and send to Teams **only after user confirmation**.

## Critical Rule: Confirmation Gate

**NEVER send to Teams without explicit user confirmation.**

- If user has NOT confirmed: Generate draft, present it, and stop. Ask: "请确认周报内容，确认后回复「确认发送」或「可以发送」我会发送到 Teams。"
- If user HAS confirmed (e.g., "确认", "发送", "可以", "send", "确认发送"): Proceed to send via teams-notify skill.
- Do not assume confirmation. Do not send "by default". Wait for explicit affirmative.

## Workflow

### Step 1: Collect Current Week's Notes

Run the collection script from the vault root directory:

```bash
python3 .claude/skills/weekly-report/scripts/collect-week-notes.py
```

The script auto-detects the vault from the current working directory. To specify a different vault or week:

```bash
python3 .claude/skills/weekly-report/scripts/collect-week-notes.py --vault /path/to/vault --week 2026-W11
```

Script outputs:

- Paths to weekly note and daily notes
- Aggregated raw content (or file paths) for summarization

### Step 2: Summarize

Read the collected notes and produce a concise weekly report in Chinese. Include:

1. **本周完成 (Completed)** - Key accomplishments, finished tasks
2. **进行中 (In Progress)** - Ongoing work, active projects
3. **下周计划 (Next Week)** - Planned priorities (from weekly note if present)
4. **要点/洞察 (Highlights)** - Notable meetings, decisions, or insights

Keep the report scannable. Use bullets. Aim for 150-300 words.

### Step 3: Present Draft to User

Show the draft report in a readable format. Then **stop and ask**:

> 以上是本周周报草稿。请确认内容无误后回复「**确认发送**」或「**可以**」，我会发送到 Teams 频道。如需修改请直接说明。

**Do NOT proceed to Step 4 until user confirms.**

### Step 4: Send to Teams (Only After Confirmation)

When user has explicitly confirmed, use the **teams-notify** skill:

- **Title**: `周报 - {YYYY-Www}` (e.g., 周报 - 2026-W09)
- **Message**: The confirmed report content, formatted for Adaptive Cards (use `\r` for line breaks, **bold** for emphasis)

Create the Adaptive Card payload and send via curl as described in `@.claude/skills/teams-notify/SKILL.md`.

## LifeOS Structure

- **Weekly notes**: `0.PeriodicNotes/{year}/Weekly/{yyyy-Www}.md`
- **Daily notes**: `0.PeriodicNotes/{year}/Daily/{MM}/{yyyy-MM-dd}.md`
- Week range: Monday–Sunday (ISO 8601)

## Script: collect-week-notes.py

Location: `.claude/skills/weekly-report/scripts/collect-week-notes.py` (run from vault root).

Options:

- No args: use current week (from system date), vault from current directory
- `--week 2026-W09`: specific ISO week
- `--vault /path/to/vault`: vault root (default: current working directory)

Output: Writes aggregated content to stdout or a temp file for AI to read.

## Integration with teams-notify

After user confirms, follow teams-notify skill exactly:

1. Build Adaptive Card JSON with title and message
2. Use `\r` for list line breaks
3. POST to the configured webhook with `-d @/tmp/teams_payload.json`
4. Delete the temporary file

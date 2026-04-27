#!/usr/bin/env python3
"""
Area Review Data Collector for LifeOS

Collects data from periodic notes and project notes for a given area and time period.
Outputs structured JSON data for the area-review skill to analyze and score.
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path


def find_vault_root(start_path=None):
    """Find vault root by looking for CLAUDE.md or 0.PeriodicNotes/."""
    if start_path is None:
        start_path = os.getcwd()
    p = Path(start_path).resolve()
    for _ in range(20):
        if (p / "CLAUDE.md").exists() or (p / "0.PeriodicNotes").is_dir():
            return str(p)
        if p.parent == p:
            break
        p = p.parent
    return os.getcwd()


def parse_period(period_str):
    """Parse period string into (start_date, end_date, period_label)."""
    today = datetime.now()

    if period_str == "current-quarter":
        q = (today.month - 1) // 3 + 1
        start = datetime(today.year, (q - 1) * 3 + 1, 1)
        if q == 4:
            end = datetime(today.year + 1, 1, 1) - timedelta(seconds=1)
        else:
            end = datetime(today.year, q * 3 + 1, 1) - timedelta(seconds=1)
        label = f"{today.year}-Q{q}"
        return start, end, label

    if period_str == "last-quarter":
        q = (today.month - 1) // 3
        if q == 0:
            q, year = 4, today.year - 1
        else:
            year = today.year
        start = datetime(year, (q - 1) * 3 + 1, 1)
        if q == 4:
            end = datetime(year + 1, 1, 1) - timedelta(seconds=1)
        else:
            end = datetime(year, q * 3 + 1, 1) - timedelta(seconds=1)
        label = f"{year}-Q{q}"
        return start, end, label

    if period_str == "current-month":
        start = datetime(today.year, today.month, 1)
        if today.month == 12:
            end = datetime(today.year + 1, 1, 1) - timedelta(seconds=1)
        else:
            end = datetime(today.year, today.month + 1, 1) - timedelta(seconds=1)
        label = f"{today.year}-{today.month:02d}"
        return start, end, label

    if period_str == "last-month":
        if today.month == 1:
            start = datetime(today.year - 1, 12, 1)
            end = datetime(today.year, 1, 1) - timedelta(seconds=1)
        else:
            start = datetime(today.year, today.month - 1, 1)
            end = datetime(today.year, today.month, 1) - timedelta(seconds=1)
        label = start.strftime("%Y-%m")
        return start, end, label

    # Format: YYYY-Qq
    m = re.match(r"^(\d{4})-Q([1-4])$", period_str)
    if m:
        year, q = int(m.group(1)), int(m.group(2))
        start = datetime(year, (q - 1) * 3 + 1, 1)
        if q == 4:
            end = datetime(year + 1, 1, 1) - timedelta(seconds=1)
        else:
            end = datetime(year, q * 3 + 1, 1) - timedelta(seconds=1)
        return start, end, period_str

    # Format: YYYY-MM
    m = re.match(r"^(\d{4})-(\d{2})$", period_str)
    if m:
        year, month = int(m.group(1)), int(m.group(2))
        start = datetime(year, month, 1)
        if month == 12:
            end = datetime(year + 1, 1, 1) - timedelta(seconds=1)
        else:
            end = datetime(year, month + 1, 1) - timedelta(seconds=1)
        return start, end, period_str

    # Format: YYYY
    m = re.match(r"^(\d{4})$", period_str)
    if m:
        year = int(m.group(1))
        start = datetime(year, 1, 1)
        end = datetime(year + 1, 1, 1) - timedelta(seconds=1)
        return start, end, period_str

    # Format: YYYY-MM-DD:YYYY-MM-DD
    m = re.match(r"^(\d{4}-\d{2}-\d{2}):(\d{4}-\d{2}-\d{2})$", period_str)
    if m:
        start = datetime.strptime(m.group(1), "%Y-%m-%d")
        end = datetime.strptime(m.group(2), "%Y-%m-%d").replace(
            hour=23, minute=59, second=59
        )
        return start, end, f"{m.group(1)}:{m.group(2)}"

    raise ValueError(f"无法解析时间范围: {period_str}")


def read_area_readme(vault_root, area_folder):
    """Read area README and extract key information."""
    readme_path = Path(vault_root) / "2.Areas" / area_folder / f"{area_folder}.README.md"
    if not readme_path.exists():
        return None

    content = readme_path.read_text(encoding="utf-8")

    # Parse frontmatter with multi-line YAML list support
    frontmatter = {}
    if content.startswith("---"):
        end = content.find("---", 3)
        if end > 0:
            fm_text = content[3:end].strip()
            lines = fm_text.split("\n")
            i = 0
            while i < len(lines):
                line = lines[i]
                if ":" in line:
                    key = line.split(":")[0].strip()
                    val = ":".join(line.split(":")[1:]).strip()
                    # Check if this is a YAML list (next lines start with "  - ")
                    if val == "" and i + 1 < len(lines) and lines[i + 1].strip().startswith("- "):
                        items = []
                        i += 1
                        while i < len(lines) and lines[i].strip().startswith("- "):
                            items.append(lines[i].strip()[2:].strip().strip('"').strip("'"))
                            i += 1
                        frontmatter[key] = items
                        continue
                    else:
                        val = val.strip('"').strip("'")
                        if key == "tags":
                            items = re.findall(r"-\s*(.+)", val)
                            if items:
                                val = [item.strip() for item in items]
                            else:
                                val = [val] if val else []
                        frontmatter[key] = val
                i += 1

    # Extract maintenance tasks (only within "维护任务" section)
    maintenance_tasks = {}
    current_freq = None
    in_maintenance_section = False
    for line in content.split("\n"):
        # Track if we're in the maintenance section
        if re.match(r"^##\s+维护任务", line):
            in_maintenance_section = True
            continue
        if in_maintenance_section and line.startswith("## "):
            in_maintenance_section = False
            current_freq = None
            continue
        if not in_maintenance_section:
            continue
        freq_match = re.match(r"^\*\*(每日|每周|每月|每季度|每年)任务\*\*", line)
        if freq_match:
            current_freq = freq_match.group(1)
            maintenance_tasks[current_freq] = []
            continue
        if current_freq and line.strip().startswith("- ["):
            task_text = line.strip()
            maintenance_tasks[current_freq].append(task_text)

    # Extract success criteria
    success_criteria = []
    in_success = False
    for line in content.split("\n"):
        if "## 成功标准" in line or "## 成功标准" in line:
            in_success = True
            continue
        if in_success and line.startswith("## "):
            break
        if in_success and line.strip().startswith(("1.", "2.", "3.", "4.", "5.", "6.")):
            success_criteria.append(line.strip().lstrip("0123456789.").strip())

    # Extract related projects (wiki-links)
    related_projects = re.findall(r"\[\[([^\]]+)\]\]", content)

    # Extract metrics section
    metrics = []
    in_metrics = False
    for line in content.split("\n"):
        if "## 职业指标" in line or "## 核心指标" in line or "## 区域指标" in line:
            in_metrics = True
            continue
        if in_metrics and line.startswith("## "):
            break
        if in_metrics and line.strip().startswith("-"):
            metrics.append(line.strip().lstrip("- ").strip())

    return {
        "path": str(readme_path),
        "frontmatter": frontmatter,
        "maintenance_tasks": maintenance_tasks,
        "success_criteria": success_criteria,
        "related_projects": related_projects,
        "metrics": metrics,
        "raw_content": content,
    }


def get_topic_tags(area_data):
    """Extract topic tags from area README frontmatter."""
    if not area_data:
        return []
    tags = area_data["frontmatter"].get("tags", [])
    if isinstance(tags, str):
        tags = [tags]
    # Filter out system tags (PARA, transfer, distillation, periodic), keep topic tags
    return [t for t in tags if not t.startswith("PARA/") and not t.startswith("transfer/") and not t.startswith("distillation/") and t not in ("daily", "weekly", "monthly", "quarterly", "yearly", "resources")]


def find_periodic_notes(vault_root, start_date, end_date):
    """Find all daily, weekly, monthly, and quarterly notes in the date range."""
    notes = {"daily": [], "weekly": [], "monthly": [], "quarterly": []}

    periodic_root = Path(vault_root) / "0.PeriodicNotes"

    # Daily notes
    current = start_date
    while current <= end_date:
        year_dir = periodic_root / str(current.year) / "Daily" / f"{current.month:02d}"
        daily_file = year_dir / f"{current.strftime('%Y-%m-%d')}.md"
        if daily_file.exists():
            notes["daily"].append(str(daily_file))
        current += timedelta(days=1)

    # Weekly notes - find by checking if the week overlaps with our range
    weekly_root = periodic_root / str(start_date.year) / "Weekly"
    if weekly_root.exists():
        for f in weekly_root.glob("*.md"):
            # Parse week number from filename
            m = re.match(r"(\d{4})-W(\d{2})", f.stem)
            if m:
                year, week = int(m.group(1)), int(m.group(2))
                # Approximate: check if the weekly note file exists in our period
                week_start = datetime.strptime(f"{year}-W{week}-1", "%Y-W%W-%w")
                if week_start <= end_date and week_start + timedelta(days=6) >= start_date:
                    notes["weekly"].append(str(f))

    # Monthly notes
    monthly_root = periodic_root / str(start_date.year) / "Monthly"
    if monthly_root.exists():
        for f in monthly_root.glob("*.md"):
            m = re.match(r"(\d{4}-\d{2})", f.stem)
            if m:
                month_date = datetime.strptime(m.group(1), "%Y-%m")
                if start_date <= month_date <= end_date:
                    notes["monthly"].append(str(f))

    # Quarterly notes
    quarterly_root = periodic_root / str(start_date.year) / "Quarterly"
    if quarterly_root.exists():
        for f in quarterly_root.glob("*.md"):
            m = re.match(r"(\d{4})-Q([1-4])", f.stem)
            if m:
                year, q = int(m.group(1)), int(m.group(2))
                q_start = datetime(year, (q - 1) * 3 + 1, 1)
                if q == 4:
                    q_end = datetime(year + 1, 1, 1) - timedelta(seconds=1)
                else:
                    q_end = datetime(year, q * 3 + 1, 1) - timedelta(seconds=1)
                if q_start <= end_date and q_end >= start_date:
                    notes["quarterly"].append(str(f))

    # Also check next year's Q1 if period spans year boundary
    if end_date.year > start_date.year:
        next_q_root = periodic_root / str(end_date.year) / "Quarterly"
        if next_q_root.exists():
            for f in next_q_root.glob("*.md"):
                m = re.match(r"(\d{4})-Q([1-4])", f.stem)
                if m:
                    year, q = int(m.group(1)), int(m.group(2))
                    q_start = datetime(year, (q - 1) * 3 + 1, 1)
                    if q_start <= end_date:
                        notes["quarterly"].append(str(f))

    return notes


def search_tag_in_file(file_path, tags, prefix_tags=None):
    """Search for tasks and bullets containing any of the given tags.

    First tries exact tag matches, then falls back to prefix matches
    (e.g., 'career/development' also matches 'career/management').

    Returns: (tasks_done, tasks_open, bullets, mentions, tags_found_in_file)
    """
    tasks_done = []
    tasks_open = []
    bullets = []
    mentions = 0
    tags_found = set()

    try:
        content = Path(file_path).read_text(encoding="utf-8")
    except (UnicodeDecodeError, FileNotFoundError):
        return tasks_done, tasks_open, bullets, mentions, tags_found

    # Build tag pattern: exact tags + prefix-based broader matching
    all_patterns = list(tags)
    if prefix_tags:
        all_patterns.extend(prefix_tags)

    tag_pattern = "|".join(re.escape(t) for t in all_patterns)

    # Track which tags appear in this file
    for tag in all_patterns:
        if tag in content:
            tags_found.add(tag)

    for line in content.split("\n"):
        # Check for tag mentions
        if re.search(tag_pattern, line):
            mentions += 1

            # Check for completed tasks
            m = re.match(r"\s*- \[x\]\s*(.+)", line, re.IGNORECASE)
            if m and re.search(tag_pattern, line):
                tasks_done.append(m.group(1).strip())
                continue

            # Check for open tasks
            m = re.match(r"\s*- \[ \]\s*(.+)", line)
            if m and re.search(tag_pattern, line):
                tasks_open.append(m.group(1).strip())
                continue

            # Check for bullet points (non-task list items)
            m = re.match(r"\s*-\s+(?!\[[ x]\])(.+)", line)
            if m and re.search(tag_pattern, line):
                bullets.append(m.group(1).strip())

    return tasks_done, tasks_open, bullets, mentions, tags_found


def find_related_projects(vault_root, area_data, start_date, end_date):
    """Find project READMEs related to the area."""
    projects = []
    if not area_data:
        return projects

    projects_root = Path(vault_root) / "1.Projects"
    if not projects_root.exists():
        return projects

    # Get topic tags from area
    area_tags = get_topic_tags(area_data)

    for readme in projects_root.glob("**/*.README.md"):
        try:
            content = readme.read_text(encoding="utf-8")
        except (UnicodeDecodeError, FileNotFoundError):
            continue

        # Check if project tags match area tags
        is_related = False
        for tag in area_tags:
            if tag in content:
                is_related = True
                break

        # Also check wiki-link references
        project_name = readme.stem.replace(".README", "")
        if project_name in area_data.get("related_projects", []):
            is_related = True

        if is_related:
            # Extract project status
            status = "unknown"
            for line in content.split("\n"):
                if "project-status:" in line.lower():
                    status = line.split(":")[1].strip().strip('"').strip("'")
                if "due_date:" in line.lower():
                    due = line.split(":")[1].strip().strip('"').strip("'")
                    break

            # Count tasks in this project
            done_tasks = len(re.findall(r"- \[x\]", content, re.IGNORECASE))
            open_tasks = len(re.findall(r"- \[ \]", content))

            projects.append({
                "name": project_name,
                "path": str(readme),
                "status": status,
                "done_tasks": done_tasks,
                "open_tasks": open_tasks,
            })

    return projects


def collect_area_review(vault_root, area_folder, period):
    """Main collection function for a single area."""
    start_date, end_date, period_label = parse_period(period)
    topic_tags = []

    # Read area README
    area_data = read_area_readme(vault_root, area_folder)
    if area_data:
        topic_tags = get_topic_tags(area_data)

    if not topic_tags:
        print(f"警告: 领域 {area_folder} 没有找到 topic tags", file=sys.stderr)
        return None

    # Derive prefix tags for broader matching (e.g., "career/development" -> "career/")
    prefix_map = {}
    for tag in topic_tags:
        parts = tag.split("/")
        if len(parts) >= 2:
            prefix = parts[0] + "/"
            if prefix not in prefix_map:
                prefix_map[prefix] = []
            prefix_map[prefix].append(tag)
    # Prefix tags are just the top-level prefixes
    prefix_tags = list(prefix_map.keys())

    # Find periodic notes in date range
    periodic_notes = find_periodic_notes(vault_root, start_date, end_date)

    # Collect tag matches across all periodic notes
    all_done = []
    all_open = []
    all_bullets = []
    total_mentions = 0
    matched_tags = set()
    note_type_counts = {"daily": 0, "weekly": 0, "monthly": 0, "quarterly": 0}

    for note_type, files in periodic_notes.items():
        for f in files:
            done, open_t, bullets, mentions, tags_found = search_tag_in_file(f, topic_tags, prefix_tags)
            all_done.extend(done)
            all_open.extend(open_t)
            all_bullets.extend(bullets)
            total_mentions += mentions
            matched_tags.update(tags_found)
            if mentions > 0:
                note_type_counts[note_type] += 1

    # Find related projects
    related_projects = find_related_projects(vault_root, area_data, start_date, end_date)

    # Calculate daily note count for engagement ratio
    total_daily = len(periodic_notes["daily"])
    active_daily = note_type_counts["daily"]

    result = {
        "area": area_folder,
        "area_name": area_data["frontmatter"].get("area_name", area_folder)
        if area_data
        else area_folder,
        "period": period_label,
        "start_date": start_date.strftime("%Y-%m-%d"),
        "end_date": end_date.strftime("%Y-%m-%d"),
        "topic_tags": topic_tags,
        "prefix_tags_used": prefix_tags,
        "tags_actually_matched": sorted(matched_tags),
        "area_readme": {
            "maintenance_tasks": area_data["maintenance_tasks"] if area_data else {},
            "success_criteria": area_data["success_criteria"] if area_data else [],
            "metrics": area_data["metrics"] if area_data else [],
        },
        "statistics": {
            "total_done_tasks": len(all_done),
            "total_open_tasks": len(all_open),
            "total_bullets": len(all_bullets),
            "total_mentions": total_mentions,
            "active_daily_notes": active_daily,
            "total_daily_notes": total_daily,
            "engagement_ratio": round(active_daily / total_daily, 2) if total_daily > 0 else 0,
            "note_type_counts": note_type_counts,
        },
        "done_tasks_sample": all_done[:20],
        "open_tasks_sample": all_open[:20],
        "bullets_sample": all_bullets[:20],
        "related_projects": related_projects,
        "periodic_note_files": {
            "daily_count": len(periodic_notes["daily"]),
            "weekly_count": len(periodic_notes["weekly"]),
            "monthly_count": len(periodic_notes["monthly"]),
            "quarterly_count": len(periodic_notes["quarterly"]),
        },
    }

    return result


def list_active_areas(vault_root):
    """List all active areas in the vault."""
    areas_root = Path(vault_root) / "2.Areas"
    if not areas_root.exists():
        return []

    areas = []
    for readme in sorted(areas_root.glob("**/*.README.md")):
        try:
            content = readme.read_text(encoding="utf-8")
        except (UnicodeDecodeError, FileNotFoundError):
            continue

        # Check area-status (handle both area-status and area_status)
        status = "unknown"
        name = readme.stem.replace(".README", "")
        m = re.search(r"area[_-]status:\s*[\"']?(\w+)", content, re.IGNORECASE)
        if m:
            status = m.group(1)

        # Get area_name from frontmatter
        area_name = name
        m = re.search(r'area_name:\s*["\'](.+?)["\']', content)
        if m:
            area_name = m.group(1)

        # Get topic tags
        tags = []
        tag_section = False
        for line in content.split("\n"):
            if line.strip() == "tags:":
                tag_section = True
                continue
            if tag_section:
                if line.startswith("  - "):
                    tag = line.strip()[2:].strip()
                    if not tag.startswith("PARA/") and not tag.startswith("transfer/") and not tag.startswith("distillation/") and tag not in ("daily", "weekly", "monthly", "quarterly", "yearly", "resources"):
                        tags.append(tag)
                elif not line.startswith("  "):
                    break

        areas.append({
            "folder": name,
            "name": area_name,
            "status": status,
            "topic_tags": tags,
        })

    return areas


def main():
    parser = argparse.ArgumentParser(description="Collect area review data for LifeOS")
    parser.add_argument(
        "--area", required=True, help="Area folder name (e.g., personal-health) or 'all'"
    )
    parser.add_argument(
        "--period",
        default="current-quarter",
        help="Time period: current-quarter, last-quarter, current-month, YYYY-Qq, YYYY-MM, YYYY, or YYYY-MM-DD:YYYY-MM-DD",
    )
    parser.add_argument("--vault", default=None, help="Path to vault root (auto-detected)")
    parser.add_argument("--list-areas", action="store_true", help="List all active areas and exit")

    args = parser.parse_args()

    vault_root = find_vault_root(args.vault)

    if args.list_areas:
        areas = list_active_areas(vault_root)
        print(json.dumps(areas, ensure_ascii=False, indent=2))
        return

    if args.area == "all":
        areas = list_active_areas(vault_root)
        active_areas = [a for a in areas if a["status"] == "active"]
        results = []
        for area in active_areas:
            result = collect_area_review(vault_root, area["folder"], args.period)
            if result:
                results.append(result)
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        result = collect_area_review(vault_root, args.area, args.period)
        if result:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"错误: 无法收集领域 {args.area} 的数据", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()

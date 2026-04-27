# CLAUDE.md

Personal Knowledge Management system (LifeOS) built as an Obsidian vault. Implements PARA Method and CODE/CETDE workflow to create a "second brain."

**IMPORTANT**: This is NOT a software repository - it's an Obsidian vault (Markdown files) with no build, test, or deployment processes. Git-tracked for backup.

---

## Quick Start

### Daily Workflow

1. **Capture** in `9.Capture/` (quick notes, links, ideas)
2. **Encode** with frontmatter, tags, PARA classification
3. **Transfer** by adding 3-7 wiki-links to related notes

See @.claude/rules/cetde-workflow.md for complete 5-stage workflow.

### Task Syntax

```markdown
- [ ] Task description #project-name 📅 2026-01-20
```

**Task Management**:

- Create tasks in Daily Notes with project/area tags
- Tasks auto-aggregate via `TaskListByTag` query in project READMEs
- Track all tasks in `TASK.md` (central hub)

## Directory Structure

| Directory          | Purpose                                            |
| ------------------ | -------------------------------------------------- |
| `0.PeriodicNotes/` | Time-based (daily/weekly/monthly/quarterly/yearly) |
| `1.Projects/`      | Active projects with deadlines                     |
| `2.Areas/`         | Ongoing responsibilities                           |
| `3.Resources/`     | Knowledge collections by topic                     |
| `4.Archives/`      | Completed or inactive items                        |
| `5.Express/`       | Outgoing knowledge outputs                         |
| `6.Attachments/`   | Supporting files and media                         |
| `7.Excalidraws/`   | Visual diagrams and frameworks                     |
| `8.Templates/`     | Reusable note templates                            |
| `9.Capture/`       | Temporary holding for new info                     |
| `.claude/rules/`   | Detailed system rules                              |

## Periodic Notes Directory Structure

```text
0.PeriodicNotes/
└── {year}/                    # Year subdirectory (e.g., 2026/)
    ├── {year}.md              # Yearly note
    ├── Daily/                 # Daily notes (organized by month)
    │   └── {MM}/              # Month subdirectory (01-12)
    │       └── {yyyy-MM-dd}.md
    ├── Weekly/                # Weekly notes
    │   └── {yyyy-Www}.md      # ww = week number (01-53)
    ├── Monthly/               # Monthly notes
    │   └── {yyyy-MM}.md       # MM = month (01-12)
    └── Quarterly/             # Quarterly notes
        └── {yyyy-Qq}.md       # Qq = quarter (Q1-Q4)
```

**File Naming**:

- PARA Notes
  - Each folder has `{folder}.README.md` as metadata
  - Example: `1.Projects/work-devops-FY26Q1/work-devops-FY26Q1.README.md`

---

## Core Frameworks

### PARA (Organization by Actionability)

- **Projects**: Short-term, deadline-driven → `1.Projects/`
- **Areas**: Ongoing responsibilities → `2.Areas/`
- **Resources**: Future-use reference → `3.Resources/`
- **Archives**: Inactive items → `4.Archives/`

See @.claude/rules/para-method.md for complete guide.

### CETDE (Knowledge Processing)

Extended CODE workflow: **C**apture → **E**ncode → **T**ransfer → **D**istill → **E**xpress

See @.claude/rules/cetde-workflow.md for complete workflow.

### Integration

```
Capture → 9.Capture/
Organize (PARA) → 1-3. Projects/Areas/Resources
Distill → Progressive compression based on usage
Express → 5.Express/
Archive → 4.Archives/
```

**Key insight**: PARA implements CODE's "Organize" stage.

---

## Critical Rules

**IMPORTANT**:

- **ALWAYS** set the `para` property in note frontmatter
- **NEVER** create tasks without project/area tags (won't aggregate)
- **ALWAYS** use topic tags per @.claude/rules/tag-system.md (naming, hierarchy, placement)
- **ALWAYS** use 3-7 wiki-links when transferring knowledge
- **NEVER** commit sensitive information (API keys, credentials)
- **ALWAYS** use obsidian skills to edit notes, rather than manual editing.

**Avoid**: Over-classification, perfectionism, not archiving, premature distillation

---
## Two-Dimensional Planning

**Spatial (PARA)**: What information lives where

- Projects → Areas → Resources → Archives

**Temporal (Periodic Notes)**: When information is used

- Daily → Weekly → Monthly → Quarterly → Yearly

**Integration**: Daily notes focus on active projects, quarterly notes review area maintenance.

---

## Troubleshooting

**Tasks not aggregating in project README?**

- Check project README has `TaskListByTag` query block
- Verify tasks use correct topic tag (must match README `tags` or `aliases`); see @.claude/rules/tag-system.md
- Ensure tasks are in markdown format `- [ ]`

**Templates not expanding?**

- Verify Templater plugin is enabled
- Check template path in `8.Templates/`
- Test with simple template first

**Wiki-links broken?**

- Use exact note name (case-sensitive)
- Check file exists in correct PARA location
- Use spaces, not underscores, in `[[note name]]`

**Dataview queries not working?**

- Verify Dataview plugin is enabled
- Check query syntax matches LifeOS query language

---

## Summary

LifeOS implements Tiago Forte's "Building a Second Brain" methodology:

- **CETDE**: 5-stage knowledge processing (Capture → Encode → Transfer → Distill → Express)
- **PARA**: Organization by actionability (Projects/Areas/Resources/Archives)
- **Periodic Notes**: Time dimension for planning and review

**Goal**: Create an external cognitive system that enhances natural thinking processes.

**Remember**: Capture first, organize later. Organize by actionability, not topic. Link generously, express selectively.

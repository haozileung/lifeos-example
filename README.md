---
tags: []
---

# LifeOS

> Personal Knowledge Management system — an Obsidian vault implementing PARA Method and CETDE workflow to create a "second brain."

## Why LifeOS

The first brain is like a CPU — constantly switching between tasks, overwhelmed by context overload. LifeOS serves as the "second brain": an external storage system (memory + hard disk) that caches everything the first brain doesn't need to hold right now, allowing it to focus on the present moment.

You can call it a second brain, a "Programmable Personal Productivity System," or a "Monorepo Project" — each folder is a project, and each project's README describes its metadata like a `package.json`.

## Core Frameworks

### CETDE — 5-Stage Knowledge Processing

Extended from Tiago Forte's CODE model (Capture → Organize → Distill → Express), CETDE adds two intermediate stages for deeper knowledge integration:

| Stage | Directory | Purpose | DIKW Level |
|-------|-----------|---------|------------|
| **C**apture | `9.Capture/` | Externalize information quickly | Data |
| **E**ncode | PARA folders | Add structure & metadata (frontmatter, tags) | Information |
| **T**ransfer | Links created | Connect with 3-7 typed relationships | Knowledge |
| **D**istill | In-place | Progressive Summarization (5 layers) | Knowledge (refined) |
| **E**xpress | `5.Express/` | Share top 1% as outputs | Wisdom |

**Key insight**: CODE focuses on *what* to do; CETDE focuses on *how* to implement it in a PKM system.

### PARA — Organization by Actionability

Organize information by **actionability**, not by topic:

| Category | Directory | Definition | Key Attribute |
|----------|-----------|------------|---------------|
| **P**rojects | `1.Projects/` | Short-term efforts with outcomes & deadlines | Has a deadline |
| **A**reas | `2.Areas/` | Ongoing responsibilities to maintain | No end date |
| **R**esources | `3.Resources/` | Topics of interest for future reference | Not immediately actionable |
| **A**rchives | `4.Archives/` | Completed or inactive items | Preserved but dormant |

**Decision tree**: Actionable now + has deadline → Project. Actionable now + no deadline → Area. Not actionable + useful later → Resource. Not actionable + not useful → Archive.

### Two-Dimensional Planning

```
Spatial (PARA):   Projects → Areas → Resources → Archives
                      ↕
Temporal (Notes):  Daily → Weekly → Monthly → Quarterly → Yearly
```

- **Daily notes**: Focus on active project tasks
- **Weekly notes**: Review progress across projects
- **Quarterly notes**: Review area health, spawn new projects
- **Yearly notes**: Set vision, express achievements

## Directory Structure

| Directory | Purpose |
|-----------|---------|
| `0.PeriodicNotes/` | Time-based notes (daily/weekly/monthly/quarterly/yearly) |
| `1.Projects/` | Active projects with deadlines |
| `2.Areas/` | Ongoing responsibilities |
| `3.Resources/` | Knowledge collections by topic |
| `4.Archives/` | Completed or inactive items |
| `5.Express/` | Outgoing knowledge outputs |
| `6.Attachments/` | Supporting files and media |
| `7.Excalidraws/` | Visual diagrams and frameworks |
| `8.Templates/` | Reusable note templates |
| `9.Capture/` | Temporary holding for new info |

### Periodic Notes Structure

```
0.PeriodicNotes/
└── {year}/
    ├── {year}.md              # Yearly note
    ├── Daily/{MM}/{yyyy-MM-dd}.md
    ├── Weekly/{yyyy-Www}.md
    ├── Monthly/{yyyy-MM}.md
    └── Quarterly/{yyyy-Qq}.md
```

### PARA Note Structure

Each PARA item has a README as metadata:

```
1.Projects/project-alpha/
└── project-alpha.README.md    # project_name, status, due_date, queries
```

## Knowledge Processing

### Tag System

Tags are used **only** for topic aggregation (TaskListByTag / BulletListByTag / FileListByTag). Classification uses frontmatter properties.

**Topic tags** (in frontmatter + end of task lines):
- Format: `#work/project-alpha`, `#life/health`, `#candidate/jane-doe`
- Max 3 levels, lowercase, hyphens for multi-word

**Properties** (in frontmatter, NOT in tags field):

| Property | Values | Purpose |
|----------|--------|---------|
| `para` | `projects` / `areas` / `resources` / `archives` | PARA classification |
| `transfer` | `connected` / `integrated` / `applied` / `internalized` | Transfer stage |
| `distillation` | `layer2` / `layer3` / `layer4` / `layer5` | Distillation stage |
| `periodic_type` | `daily` / `weekly` / `monthly` / `quarterly` / `yearly` | Note type |

### Relationship Modeling

Typed relationships using Dataview inline fields (placed in `## 🔗 Relations` section):

```markdown
- Based on: [based_on:: [[Source Note]]]
- Extends: [extends:: [[Related Concept]]]
- Applies to: [applies_to:: [[Active Project]]]
```

6 core types: `based_on`, `extends`, `applies_to`, `contradicts`, `depends_on`, `part_of`

**Transfer: connected** = note has ≥3 typed relationships (auto-detectable).

### Progressive Summarization

Apply compression based on actual usage, NOT upfront:

| Layer | Action | Trigger |
|-------|--------|---------|
| 1 — Raw | Keep as captured | Initial capture |
| 2 — Bold | Bold key passages (20-30%) | First time you use it |
| 3 — Highlight | Highlight best parts (5-10%) | Second time you use it |
| 4 — Summary | Write executive summary | Third time you use it |
| 5 — Express | Transform into output | Fourth time you use it |

## Daily Workflow

1. **Capture** in `9.Capture/` or daily note — quick, no overthinking
2. **Encode** — add frontmatter (`para`, `tags`), move to PARA folder
3. **Transfer** — add 3-7 typed relationships in `## 🔗 Relations`
4. **Distill** — only when you actually use the information
5. **Express** — share top 1% in `5.Express/`

### Task Management

```markdown
- [ ] Task description #project-tag 📅 2026-01-20
```

- Create tasks in Daily Notes with project/area tags
- Tasks auto-aggregate via `TaskListByTag` queries in project READMEs
- Central task hub: `TASK.md`

## System Rules

- **ALWAYS** set the `para` property in note frontmatter
- **ALWAYS** add topic tags matching the project/area README
- **NEVER** create tasks without topic tags (won't aggregate)
- **ALWAYS** add 3-7 typed relationships when transferring
- **NEVER** distill upfront — wait until you actually use the information
- **NEVER** commit sensitive information

**Avoid**: Over-classification, perfectionism, not archiving, premature distillation

## References

- [Building a Second Brain](https://www.buildingasecondbrain.com/book) — Tiago Forte
- [PARA Method](https://fortelabs.com/blog/para/) — Tiago Forte

---

*Capture first, organize later. Organize by actionability, not topic. Link generously, express selectively.*

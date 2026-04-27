# PARA Method - Detailed Implementation Guide

## Overview

PARA (Projects-Areas-Resources-Archives) is an organizational system that categorizes information by actionability rather than topic. It's the implementation of CODE's "Organize" stage in the LifeOS system.

## The Four Categories

### 1.Projects (`1.Projects/`)

**Definition**: "A series of tasks with a specific goal and deadline"

**Characteristics**:
- Has a specific, measurable outcome
- Has a clear deadline or end date
- Can be marked as "complete"
- Drives current action and attention

**Examples**:
- Complete website redesign (due: 2026-03-31)
- Launch new product feature (due: 2026-02-28)
- Write quarterly report (due: 2026-04-15)

**Project lifecycle**:
1. **Create**: Define outcome, success criteria, due date
2. **Active**: Track tasks, time, progress in daily/weekly notes
3. **Complete**: Mark as complete, extract learnings
4. **Archive**: Move to `4.Archives/` with completion metadata

### 2.Areas (`2.Areas/`)

**Definition**: "A responsibility requiring ongoing maintenance"

**Characteristics**:
- Has a standard to be maintained
- No completion date (ongoing)
- Can have multiple projects within them
- Reviewed regularly for maintenance needs

**Examples**:
- Personal Health (standards: exercise 3x/week, sleep 7-8 hours)
- Team Management (standards: weekly 1:1s, quarterly reviews)
- Product Development (standards: agile process, quality metrics)

**Area maintenance**:
1. **Define**: Set standards and maintenance frequency
2. **Review**: Check area health regularly (quarterly review)
3. **Maintain**: Perform ongoing maintenance tasks
4. **Projects**: Spawn projects to improve areas when needed

### 3.Resources (`3.Resources/`)

**Definition**: "A topic of ongoing interest or collection of information"

**Characteristics**:
- Useful but not immediately actionable
- Reference materials for future use
- Can fuel both projects and areas
- Organized by topic, not actionability

**Examples**:
- Graphic design principles and examples
- Software architecture patterns
- Personal productivity techniques

**Resource management**:
1. **Collect**: Gather useful information and references
2. **Organize**: Structure by topic for easy retrieval
3. **Distill**: Apply Progressive Summarization based on usage
4. **Apply**: Use resources to support projects and areas

### 4.Archives (`4.Archives/`)

**Definition**: "Inactive items from the other three categories"

**Purpose**: Preserve value while reducing clutter

**What to archive**:
- Completed projects
- Dormant areas (no longer maintained)
- Outdated resources (but potentially useful later)

**When to archive**: When item is no longer active or relevant

**Archive strategy**:
1. **Trigger**: Project complete, area dormant, or resource outdated
2. **Metadata**: Add archive date, reason, original type
3. **Preserve**: Keep value while removing clutter from active view
4. **Retrieve**: Can be reactivated if needed later

## Decision Tree for Organizing

```
Is this item actionable RIGHT NOW?
↓ YES
Is there a specific deadline or completion?
  ↓ YES → → → → PROJECT
  ↓ NO → → → → AREA

Is this item actionable RIGHT NOW?
↓ NO
Is it potentially useful in the future?
  ↓ YES → → → → RESOURCE
  ↓ NO → → → → ARCHIVE (or discard)
```

## PARA Integration with LifeOS

### Directory Structure

```
1.Projects/
└── work-devops-FY26Q1/
    └── work-devops-FY26Q1.README.md
        - project_name: "DevOps FY26 Q1"
        - project-status: "active"
        - due_date: 2026-03-31
        - Contains: TaskListByTag query for all project tasks

2.Areas/
└── personal-health/
    └── personal-health.README.md
        - area_name: "Personal Health"
        - area-status: "active"
        - Contains: Maintenance standards and related projects

3.Resources/
└── pkm-knowledge-management/
    └── pkm-knowledge-management.README.md
        - resource_name: "PKM Resources"
        - resource-type: "topic"
        - Contains: Knowledge map and related notes

4.Archives/
└── completed-projects/
    └── work-devops-FY25Q4/
        └── work-devops-FY25Q4.README.md
            - archive_name: "DevOps FY25 Q4"
            - archive-date: 2026-01-01
            - archive-reason: "completed"
```

### Tagging System

**PARA classification** (stored as frontmatter property, not tag):
```yaml
para: projects       # or areas/resources/archives/capture/express
```

**Topic tags** (1-3 per note):
- `#work/devops` - Work-related DevOps topics
- `#personal/health` - Personal health and wellness
- `#productivity/pkm` - Productivity and PKM techniques

## Best Practices

### DO ✓

- Use actionability as primary organizing principle
- Move items between categories as their status changes
- Archive completed items promptly
- Review areas regularly for maintenance needs
- Link resources to active projects when applying them

### DON'T ✗

- Organize by topic only (school method)
- Keep completed items in active categories
- Neglect area maintenance until crisis
- Over-classify with too many subcategories
- Archive without metadata (date, reason, type)

## Common Scenarios

### Scenario 1: Meeting Notes

```
Is it actionable? YES (follow-up tasks)
Has deadline? YES → PROJECT

→ File in: 1.Projects/[project-name]/meeting-notes.md
→ Tag with: #project-name
→ Contains: Action items, decisions, attendees
```

### Scenario 2: Research Article

```
Is it actionable right now? NO (reference material)
Is it potentially useful? YES → RESOURCE

→ File in: 3.Resources/[topic]/[article-name].md
→ Tag with: #[topic]
→ Distill progressively based on usage
```

### Scenario 3: Health Goals

```
Is it actionable? YES (ongoing responsibility)
Has deadline? NO (ongoing) → AREA

→ File in: 2.Areas/personal-health/health-goals.md
→ Tag with: #personal-health
→ Review quarterly for maintenance
```

## PARA and Time-Based Planning

PARA works with periodic notes for two-dimensional planning:

- **PARA (Spatial)**: What information lives where
- **Periodic Notes (Temporal)**: When information is used

```
Spatial:  Projects → Areas → Resources → Archives
            ↓
Temporal:  Daily → Weekly → Monthly → Quarterly → Yearly
```

**Integration examples**:
- **Daily note**: Focus on active project tasks
- **Weekly note**: Review progress across all projects
- **Quarterly note**: Review area maintenance and spawn new projects
- **Yearly note**: Express achievements and set vision

## Summary

**Key principle**: Organize by **actionability**, not topic.

**PARA categories**:
- **Projects**: Short-term, deadline-driven
- **Areas**: Ongoing responsibilities
- **Resources**: Future-use reference materials
- **Archives**: Inactive but preserved items

**Benefit**: The right information at the right time increases productivity and reduces cognitive load.

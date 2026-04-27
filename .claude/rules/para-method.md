---
# Apply when editing notes in PARA + periodic + capture, or rule files
paths:
  - "0.PeriodicNotes/**/*.md"
  - "1.Projects/**/*.md"
  - "2.Areas/**/*.md"
  - "3.Resources/**/*.md"
  - "4.Archives/**/*.md"
  - "9.Capture/**/*.md"
  - ".claude/rules/**/*.md"
---

# PARA Method - Detailed Guide

PARA is the implementation of CODE's "Organize" stage. It provides the organizational structure for the entire LifeOS system.

## The Four Categories

### Projects (`1.Projects/`)

Short-term efforts with specific outcomes and deadlines.

- **Definition**: "A series of tasks with a specific goal and deadline"
- **Examples**: Complete website redesign, Launch new product, Write quarterly report
- **Key attributes**:
  - Has a specific, measurable outcome
  - Has a clear deadline or end date
  - Can be marked as "complete"
  - Drives current action and attention

### Areas (`2.Areas/`)

Ongoing responsibilities requiring maintenance over time.

- **Definition**: "A responsibility requiring ongoing maintenance"
- **Examples**: Health, Finances, Team Management, Product Development
- **Key attributes**:
  - Has a standard to be maintained
  - No completion date (ongoing)
  - Can have multiple projects within them
  - Reviewed regularly for maintenance needs

### Resources (`3.Resources/`)

Topics of ongoing interest and reference materials.

- **Definition**: "A topic of ongoing interest or collection of information"
- **Examples**: Graphic design, Personal productivity, Software architecture
- **Key attributes**:
  - Useful but not immediately actionable
  - Reference materials for future use
  - Can fuel both projects and areas
  - Organized by topic, not actionability

### Archives (`4.Archives/`)

Completed or inactive items.

- **Definition**: "Inactive items from the other three categories"
- **Purpose**: Preserve value while reducing clutter
- **What to archive**:
  - Completed projects
  - Dormant areas (no longer maintained)
  - Outdated resources (but potentially useful later)
- **When to archive**: When item is no longer active or relevant

## Key Principle: Organize by Actionability

**NOT by topic** (school method): Marketing, Psychology, Business
**BY actionability** (PARA method): What are you trying to accomplish right now?

### Decision Tree for Organizing

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

## PARA in Practice

### Project Lifecycle

1. **Create**: Define outcome, success criteria, due date
2. **Active**: Track tasks, time, progress in daily/weekly notes
3. **Complete**: Mark as complete, extract learnings
4. **Archive**: Move to `4.Archives/` with completion metadata

### Area Maintenance

1. **Define**: Set standards and maintenance frequency
2. **Review**: Check area health regularly (quarterly review)
3. **Maintain**: Perform ongoing maintenance tasks
4. **Projects**: Spawn projects to improve areas when needed

### Resource Management

1. **Collect**: Gather useful information and references
2. **Organize**: Structure by topic for easy retrieval
3. **Distill**: Apply Progressive Summarization based on usage
4. **Apply**: Use resources to support projects and areas

### Archive Strategy

1. **Trigger**: Project complete, area dormant, or resource outdated
2. **Metadata**: Add archive date, reason, original type
3. **Preserve**: Keep value while removing clutter from active view
4. **Retrieve**: Can be reactivated if needed later

## PARA Integration with CODE

PARA is not separate from CODE - it **is** the implementation of CODE's "Organize" stage:

```
CODE Stage          PARA Implementation
─────────────────────────────────────────
Capture    →        9.Capture/ (temporary)
Organize   →        PARA (Projects/Areas/Resources)
Distill    →        Applied throughout PARA
Express    →        5.Express/
Archives   →        4.Archives/
```

**Key insight**: Organize by actionability (PARA), not by topic.

## PARA File Structure

Each PARA category uses README files as metadata:

```
1.Projects/
└── project-alpha/
    └── project-alpha.README.md
        - project_name: "Project Alpha"
        - project-status: "active"
        - due_date: 2026-06-30
        - Contains: TaskListByTag query for all project tasks

2.Areas/
└── area-wellness/
    └── area-wellness.README.md
        - area_name: "Wellness"
        - area-status: "active"
        - Contains: Maintenance standards and related projects

3.Resources/
└── resource-topic-x/
    └── resource-topic-x.README.md
        - resource_name: "Topic X Resources"
        - resource-type: "topic"
        - Contains: Knowledge map and related notes

4.Archives/
└── completed-projects/
    └── project-beta/
        └── project-beta.README.md
            - archive_name: "Project Beta"
            - archive-date: 2026-01-15
            - archive-reason: "completed"
```

## PARA Best Practices

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

## PARA Decision Examples

### Example 1: Meeting Notes

```
Is it actionable? YES (follow-up tasks)
Has deadline? YES → PROJECT

→ File in: 1.Projects/project-alpha/meeting-notes.md
→ Tag with: #work/project-alpha
→ Contains: Action items, decisions, attendees
```

### Example 2: Reference Article

```
Is it actionable right now? NO (reference material)
Is it potentially useful? YES → RESOURCE

→ File in: 3.Resources/topic-x/[article-name].md
→ Tag with: #topic-x
→ Distill progressively based on usage
```

### Example 3: Area Goals

```
Is it actionable? YES (ongoing responsibility)
Has deadline? NO (ongoing) → AREA

→ File in: 2.Areas/area-wellness/area-goals.md
→ Tag with: #area-wellness
→ Review quarterly for maintenance
```

### Example 4: Completed Project

```
Project marked complete?
Archive to preserve learning

→ Move to: 4.Archives/completed-projects/project-beta/
→ Add metadata: archive-date, archive-reason
→ Extract learnings to resources if applicable
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

Example:

- **Daily note**: Focus on active project tasks
- **Weekly note**: Review progress across all projects
- **Quarterly note**: Review area maintenance and spawn new projects
- **Yearly note**: Express achievements and set vision

## Summary

**PARA Method**:

- Organize by **actionability**, not topic
- **Projects**: Short-term, deadline-driven
- **Areas**: Ongoing responsibilities
- **Resources**: Future-use reference materials
- **Archives**: Inactive but preserved items

**Key Principle**: The right information at the right time increases productivity.

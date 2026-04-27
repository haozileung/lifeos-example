# Obsidian Best Practices for LifeOS

## Overview

This guide covers Obsidian-specific optimizations for implementing LifeOS effectively. Focus on features and workflows that enhance the PARA method and CETDE workflow.

## Core Obsidian Features for LifeOS

### 1. Frontmatter (YAML Metadata)

**Purpose**: Add structured metadata to notes

**LifeOS frontmatter template**:
```yaml
---
title: "Note Title"
created: 2026-02-10
updated: 2026-02-15
para: projects       # or areas/resources/archives/capture/express
tags:
  - work/devops      # 1-3 topic tags
  - automation
aliases:
  - alternative-name
  - related-concept
status: "active"     # active, completed, archived
due_date: 2026-03-31 # for projects
---
```

**Recommended plugins**:
- **Templater**: For dynamic template insertion
- **QuickAdd**: For fast note creation with templates
- **Dataview**: For querying frontmatter

### 2. Wiki-Links (Internal Links)

**Purpose**: Create bidirectional connections between notes

**Basic syntax**:
```markdown
[[Note Name]]
[[Note Name|Display Text]]
[[Note Name#Heading]]
[[Note Name#^block-id]]
```

**LifeOS linking patterns**:
```markdown
## Related Projects
- [[Active Project Name]] for implementation
- [[Completed Project|lessons learned]]

## Connected Areas
- [[Personal Health]] standards apply
- [[Team Management]] processes

## Reference Resources
- [[PKM Resources]] for methodology
- [[DevOps Tools]] for technical context
```

**Best practices**:
- Create 3-7 wiki-links per note
- Use descriptive display text
- Link to headings for specific sections
- Create backlinks naturally

### 3. Tags and Tag Hierarchy

**Purpose**: Categorize and filter notes

**LifeOS PARA classification** (stored as frontmatter property, not tag):
```yaml
para: projects       # or areas/resources/archives/capture/express
```

**LifeOS topic tag structure**:
```
#work/             # Work-related topics
  #work/devops
  #work/development
  #work/management

#personal/         # Personal topics
  #personal/health
  #personal/finance
  #personal/learning

#productivity/     # Productivity topics
  #productivity/pkm
  #productivity/time-management
```

**Tagging guidelines**:
- Use 1-3 topic tags per note
- Maintain consistent hierarchy
- Avoid over-tagging
- Use nested tags for organization

### 4. Callouts for Structure

**Purpose**: Visually distinguish different content types

**LifeOS callout patterns**:
```markdown
> [!summary]
> Executive summary of key insights

> [!todo]
> Action items and next steps
> - [ ] Task 1
> - [ ] Task 2

> [!note]
> Important information to remember

> [!tip]
> Helpful suggestion or best practice

> [!warning]
> Potential issue or caution

> [!quote]
> Important quote or excerpt
```

### 5. Dataview Queries

**Purpose**: Dynamic aggregation and filtering

**LifeOS query examples**:

**Project task aggregation**:
````markdown
```dataview
TASK
FROM #work-devops-FY26Q1
WHERE !completed
GROUP BY file.link
```
````

**Note listing by property**:
````markdown
```dataview
LIST
FROM "" WHERE para = "projects"
WHERE status = "active"
SORT due_date ASC
```
````

**Weekly review query**:
````markdown
```dataview
TABLE created, status, due_date
FROM "" WHERE para = "projects"
WHERE status = "active"
SORT due_date ASC
```
````

## Recommended Plugins

### Essential for LifeOS

1. **Templater**
   - Dynamic template insertion
   - JavaScript functions in templates
   - Auto-trigger on file creation

2. **Dataview**
   - Query language for notes
   - Dynamic task aggregation
   - Frontmatter-based filtering

3. **Periodic Notes**
   - Daily/weekly/monthly notes
   - PARA-integrated directory structure
   - Time-based organization

4. **Tasks**
   - Task management with tags
   - Due dates and priorities
   - Recurring tasks

5. **QuickAdd**
   - Fast note creation
   - Template-based capture
   - Workflow automation

### Optional Enhancements

6. **Calendar**
   - Visual date navigation
   - Daily note integration
   - Event tracking

7. **Kanban**
   - Visual project boards
   - Task status tracking
   - Drag-and-drop organization

8. **Excalidraw**
   - Visual diagrams
   - Mind maps and frameworks
   - Hand-drawn notes

9. **Outliner**
   - Better list management
   - Drag-and-drop reorganization
   - Keyboard shortcuts

## Workflow Optimizations

### Daily Workflow

**Morning setup**:
1. Open today's daily note (Cmd/Ctrl + D)
2. Review `LifeOS.Project.snapshot()` for active projects
3. Set priorities using PARA framework
4. Capture new ideas in dedicated section

**Throughout day**:
1. Capture ideas in daily note or `9.Capture/`
2. Use QuickAdd for fast note creation
3. Add wiki-links to connect ideas
4. Add `para:` property for PARA classification

**Evening review**:
1. Process captures through encoding
2. Move notes to appropriate PARA locations
3. Update task statuses
4. Plan tomorrow's priorities

### Weekly Review

**PARA review process**:
1. **Projects**: Check progress, update tasks, adjust deadlines
2. **Areas**: Review maintenance, identify improvement projects
3. **Resources**: Distill frequently used resources
4. **Archives**: Move completed items, review for reactivation

**Dataview queries for weekly review**:
````markdown
## Active Projects
```dataview
TABLE due_date, status
FROM "" WHERE para = "projects"
WHERE status = "active"
SORT due_date ASC
```

## Overdue Tasks
```dataview
TASK
FROM "" WHERE para = "projects"
WHERE !completed AND due < date(today)
GROUP BY file.link
```

## Area Maintenance
```dataview
LIST
FROM "" WHERE para = "areas"
WHERE status = "active"
```
````

### Note Creation Workflow

**Option 1: QuickAdd capture**
1. Assign hotkey to QuickAdd capture
2. Use template with frontmatter
3. Auto-file to appropriate PARA location

**Option 2: Daily note capture**
1. Capture in daily note throughout day
2. Evening: Process and encode captures
3. Move to PARA locations with metadata

**Option 3: Direct creation**
1. Create note in target PARA location
2. Apply template with frontmatter
3. Add wiki-links and tags immediately

## Performance Tips

### Vault Organization

**Directory structure**:
```
LifeOS/
├── 0.PeriodicNotes/
├── 1.Projects/
├── 2.Areas/
├── 3.Resources/
├── 4.Archives/
├── 5.Express/
├── 6.Attachments/
├── 7.Excalidraws/
├── 8.Templates/
└── 9.Capture/
```

**File naming**:
- Use descriptive names with spaces
- Include dates where relevant: `2026-02-10 Meeting Notes.md`
- Project notes: `project-name/note-purpose.md`
- Avoid special characters except hyphens and underscores

### Search Optimization

**Effective search patterns**:
```
# Search by frontmatter property
[para:projects]

# Search by frontmatter
status:active

# Search linked notes
[[Note Name]]

# Search task status
- [ ] incomplete
- [x] completed
```

**Saved searches**:
- `[para:projects] status:active`
- `- [ ]` (all incomplete tasks)
- `path:"9.Capture/"` (unprocessed captures)

### Plugin Configuration

**Templater settings**:
- Template folder: `8.Templates/`
- Trigger on file creation
- Use JavaScript functions for dynamic content

**Dataview settings**:
- Enable inline queries
- Set default result limit
- Configure date formats

**Tasks settings**:
- Use `#tags` for project association
- Set due date format: `📅 YYYY-MM-DD`
- Enable recurrence patterns

## Troubleshooting

### Common Issues

**Problem**: Templates not expanding
**Solution**: Check Templater plugin is enabled, verify template folder path

**Problem**: Dataview queries not working
**Solution**: Ensure frontmatter format is correct, check query syntax

**Problem**: Wiki-links broken (red)
**Solution**: Check file exists, verify exact name match, use spaces not underscores

**Problem**: Performance slow with many notes
**Solution**: Exclude large directories from search, use `.obsidianignore` file

**Problem**: Sync conflicts between devices
**Solution**: Use git for version control, resolve conflicts carefully

### Quality Checks

**Note quality checklist**:
- [ ] Has descriptive title
- [ ] Includes frontmatter with `para:` property and topic tags
- [ ] Contains 3-7 wiki-links
- [ ] Uses proper heading hierarchy
- [ ] Applies progressive summarization
- [ ] Located in correct PARA directory
- [ ] Connected to active projects/areas

**Vault health indicators**:
- Low number of orphan notes (no links)
- High link density (3-7 links per note)
- Consistent tagging hierarchy
- Regular archival of completed items
- Progressive summarization applied

## Summary

**Obsidian + LifeOS integration**:
- **Frontmatter** for structured metadata
- **Wiki-links** for knowledge connections
- **Properties** (`para:`, `transfer:`, `distillation:`) for classification and workflow state
- **Dataview** for dynamic aggregation
- **Templates** for consistent note creation

**Key plugins**: Templater, Dataview, Periodic Notes, Tasks, QuickAdd

**Workflow**: Daily capture → PARA organization → CETDE processing → Regular review

**Goal**: Create a connected, actionable knowledge system that enhances productivity and reduces cognitive load.

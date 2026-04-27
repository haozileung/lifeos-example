---
# Apply when editing templates or rule files that reference templates
paths:
  - "8.Templates/**/*.md"
  - ".claude/rules/**/*.md"
---

# Template System

Templates in this directory use Obsidian Templater syntax (`<% tp.* %>`).

## Template Functions

- **Date insertion**: `<% tp.date.now() %>` - Inserts current date/time
- **Custom LifeOS object**:
  - `LifeOS.Project.snapshot()` - Dynamic project list with time allocation
  - `LifeOS.Area.snapshot()` - Area status snapshots
- **Auto-trigger**: Templates can auto-trigger on file creation

## Key Templates

### Periodic Note Templates

#### Daily.md

- Project snapshot via `LifeOS.Project.snapshot()`
- Time tracking sections
- Task completion tracking with `TaskDoneListByTime`
- Habit checklists
- Two-dimensional organization (projects + execution focus)

#### Weekly.md

- Weekly priorities
- `ProjectListByTime` query
- Role focus sections
- Week-in-review prompts

#### Monthly.md

- Monthly goals
- Role-based task breakdown
- `ProjectListByTime` query
- Month-in-review structure

#### Quarterly.md

- `Area.snapshot()` for area-level review
- Quarterly goals
- Role-based quarterly goals
- Area maintenance checklists

#### Yearly.md

- Annual vision and themes
- `AreaListByTime` query
- Role-based annual goals
- Year-in-review framework

### PARA Templates

#### Project.md

- Project definition sections (outcome, success criteria, due date)
- `TaskListByTag` for automatic task aggregation
- `BulletListByTag` for idea collection
- `FileListByTag` for related files
- Project review checklist

#### Area.md

- Area standards definition
- Maintenance tracking sections
- Related Projects aggregation
- Responsibility boundaries

#### Resource.md

- Topic structure and taxonomy
- Knowledge mapping sections
- Related notes and resources
- Distillation tracking

#### Archive.md

- Completion metadata
- Original location tracking
- Reason for archiving
- Retrieval triggers

## Template Editing Best Practices

When editing templates:

1. **Preserve Templater syntax**: Don't break `<% tp.* %>` expressions
2. **Maintain query blocks**: Keep `` ```LifeOS` `` blocks intact
3. **Test changes**: Create test notes to verify template functionality
4. **Document changes**: Update this file if you add new template functions
5. **Use consistent formatting**: Match existing structure for easier maintenance

## Common Template Patterns

### Frontmatter Pattern

```yaml
---
tags:
  - <% tp.system.prompt("Tags (comma-separated)") %>
aliases:
  - <% tp.system.prompt("Aliases (comma-separated)") %>
created: <% tp.date.now("YYYY-MM-DD") %>
---
```

### Query Block Pattern

````markdown
```LifeOS
ProjectListByTime
```
````

### Dynamic Date Pattern

- Current date: `<% tp.date.now("YYYY-MM-DD") %>`
- Week number: `<% tp.date.now("yyyy-Www") %>`
- Month: `<% tp.date.now("yyyy-MM") %>`
- Quarter: `<% tp.date.now("yyyy-Qq") %>`

### Link Pattern

```markdown
<% tp.file.cursor() %> # Cursor position when template expands
[[<% tp.system.prompt("Link to note") %>]]
```

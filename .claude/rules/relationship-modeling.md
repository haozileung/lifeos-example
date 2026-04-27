---
# Apply when creating or editing notes in PARA dirs; applies to new notes only
paths:
  - "1.Projects/**/*.md"
  - "2.Areas/**/*.md"
  - "3.Resources/**/*.md"
  - "4.Archives/**/*.md"
---

# Relationship Modeling Rules

Typed relationships between notes using Dataview inline fields. This extends the CETDE Transfer stage with queryable, attributed links.

## 0. Design Principles

- **Progressive enhancement**: Only applies to new notes; existing notes remain unchanged.
- **Human + machine readable**: Chinese label + Dataview inline field format.
- **Minimal type set**: 8 types cover 80% of use cases.
- **Backward compatible**: Plain `[[wikilink]]` still valid but does not count toward `transfer: connected`.

## 1. Relationship Types

### Core Types (6)

| Inline Field | Chinese Label | Meaning | Direction | Typical Use |
|---|---|---|---|---|
| `based_on` | 基于 | Based on / references | → source knowledge | Resource built on [[X]] |
| `extends` | 延伸 | Extends / develops | → concept evolution | Extends thinking in [[Y]] |
| `applies_to` | 应用于 | Applied to | → practice | Method applied in [[Project Z]] |
| `contradicts` | 矛盾 | Contradicts | → critical thinking | Contradicts conclusion in [[W]] |
| `depends_on` | 依赖 | Depends on / prerequisite | → blocking | Project A depends on [[Project B]] |
| `part_of` | 属于 | Part of / subordinated to | → hierarchy | Sub-project of [[Main Project]] |

### Extended Types (2, use as needed)

| Inline Field | Chinese Label | Meaning | Typical Use |
|---|---|---|---|
| `supersedes` | 取代 | Replaces / upgrades | New approach replaces [[old approach]] |
| `alternative_to` | 替代 | Alternative to | A is an alternative to [[B]] |

## 2. Syntax

### Inline Field Format

```markdown
- 基于：[based_on:: [[Note Name]]]
- 延伸：[extends:: [[Note Name]]]
- 应用于：[applies_to:: [[Note Name]]]
```

**Rules**:
- Each relationship type can appear multiple times: `[depends_on:: [[X]]] [depends_on:: [[Y]]]`
- Always use Chinese label prefix for readability
- Target must be a valid wikilink `[[...]]` (for graph view and backlinks)
- Place all relationships in the `## 🔗 Relations` section

### Note Structure (New Notes)

```markdown
---
para: resources
tags:
  - topic/tag-name
---
# Note Title

(content...)

## 🔗 Relations

- 基于：[based_on:: [[Source Note]]]
- 延伸：[extends:: [[Related Concept]]]
- 应用于：[applies_to:: [[Active Project]]]

## 📋 Task
(LifeOS queries...)

## 💡 Bullet
(LifeOS queries...)

## 📂 File
(LifeOS queries...)
```

## 3. PARA-Specific Defaults

### Resource Notes (3.Resources/)

Default relationship types to consider:

```markdown
## 🔗 Relations
- 基于：[based_on:: ]
- 延伸：[extends:: ]
- 应用于：[applies_to:: ]
- 矛盾：[contradicts:: ]
```

### Project Notes (1.Projects/)

Default relationship types to consider:

```markdown
## 🔗 Relations
- 依赖：[depends_on:: ]
- 属于：[part_of:: ]
- 取代：[supersedes:: ]
- 应用于：[applies_to:: ]
```

### Area Notes (2.Areas/)

Default relationship types to consider:

```markdown
## 🔗 Relations
- 应用于：[applies_to:: ]
- 属于：[part_of:: ]
```

### Archive Notes (4.Archives/)

No new relationships needed; preserve existing ones from original note.

## 4. Query Patterns

### Forward Query: What does this note relate to?

```dataview
TABLE based_on AS "基于", extends AS "延伸", applies_to AS "应用于",
      depends_on AS "依赖", contradicts AS "矛盾", part_of AS "属于"
FROM ""
WHERE based_on OR extends OR applies_to OR depends_on OR contradicts OR part_of
```

### Reverse Query: What relates to this note?

```dataview
LIST
FROM ""
WHERE contains(based_on, [[this.file.name]])
   OR contains(extends, [[this.file.name]])
   OR contains(applies_to, [[this.file.name]])
   OR contains(depends_on, [[this.file.name]])
   OR contains(contradicts, [[this.file.name]])
   OR contains(part_of, [[this.file.name]])
```

### Project Dependency Chain

```dataview
TABLE depends_on AS "依赖", part_of AS "属于"
FROM "1.Projects"
WHERE depends_on OR part_of
SORT file.name ASC
```

### Knowledge Evolution Map

```dataview
TABLE extends AS "延伸了", based_on AS "基于", contradicts AS "与...矛盾"
FROM "3.Resources"
WHERE extends OR based_on OR contradicts
SORT file.name ASC
```

## 5. Integration with CETDE Transfer

### Transfer Stage Update

When processing a note through CETDE Transfer:

1. **Create 3-7 typed relationships** instead of plain wikilinks
2. Ask: "What is the relationship between this note and the target?"
3. Choose from the 6 core types (or 2 extended types)
4. Place in `## 🔗 Relations` section with Chinese label

### transfer: connected Detection (Updated)

| Property | Condition | Detection |
|---|---|---|
| `connected` | Note contains ≥3 typed relationship inline fields `[xxx:: [[...]]]` | Auto-detectable |

**Note**: Plain `[[wikilink]]` in body text no longer counts toward `transfer: connected`. This incentivizes typed relationships while keeping plain links valid for casual reference.

## 6. Compatibility

| Existing Mechanism | Affected? | Notes |
|---|---|---|
| `TABLE join(file.outlinks)` | ✅ Compatible | Wikilinks inside inline fields still count as outlinks |
| `TaskListByTag` / `BulletListByTag` / `FileListByTag` | ✅ Compatible | Tag system unchanged |
| Plain `[[wikilink]]` in body | ✅ Preserved | Still valid for casual references |
| Graph View | ✅ Compatible | Relationships contribute to graph edges |
| `transfer: connected` | ⚠️ Updated | Detection logic changed (see Section 5) |

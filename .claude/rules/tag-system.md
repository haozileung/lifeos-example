---
# Apply in core LifeOS dirs only (excl. 6.Attachments, 7.Excalidraws); incl. rule files
paths:
  - "0.PeriodicNotes/**/*.md"
  - "1.Projects/**/*.md"
  - "2.Areas/**/*.md"
  - "3.Resources/**/*.md"
  - "4.Archives/**/*.md"
  - "5.Express/**/*.md"
  - "8.Templates/**/*.md"
  - "9.Capture/**/*.md"
  - ".claude/rules/**/*.md"
---

# Tag System Rules

**Scope**: Applied when editing files under the `paths` above (core dirs 0–5, 8, 9 and `.claude/rules/`). Not applied under `6.Attachments/`, `7.Excalidraws/`, or ad-hoc locations.

In LifeOS, **tags** are used exclusively for **topic aggregation** (TaskListByTag / BulletListByTag / FileListByTag). Classification metadata (PARA, workflow state, periodic type) is stored as **frontmatter properties**. This rule defines naming, hierarchy, placement, and the property system.

## 0. Frontmatter Properties (Metadata)

These properties replace the old PARA/workflow/periodic tags. They are set in frontmatter, never in the `tags` field.

| Property | Type | Values | Required | Purpose |
|----------|------|--------|----------|---------|
| `para` | string | `projects`, `areas`, `resources`, `archives`, `capture`, `express` | Yes (for PARA notes) | PARA classification |
| `transfer` | string | `connected`, `integrated`, `applied`, `internalized` | No | CETDE Transfer stage |
| `distillation` | string | `layer2`, `layer3`, `layer4`, `layer5` | No | CETDE Distillation stage |
| `periodic_type` | string | `daily`, `weekly`, `monthly`, `quarterly`, `yearly` | No (periodic notes only) | Periodic note type |

### Property assignment rules

**`para`**: Set based on which directory the note lives in (`1.Projects/` → `projects`, etc.).

**`transfer`**:

| 值 | 赋值条件 | 自动/手动 |
|----|----------|-----------|
| `connected` | 笔记中包含 ≥3 个类型化关联 `[xxx:: [[...]]]`（Dataview 内联字段，如 `[based_on:: [[Note]]]`） | 可自动检测 |
| `integrated` | 有明确的应用计划段落 | 需人工判断 |
| `applied` | 被其他项目/笔记引用并实际使用 | 需人工判断 |
| `internalized` | 可不经检索自动回忆 | 需人工判断 |

**注意**: 普通 `[[wikilink]]` 不再计入 `transfer: connected` 检测。只有 Dataview 内联字段格式的关系才计入。详见 @.claude/rules/relationship-modeling.md。

**`distillation`**:

| 值 | 赋值条件 | 检测方式 |
|----|----------|----------|
| `layer2` | 正文中有 ≥3 处有意义的粗体 `**...**` | 排除 frontmatter 和 `#` 标题行后统计 |
| `layer3` | 正文中有 ≥1 处高亮 `==...==` | 任意高亮文本即满足 |
| `layer4` | 笔记顶部有摘要/总结段落 | frontmatter 后、第一个 `##` 前，含关键词（摘要、总结、summary、概要、核心、要点、概述） |
| `layer5` | 内容已转化为 `5.Express/` 中的输出 | 需人工判断 |

**关键规则**:
- **只标记最高 distillation 层级**：同时满足多个层级时，只标记最高的那个
- **Transfer 和 Distillation 属性可共存**
- **排除格式性粗体**：`#` 标题行、frontmatter 中的粗体不计入 layer2 判定
- 仅 `transfer: connected` 可自动检测，其余 transfer 值和 `distillation: layer5` 需人工判断

## 1. Tag Types and Uses

Tags are used **only** for topic aggregation and entity context. Classification metadata uses properties (see Section 0).

| Type | Purpose | Examples | Where to put |
|------|---------|----------|-------------|
| **Topic** | Aggregate tasks, bullets, and files to a theme/project/area | `#work/project-alpha`, `#work/ops/hiring-pilot`, `#life/personal` | Frontmatter + end of task/bullet lines in body |
| **Entity/context** | People, candidates, situations | `#candidate/jane-doe` | End of line in body (use with topic tags) |

**Key**: The topic tag is the unique identifier for a "topic note". TaskListByTag / BulletListByTag / FileListByTag only aggregate correctly when the tag matches the project/area README `tags` or `aliases`.

## 2. Naming and Format

### 2.1 General rules

- **Hierarchy**: At most three levels, separated by `/`.
  - OK: `#work/project-alpha`, `#work/ops/hiring-pilot`
  - Avoid: `#work/team/a/b/c`
- **Characters**: Lowercase letters, digits, hyphens; use hyphens for multiple words, no spaces.
  - Correct: `#work/initiative-gamma`
  - Wrong: `#work/initiative gamma`
- **Semantics**: Use nouns or noun phrases; avoid verbs or full sentences.

### 2.2 Topic tag prefix conventions

| Prefix | Meaning | Examples |
|--------|---------|----------|
| `#work/` | Work projects, areas, meetings | `#work/project-alpha`, `#work/team-beta`, `#work/ops` |
| `#work/area/subitem` | Work sub-projects or sub-areas | `#work/ops/migration-x`, `#work/ops/hiring-pilot` |
| `#life/` | Life, personal | `#life/personal` |
| `#candidate/` | Candidates/people (with project) | `#candidate/jane-doe` (use with `#work/ops/hiring-pilot`) |

Project or area README `tags` should include the **topic tag** (or expose it via `aliases`) so LifeOS queries can aggregate by "current file's tags".

## 3. Placement Rules

### 3.1 Note frontmatter

- **Required**: PARA notes (project/area/resource/archive) must have a **`para`** property and at least one **topic tag** in `tags`.
- **Recommended**: When encoding, use `para` property + 1–3 topic/area tags.

```yaml
---
para: projects
tags:
  - work/ops/hiring-pilot
---
```

### 3.2 Tasks and bullets (Daily/Weekly and other periodic notes)

- **Required**: Every task or bullet line must end with at least one **topic tag** that exists in some project/area README `tags` (or `aliases`), or it will not be aggregated by TaskListByTag / BulletListByTag.
- Multiple tags per line are allowed, e.g. `#work/project-alpha #work/team-beta`, `#work/ops/hiring-pilot #candidate/jane-doe`.

```markdown
- [ ] 08:30 Project A standup #work/project-alpha
- Interview conclusion: prefer Jane #work/ops/hiring-pilot #candidate/jane-doe
```

### 3.3 Non-periodic notes (project docs, resources, etc.)

- Add the **topic tag** in frontmatter `tags` and set the `para` property for FileListByTag and search.

## 4. Coordination with PARA and topic notes

- **Topic notes** (project/area READMEs): Identified by their **topic tag**; the tag in their `tags` (or `aliases`) is "that topic's ID".
- **TaskListByTag / BulletListByTag / FileListByTag**: Read the **current note's** frontmatter `tags` and find tasks, bullets, and files with the same tag across the vault. So:
  - Project/area README `tags` must include the topic tag (e.g. `work/ops/hiring-pilot`).
  - Tasks/bullets in Daily notes must use that same topic tag at the end of the line.

See @.claude/rules/para-method.md and @.claude/rules/cetde-workflow.md for details.

## 5. Rule summary

1. **New or updated PARA notes**: Frontmatter must have a `para` property and at least one topic tag (matching the README).
2. **Tasks or bullets in Daily/Weekly**: End of line must have at least one topic tag that exists in the corresponding project/area README tags or aliases.
3. **Tag format**: Lowercase, at most three levels with `/`, hyphenate multi-word tags; do not invent new topic tags that don't match an existing README unless you create or update the topic note.
4. **Properties, not tags**: PARA classification, CETDE workflow state, and periodic note type are stored as frontmatter properties (`para`, `transfer`, `distillation`, `periodic_type`), never in the `tags` field.

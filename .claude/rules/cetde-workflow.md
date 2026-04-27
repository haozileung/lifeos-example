---
# Apply when editing content in core LifeOS dirs (excl. 6.Attachments, 7.Excalidraws) or rule files
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

# CETDE Workflow - Extended CODE Implementation

CETDE is LifeOS's extended implementation of the CODE framework, adding two intermediate stages for deeper knowledge integration.

## How CETDE Extends CODE

```text
CODE (4 stages):   Capture → Organize → Distill → Express

CETDE (5 stages):  Capture → Encode → Transfer → Distill → Express
                              ↑         ↑
                           NEW stages added
```

**Why extend CODE?** CODE focuses on **what** to do with information, while CETDE focuses on **how** to implement it in a PKM system.

## The Five Stages

### 1. CAPTURE (`9.Capture/`)

Collect raw data/information quickly.

- **Purpose**: Reduce cognitive load by externalizing information
- **Practice**: Fast recording without overthinking, use any available tool
- **Location**: `9.Capture/` or daily notes
- **Key principle**: Capture first, organize later

**What to capture**:

- Article links and web clips
- Meeting notes and conversations
- Ideas and insights
- Tasks and reminders
- Quotes and excerpts

**Don't worry about**:

- Perfect organization
- Correct categorization
- Proper tagging
- Complete information

### 2. ENCODE (EXTENDS CODE)

Transform data into structured information.

**Splits CODE's "Organize" into two phases**

Encode makes information queryable and retrievable by adding structure:

#### What Encoding Includes

1. **Frontmatter metadata**:

   ```yaml
   ---
   para: resources
   tags:
     - work/project-alpha
   created: 2026-01-15
   ---
   ```

2. **PARA classification**: Set `para` property
   - `para: projects` for active projects
   - `para: areas` for ongoing responsibilities
   - `para: resources` for reference materials
   - `para: archives` for completed items

3. **Topic tags**: Add 1-3 topic tags
   - Example: `#work/project-alpha`, `#life/productivity`
   - Use existing tag taxonomy when possible

4. **File organization**: Move to appropriate PARA location
   - Projects → `1.Projects/`
   - Areas → `2.Areas/`
   - Resources → `3.Resources/`

**Result**: Data transforms into Information (findable and retrievable)

### 3. TRANSFER (EXTENDS CODE)

Integrate knowledge through connections.

**Emphasizes knowledge integration** (missing in CODE)

Transfer transforms information into understanding by creating connections:

#### What Transfer Includes

1. **Create 3-7 typed relationships** to existing knowledge
   - Use Dataview inline fields with relationship types: `- 基于：[based_on:: [[Note]]]`
   - Ask: "What is the relationship between this note and the target?"
   - Choose from core types: `based_on`, `extends`, `applies_to`, `contradicts`, `depends_on`, `part_of`
   - Extended types (as needed): `supersedes`, `alternative_to`
   - Place all relationships in the `## 🔗 Relations` section of the note
   - Plain `[[wikilink]]` still valid for casual body references but does not count toward `transfer: connected`
   - See @.claude/rules/relationship-modeling.md for complete type definitions and syntax

2. **Synthesize into mental models**
   - Compare with existing knowledge
   - Identify patterns and relationships
   - Build cognitive frameworks

3. **Plan real-world application**
   - How will this information be used?
   - What projects does it support?
   - What areas does it improve?

4. **Set transfer property** (添加到 frontmatter 属性)
   - `transfer: connected` — 笔记中包含 ≥3 个类型化关联 `[xxx:: [[...]]]`（可自动检测，仅计算 Dataview 内联字段，不计普通 wikilink）
   - `transfer: integrated` — 有明确的应用计划段落（需人工判断）
   - `transfer: applied` — 被其他项目/笔记引用并实际使用（需人工判断）
   - `transfer: internalized` — 可不经检索自动回忆（需人工判断）

**Result**: Information transforms into Understanding (usable knowledge)

### 4. DISTILL

Extract only the most valuable insights through Progressive Summarization.

Apply 5-layer compression based on actual usage, not upfront:

#### Progressive Summarization Layers

**Layer 1: Raw** (Capture state)

- Full content as originally captured
- No highlighting or bolding
- Keep as reference

**Layer 2: Bold** (20-30% of content)

- First review: Bold key passages
- Focus on main ideas and valuable insights
- Don't overdo it - less is more

**Layer 3: Highlight** (5-10% of content)

- Second review: Highlight the best parts
- Use `==highlight==` syntax or yellow highlighter
- Only what you'd want to re-read

**Layer 4: Executive Summary**

- Third review: Write summary at top
- Capture the essence in 2-3 paragraphs
- What are the key takeaways?

**Layer 5: Top 1% Output** (Express stage)

- Final stage: Transform into new format
- Presentation, article, tutorial, summary
- Share with others or use for decision-making

#### When to Distill

**Progressive** = based on actual usage:

- **First time you use it**: Bold key passages
- **Second time you use it**: Highlight best parts
- **Third time you use it**: Write executive summary
- **Fourth time you use it**: Create top 1% output

**Don't distill upfront** - wait until you actually use the information

#### Distillation Tracking

Set `distillation` property in frontmatter:

| 值 | 赋值条件 | 检测方式 |
|------|----------|----------|
| `layer2` | 正文中有 ≥3 处有意义的粗体 `**...**` | 排除 frontmatter 和 `#` 标题行后统计 |
| `layer3` | 正文中有 ≥1 处高亮 `==...==` | 任意高亮文本即满足 |
| `layer4` | 笔记顶部有摘要/总结段落 | frontmatter 后、第一个 `##` 前，含关键词（摘要、总结、summary、概要、核心、要点、概述） |
| `layer5` | 内容已转化为 `5.Express/` 中的输出 | 需人工判断 |

**关键规则**:
- **只标记最高层级**：同时满足多个层级时只标记最高的那个
- **Transfer 和 Distillation 属性可共存**

### 5. EXPRESS (`5.Express/`)

Transform ideas into external forms to create value.

Share top 1% of distilled knowledge with others:

#### Express Outputs

**Internal value**:

- Decision documents
- Project proposals
- Process documentation
- Standard operating procedures

**External value**:

- Blog posts and articles
- Presentations and slide decks
- Tutorials and guides
- Videos and podcasts
- Books and courses

#### Benefits of Expression

1. **Consolidates learning**: Teaching reinforces understanding
2. **Receives feedback**: Others provide new perspectives
3. **Builds reputation**: Demonstrates expertise
4. **Creates leverage**: One-time effort, repeated value
5. **Helps others**: Knowledge becomes useful to community

**Result**: Understanding transforms into Wisdom (value-creating output)

## CETDE Workflow Examples

### Example 1: Processing a Web Article

```
CAPTURE (9.Capture/):
- Save article link with brief note about why it's interesting
- Don't worry about organization yet

ENCODE:
- Add frontmatter with tags
- Set para property: para: resources
- Add topic tags: #work/project-alpha, #life/productivity
- Move to: 3.Resources/topic-x/[article-name].md

TRANSFER:
- Link to 3-7 related notes in your system
- Connect to active projects this could help
- Plan how to apply insights

DISTILL (progressive):
- 1st use: Bold key passages (20-30%)
- 2nd use: Highlight best parts (5-10%)
- 3rd use: Write executive summary at top

EXPRESS (if valuable):
- Turn insights into blog post or presentation
- Share with team or community
- Apply to current project
```

### Example 2: Project Meeting Notes

```
CAPTURE:
- Quick notes during meeting in daily note
- Don't worry about structure

ENCODE:
- Add frontmatter with meeting metadata
- Tag with project: #work/project-alpha
- Move to: 1.Projects/project-alpha/meeting-notes.md

TRANSFER:
- Link to related project notes (3-7 wiki-links)
- Connect to relevant resources
- Create action item tasks

DISTILL:
- Extract key decisions
- Summarize action items
- Highlight important insights

EXPRESS:
- Share summary with stakeholders
- Update project README with outcomes
- Create follow-up tasks
```

## CETDE vs CODE: When to Use Which

**Use CODE (high-level)** when:

- Explaining PKM to newcomers
- Planning overall knowledge strategy
- Focusing on information flow, not implementation details

**Use CETDE (detailed)** when:

- Actually working in the LifeOS system
- Implementing specific workflows
- Teaching system operations
- Debugging knowledge management issues

## CETDE Best Practices

### DO ✓

- **Capture quickly**: Don't let organization slow down capture
- **Encode consistently**: Always add frontmatter and tags
- **Transfer generously**: Create 3-7 wiki-links per note
- **Distill progressively**: Only compress when you actually use information
- **Express selectively**: Only share top 1% of distilled knowledge

### DON'T ✗

- **Perfectionism**: Don't try to organize perfectly during capture
- **Over-distillation**: Don't distill upfront - wait until you use it
- **Under-linking**: Don't create notes without connections
- **Hoarding**: Don't collect information without ever expressing value
- **Linear processing**: Don't feel you must complete all 5 stages immediately

## CETDE and DIKW Pyramid

CETDE maps to the DIKW (Data-Information-Knowledge-Wisdom) pyramid:

```
CETDE Stage          DIKW Level              Transformation
─────────────────────────────────────────────────────────────
CAPTURE    →         Data                   → Externalize
ENCODE     →         Information            → Structure
TRANSFER   →         Knowledge              → Connect
DISTILL    →         Knowledge (refined)    → Compress
EXPRESS    →         Wisdom                 → Share
```

## CETDE Integration with LifeOS

### Directory Flow

```
9.Capture/      (CAPTURE stage)
    ↓ ENCODE
1-3. PARA/       (ENCODE stage - organize by actionability)
    ↓ TRANSFER
(Links created)  (TRANSFER stage - connect knowledge)
    ↓ DISTILL
(Apply layers)   (DISTILL stage - progressive compression)
    ↓ EXPRESS
5.Express/      (EXPRESS stage - create outputs)
    ↓ ARCHIVE
4.Archives/     (Completed or inactive)
```

### Query Integration

- **TaskListByTag**: Aggregates tasks after encoding
- **BulletListByTag**: Collects insights during transfer
- **FileListByTag**: Finds encoded notes by tags
- **Distillation property**: Track progress through layers
- **Transfer property**: Monitor integration status

## Common CETDE Mistakes

### 1. Perfectionism in Capture

❌ Trying to organize perfectly while capturing
✅ Capture first, organize later (encode stage)

### 2. Skipping Transfer

❌ Creating isolated notes without connections
✅ Always add 3-7 wiki-links to existing knowledge

### 3. Premature Distillation

❌ Distilling everything upfront
✅ Only distill when you actually use the information

### 4. Never Expressing

❌ Hoarding knowledge without sharing
✅ Express top 1% to create value for others

### 5. Linear Processing

❌ Feeling you must complete all 5 stages immediately
✅ Non-linear workflow is fine - capture now, encode later

## CETDE Workflow Summary

**CAPTURE**: Externalize information quickly
**ENCODE**: Add structure and metadata (findable)
**TRANSFER**: Create connections (understandable)
**DISTILL**: Compress progressively (usable)
**EXPRESS**: Share top 1% (valuable)

**Key insight**: CETDE bridges the gap between organizing information and actually using it by adding structure (Encode) and connections (Transfer).

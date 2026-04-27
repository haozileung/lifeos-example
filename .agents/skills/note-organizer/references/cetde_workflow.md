# CETDE Workflow - Complete Implementation Guide

## Overview

CETDE (Capture-Encode-Transfer-Distill-Express) is LifeOS's extended implementation of the CODE framework, adding two intermediate stages for deeper knowledge integration.

## How CETDE Extends CODE

```
CODE (4 stages):   Capture → Organize → Distill → Express

CETDE (5 stages):  Capture → Encode → Transfer → Distill → Express
                              ↑         ↑
                           NEW stages added
```

**Why extend CODE?** CODE focuses on **what** to do with information, while CETDE focuses on **how** to implement it in a PKM system.

## The Five Stages

### 1. CAPTURE (`9.Capture/`)

**Purpose**: Reduce cognitive load by externalizing information quickly

**Best practices**:
- Capture first, organize later
- Use any available tool (phone, notebook, voice memo)
- Don't worry about perfect organization
- Focus on getting information out of your head

**What to capture**:
- Article links and web clips
- Meeting notes and conversations
- Ideas and insights
- Tasks and reminders
- Quotes and excerpts

**Capture locations**:
- `9.Capture/` directory (temporary holding)
- Daily notes (time-based context)
- Quick notes app (mobile capture)

### 2. ENCODE

**Purpose**: Transform data into structured, findable information

**Encoding checklist**:
- [ ] Add frontmatter with metadata
- [ ] Add `para:` property for PARA classification
- [ ] Add 1-3 topic tags in `tags:` array
- [ ] Move to appropriate PARA location
- [ ] Add creation date

**Frontmatter template**:
```yaml
---
title: "Note Title"
created: 2026-02-10
para: projects         # or areas/resources/archives/capture/express
tags:
  - topic/subtopic
  - additional-tag
aliases:
  - alternative-name
  - related-concept
---
```

**PARA classification** (stored as frontmatter property):
- `para: projects` for active projects
- `para: areas` for ongoing responsibilities
- `para: resources` for reference materials
- `para: archives` for completed items

**File organization**:
- Projects → `1.Projects/`
- Areas → `2.Areas/`
- Resources → `3.Resources/`

### 3. TRANSFER

**Purpose**: Integrate knowledge through connections

**Transfer checklist**:
- [ ] Create 3-7 wiki-links to related notes
- [ ] Use descriptive link text: `[[Concept Name|how this relates]]`
- [ ] Create two-way links where appropriate
- [ ] Plan real-world application

**Wiki-link patterns**:
```markdown
## Related Concepts

This connects to:
- [[Related Note]] for broader context
- [[Specific Concept|how it relates specifically]]
- [[#Heading in same note]] for internal navigation

## Application Plan
1. Use this in [[Active Project Name]]
2. Share with [[Team or Person]]
3. Apply to [[Current Challenge]]
```

**Transfer workflow properties** (添加到 frontmatter):

| 属性 | 赋值条件 | 自动/手动 |
|------|----------|-----------|
| `transfer: connected` | 笔记中包含 ≥3 个 wiki-link `[[...]]` | 可自动检测 |
| `transfer: integrated` | 有明确的应用计划段落 | 需人工判断 |
| `transfer: applied` | 被其他项目/笔记引用并实际使用 | 需人工判断 |
| `transfer: internalized` | 可不经检索自动回忆 | 需人工判断 |

> 仅 `transfer: connected` 可基于 wiki-link 数量自动赋值。其余三个属性需基于实际使用情况人工判断。

### 4. DISTILL

**Purpose**: Extract most valuable insights through Progressive Summarization

**Progressive Summarization layers**:

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

**When to distill** (progressive based on usage):
- **First time you use it**: Bold key passages
- **Second time you use it**: Highlight best parts
- **Third time you use it**: Write executive summary
- **Fourth time you use it**: Create top 1% output

**Distillation tracking properties** (添加到 frontmatter):

| 属性 | 赋值条件 | 检测方式 |
|------|----------|----------|
| `distillation: layer2` | 正文中有 ≥3 处有意义的粗体 `**...**` | 排除 frontmatter 和 `#` 标题行后统计 |
| `distillation: layer3` | 正文中有 ≥1 处高亮 `==...==` | 任意高亮文本即满足 |
| `distillation: layer4` | 笔记顶部有摘要/总结段落 | frontmatter 后、第一个 `##` 前，含关键词（摘要、总结、summary、概要、核心、要点、概述） |
| `distillation: layer5` | 内容已转化为 `5.Express/` 中的输出 | 需人工判断 |

**关键规则**:
- **只标记最高层级**：同时满足 layer2+layer3 时只标记 `distillation: layer3`，同时满足 layer3+layer4 时只标记 `distillation: layer4`
- **Transfer 和 Distillation 属性可共存**：同一笔记可同时有 `transfer: connected` 和 `distillation: layer3`
- **排除格式性粗体**：`#` 标题行、frontmatter 中的粗体不计入 layer2 判定

### 5. EXPRESS (`5.Express/`)

**Purpose**: Share top 1% of distilled knowledge with others

**Expression outputs**:

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

**Expression template**:
```markdown
---
express_type: "blog-post"  # or presentation, tutorial, etc.
express_status: "draft"    # draft, review, published
express_date: 2026-02-15
audience: "team"           # team, public, clients, etc.
---

# Title

## Key Insights
1. First major insight
2. Second important point
3. Practical application

## Detailed Explanation
[Content from distilled notes]

## Next Steps
- Action items
- Further reading
- Implementation plan
```

## CETDE Workflow Examples

### Example 1: Processing a Web Article

```
CAPTURE (9.Capture/):
- Save article link with brief note about why it's interesting
- Don't worry about organization yet

ENCODE:
- Add frontmatter with properties and tags
- Add PARA classification: `para: resources`
- Add topic tags: #work/devops, #productivity
- Move to: 3.Resources/devops/[article-name].md

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
- Set `para: projects` and tag with project: #work-devops-FY26Q1
- Move to: 1.Projects/work-devops-FY26Q1/meeting-2026-01-16.md

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

### Time-Based Integration

**Daily workflow**:
- Morning: Capture new ideas
- Throughout day: Encode and transfer
- Evening: Distill based on usage
- Weekly: Express top insights

**Weekly review**:
- Process all captures from the week
- Strengthen connections between notes
- Apply next layer of distillation
- Identify expressions to create

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

## Summary

**CETDE Workflow**:
- **CAPTURE**: Externalize information quickly
- **ENCODE**: Add structure and metadata (findable)
- **TRANSFER**: Create connections (understandable)
- **DISTILL**: Compress progressively (usable)
- **EXPRESS**: Share top 1% (valuable)

**Key insight**: CETDE bridges the gap between organizing information and actually using it by adding structure (Encode) and connections (Transfer).

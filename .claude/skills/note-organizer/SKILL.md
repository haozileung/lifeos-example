---
name: note-organizer
description: Comprehensive note organization and optimization for Obsidian PKM systems. Use when working with Obsidian vaults, Markdown notes, or personal knowledge management systems. Specifically triggers when users need to organize notes using PARA method, apply CETDE workflow to process knowledge, add frontmatter metadata and tags, create wiki-links and connections, distill notes through progressive summarization, archive completed items, or optimize note structure for better retrieval.
---

# Note Organizer Skill

## Overview

This skill enables systematic organization and optimization of Obsidian notes using PARA method and CETDE workflow principles. It provides structured approaches for transforming raw notes into actionable knowledge.

## Quick Start

### When to Use This Skill

Use this skill when you need to:
- **Organize scattered notes** into PARA structure (Projects/Areas/Resources/Archives)
- **Process captured information** through CETDE workflow stages
- **Add metadata and connections** to make notes more discoverable
- **Distill notes** through progressive summarization
- **Archive completed items** to reduce cognitive load
- **Optimize existing notes** for better knowledge retrieval

### Basic Workflow

1. **Capture**: Collect raw information in `9.Capture/` or daily notes
2. **Encode**: Add frontmatter, tags, and PARA classification
3. **Transfer**: Create 3-7 wiki-links to related notes
4. **Distill**: Apply progressive summarization based on usage
5. **Express**: Transform insights into shareable outputs
6. **Archive**: Move completed items to `4.Archives/`

## PARA Organization

### Projects (`1.Projects/`)

Short-term efforts with specific outcomes and deadlines.

**Key attributes**:
- Has specific, measurable outcome
- Has clear deadline or end date
- Can be marked as "complete"
- Drives current action and attention

**Example project structure**:
```markdown
---
project_name: "DevOps FY26 Q1"
project-status: "active"
due_date: 2026-03-31
para: projects
tags:
  - work/devops
---

# DevOps FY26 Q1

## Outcome
Complete infrastructure automation for deployment pipeline

## Success Criteria
- 90% automated deployments
- <5 minute deployment time
- Zero manual intervention

## Tasks
```LifeOS
TaskListByTag #work-devops-FY26Q1
```
```

### Areas (`2.Areas/`)

Ongoing responsibilities requiring maintenance over time.

**Key attributes**:
- Has a standard to be maintained
- No completion date (ongoing)
- Can have multiple projects within them
- Reviewed regularly for maintenance needs

**Example area structure**:
```markdown
---
area_name: "Personal Health"
area-status: "active"
para: areas
tags:
  - personal/health
---

# Personal Health

## Standards
- Exercise 3x per week
- Sleep 7-8 hours nightly
- Balanced nutrition

## Maintenance Tasks
- Weekly meal planning
- Monthly health check-ins
- Quarterly fitness assessment
```

### Resources (`3.Resources/`)

Topics of ongoing interest and reference materials.

**Key attributes**:
- Useful but not immediately actionable
- Reference materials for future use
- Can fuel both projects and areas
- Organized by topic, not actionability

**Example resource structure**:
```markdown
---
resource_name: "PKM Resources"
resource-type: "topic"
para: resources
tags:
  - productivity/pkm
---

# PKM Resources

## Knowledge Map
- [[PARA Method]]
- [[CETDE Workflow]]
- [[Progressive Summarization]]

## Key Concepts
- Second Brain methodology
- Knowledge processing workflows
- Information architecture
```

### Archives (`4.Archives/`)

Completed or inactive items.

**When to archive**:
- Projects marked complete
- Areas no longer maintained
- Resources outdated but potentially useful

**Example archive metadata**:
```markdown
---
archive_name: "DevOps FY25 Q4"
archive-date: 2026-01-01
archive-reason: "completed"
original-type: "project"
para: archives
tags:
  - work/devops
---
```

## CETDE Workflow Implementation

### 1. Capture Stage

**Purpose**: Externalize information quickly without overthinking

**Best practices**:
- Use `9.Capture/` directory for temporary holding
- Capture in daily notes with minimal structure
- Don't worry about perfect organization
- Focus on getting information out of your head

**Example capture**:
```markdown
# 2026-02-10 Capture

## Ideas
- Need to automate deployment pipeline
- Article about progressive summarization techniques
- Meeting notes from team sync

## Tasks
- [ ] Research deployment automation tools #work-devops-FY26Q1
- [ ] Read progressive summarization article #productivity/pkm
```

### 2. Encode Stage

**Purpose**: Transform data into structured, findable information

**Encoding checklist**:
- [ ] Add frontmatter with metadata
- [ ] Add PARA classification tag
- [ ] Add 1-3 topic tags
- [ ] Move to appropriate PARA location
- [ ] Add creation date

**Example encoding**:
```yaml
---
title: "Deployment Automation Research"
created: 2026-02-10
para: projects
tags:
  - work/devops
  - automation
aliases:
  - deployment-automation
---
```

### 3. Transfer Stage

**Purpose**: Integrate knowledge through connections

**Transfer checklist**:
- [ ] Create 3-7 wiki-links to related notes
- [ ] Use descriptive link text: `[[Concept Name|how this relates]]`
- [ ] Create two-way links where appropriate
- [ ] Plan real-world application

**Transfer workflow properties** (设置 frontmatter 属性):

| 属性值 | 赋值条件 | 说明 |
|------|----------|------|
| `transfer: connected` | 笔记中包含 ≥3 个 wiki-link `[[...]]` | 已建立知识连接 |
| `transfer: integrated` | 有明确的应用计划段落 | 已规划实际应用（需人工判断） |
| `transfer: applied` | 被其他项目/笔记引用并实际使用 | 已在真实场景中使用（需人工判断） |
| `transfer: internalized` | 可不经检索自动回忆 | 已内化为直觉（需人工判断） |

> **自动判定规则**：仅 `transfer: connected` 可基于 wiki-link 数量自动赋值（≥3 个）。`integrated`/`applied`/`internalized` 需基于实际使用情况人工判断，不适合自动回填。

**Example transfer**:
```markdown
## Related Concepts

This connects to:
- [[CI/CD Pipeline]] for continuous integration
- [[Infrastructure as Code]] for automation
- [[Team Deployment Process|current team workflow]]

## Application Plan
1. Research tools mentioned in [[DevOps Tools Comparison]]
2. Create proof of concept in [[Test Environment Setup]]
3. Present findings to [[Team Meeting Notes 2026-02-15]]
```

### 4. Distill Stage

**Purpose**: Extract most valuable insights through progressive summarization

**Distillation layers**:
1. **Layer 1: Raw** - Full content as captured
2. **Layer 2: Bold** - 20-30% key passages bolded
3. **Layer 3: Highlight** - 5-10% best parts highlighted
4. **Layer 4: Summary** - Executive summary at top
5. **Layer 5: Output** - Transformed into new format

**Distillation workflow properties** (设置 frontmatter 属性):

| 属性值 | 赋值条件 | 检测方式 |
|------|----------|----------|
| `distillation: layer2` | 正文中有 ≥3 处有意义的粗体 `**...**` | 排除 frontmatter 和 `#` 标题行后统计 |
| `distillation: layer3` | 正文中有 ≥1 处高亮 `==...==` | 任意高亮文本即满足 |
| `distillation: layer4` | 笔记顶部（frontmatter 之后、第一个 `##` 之前）有摘要/总结段落 | 检测关键词：摘要、总结、summary、概要、核心、要点、概述 |
| `distillation: layer5` | 笔记内容已被转化为 5.Express/ 中的输出 | 需人工判断 |

**关键规则**:
- **只标记最高层级**：若同时满足 layer2 和 layer3，只标记 `distillation: layer3`
- **Transfer 和 Distillation 属性可共存**：同一笔记可同时有 `transfer: connected` 和 `distillation: layer3`
- **排除格式性粗体**：`#` 标题行、frontmatter 中的粗体不计入 layer2 判定

### 5.Express Stage

**Purpose**: Share top 1% of distilled knowledge

**Expression outputs**:
- **Internal**: Decision documents, project proposals, SOPs
- **External**: Blog posts, presentations, tutorials, videos

**Example expression**:
```markdown
---
express_type: "blog-post"
express_status: "draft"
express_date: 2026-02-15
---

# How PARA Method Transformed My Productivity

## Key Insights
1. Actionability over topic organization
2. Progressive processing through CETDE
3. Regular review and maintenance

## Practical Applications
- Daily workflow optimization
- Project management system
- Knowledge retention strategies
```

## Common Operations

### Note Optimization Checklist

Use this checklist to optimize existing notes:

**Structure**:
- [ ] Clear, descriptive title
- [ ] Logical heading hierarchy
- [ ] Consistent formatting
- [ ] Proper paragraph breaks

**Metadata**:
- [ ] Frontmatter with creation date
- [ ] PARA classification tag
- [ ] 1-3 topic tags
- [ ] Aliases for alternative names

**Connections**:
- [ ] 3-7 wiki-links to related notes
- [ ] Descriptive link text
- [ ] Backlinks from other notes
- [ ] Integration with active projects/areas

**Content**:
- [ ] Progressive summarization applied
- [ ] Key insights highlighted
- [ ] Action items identified
- [ ] Clear next steps

### Daily Note Optimization

**Morning routine**:
1. Review yesterday's tasks and outcomes
2. Set priorities for today using PARA framework
3. Capture new ideas in `9.Capture/` section
4. Link to active projects and areas

**Evening routine**:
1. Review completed tasks
2. Process captures through encoding
3. Create connections to existing knowledge
4. Plan tomorrow's priorities

### Weekly Review Process

**PARA review**:
1. **Projects**: Check progress, update tasks, adjust deadlines
2. **Areas**: Review maintenance, identify improvement projects
3. **Resources**: Distill frequently used resources
4. **Archives**: Move completed items, review for reactivation

**CETDE review**:
1. **Capture**: Process all items in `9.Capture/`
2. **Encode**: Add metadata to unprocessed notes
3. **Transfer**: Strengthen connections between notes
4. **Distill**: Apply next layer of summarization
5. **Express**: Identify insights worth sharing

## Troubleshooting

### Common Issues and Solutions

**Problem**: Notes feel scattered and unorganized
**Solution**: Apply PARA classification to all notes, move to appropriate directories

**Problem**: Can't find notes when needed
**Solution**: Add consistent frontmatter, tags, and wiki-links for better discoverability

**Problem**: Notes contain valuable insights but are too long
**Solution**: Apply progressive summarization - bold key passages, highlight best parts

**Problem**: Knowledge feels isolated and disconnected
**Solution**: Create 3-7 wiki-links per note to build knowledge network

**Problem**: Completed projects clutter active view
**Solution**: Archive completed items with metadata for future reference

### Quality Standards

**High-quality notes have**:
- Clear purpose and audience
- Consistent structure and formatting
- Rich metadata and tagging
- Multiple connections to related knowledge
- Progressive summarization applied
- Actionable insights and next steps

**Avoid**:
- Notes without metadata or tags
- Isolated notes without connections
- Overly long, unstructured content
- Perfectionism that prevents progress
- Hoarding without distillation or expression

## Resources

This skill includes reference materials for deeper understanding:

### References/
- `para_method.md` - Detailed PARA implementation guide
- `cetde_workflow.md` - Complete CETDE workflow documentation
- `progressive_summarization.md` - Progressive summarization techniques
- `obsidian_best_practices.md` - Obsidian-specific optimization tips

### Scripts/
- `note_analyzer.py` - Analyze note structure and suggest improvements
- `link_generator.py` - Suggest wiki-links based on content analysis
- `metadata_checker.py` - Validate frontmatter and tag consistency

### Assets/
- `para_decision_tree.png` - Visual guide for PARA classification
- `cetde_workflow_diagram.png` - CETDE workflow visualization
- `note_templates/` - Template files for different note types

## Summary

**Note Organizer Skill** provides systematic approaches for:
- **PARA organization** by actionability (Projects/Areas/Resources/Archives)
- **CETDE workflow** for knowledge processing (Capture/Encode/Transfer/Distill/Express)
- **Progressive summarization** based on actual usage
- **Connection building** through wiki-links
- **Regular review** for continuous optimization

**Key principle**: Organize by what you're trying to accomplish (actionability), not by topic. Process knowledge progressively based on usage, not upfront perfection.

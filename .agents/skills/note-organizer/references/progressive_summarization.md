# Progressive Summarization - Complete Guide

## Overview

Progressive Summarization is a technique for compressing information through multiple layers of distillation, applied progressively based on actual usage rather than upfront.

## The Five Layers

### Layer 1: Raw (Capture State)

**Purpose**: Preserve original content as reference

**Characteristics**:
- Full content as originally captured
- No highlighting or bolding
- Keep as-is for reference
- No compression applied

**When to use**: Initial capture stage
**Compression**: 0% (original)

### Layer 2: Bold (20-30% of content)

**Purpose**: Identify key passages on first review

**Process**:
- First time you use the information
- Bold the most important 20-30% of content
- Focus on main ideas and valuable insights
- Don't overdo it - less is more

**Guidelines**:
- Bold complete sentences or paragraphs
- Avoid bolding single words
- Focus on actionable insights
- Mark concepts you want to remember

**When to apply**: First time you reference the note
**Compression**: 70-80% (20-30% remains)

### Layer 3: Highlight (5-10% of content)

**Purpose**: Extract the very best parts on second review

**Process**:
- Second time you use the information
- Highlight the most valuable 5-10% of content
- Use `==highlight==` syntax or yellow highlighter
- Only what you'd absolutely want to re-read

**Guidelines**:
- Highlight within already-bolded sections
- Focus on breakthrough insights
- Mark passages worth quoting or sharing
- Identify core principles

**When to apply**: Second time you reference the note
**Compression**: 90-95% (5-10% remains)

### Layer 4: Executive Summary

**Purpose**: Capture the essence in your own words

**Process**:
- Third time you use the information
- Write 2-3 paragraph summary at the top
- Capture key takeaways in your own words
- Focus on practical applications

**Structure**:
```markdown
## Summary

**Key insights**:
1. First major insight
2. Second important point
3. Practical application

**Main takeaways**:
- What you learned
- How to apply it
- Why it matters

**Next steps**:
- Action items
- Further exploration
- Implementation plan
```

**When to apply**: Third time you reference the note
**Compression**: 99% (1% essence captured)

### Layer 5: Top 1% Output

**Purpose**: Transform insights into new, shareable formats

**Process**:
- Fourth time you use the information
- Remix distilled insights into new format
- Create value for others
- Share your unique perspective

**Output formats**:
- Blog posts and articles
- Presentations and slide decks
- Tutorials and guides
- Videos and podcasts
- Decision documents
- Project proposals

**When to apply**: When insights are valuable enough to share
**Compression**: 100% (transformed into new creation)

## Progressive Application

### When to Apply Each Layer

**Based on usage, not upfront perfection**:

```
Usage Count  →  Layer to Apply
──────────────────────────────
First use    →  Layer 2: Bold key passages
Second use   →  Layer 3: Highlight best parts
Third use    →  Layer 4: Write executive summary
Fourth use   →  Layer 5: Create top 1% output
```

**Key principle**: Only compress information when you actually use it. Don't distill everything upfront.

### Tracking Progress

**Distillation workflow properties** (添加到 frontmatter):

| 属性 | 赋值条件 | 检测方式 |
|------|----------|----------|
| `distillation: layer2` | 正文中有 ≥3 处有意义的粗体 `**...**` | 排除 frontmatter 和 `#` 标题行后统计 |
| `distillation: layer3` | 正文中有 ≥1 处高亮 `==...==` | 任意高亮文本即满足 |
| `distillation: layer4` | 笔记顶部有摘要/总结段落 | frontmatter 后、第一个 `##` 前，含关键词（摘要、总结、summary、概要、核心、要点、概述） |
| `distillation: layer5` | 内容已转化为 `5.Express/` 中的输出 | 需人工判断 |

**关键规则**:
- **只标记最高层级**：同时满足多个层级时，只标记最高的那个。例如：有粗体也有高亮，只标记 `distillation: layer3`
- **排除格式性粗体**：`#` 标题行、frontmatter 中的粗体不计入 layer2 判定
- **与 Transfer 属性共存**：同一笔记可同时有 `transfer: connected` 和任一 `distillation: layer*`

**Frontmatter tracking** (可选，补充属性):
```yaml
---
distillation: layer3
distillation_date: 2026-02-10
distillation_notes: "Highlighted core principles"
---
```

## Practical Examples

### Example 1: Research Article

**Original article**: 5,000 words

**Layer 1 (Raw)**:
- Full article saved as reference

**Layer 2 (Bold)**:
- 1,000 words bolded (20%)
- Key concepts and findings
- Important data points

**Layer 3 (Highlight)**:
- 250 words highlighted (5%)
- Breakthrough insights
- Actionable recommendations

**Layer 4 (Summary)**:
- 150-word executive summary
- 3 key takeaways
- Application plan

**Layer 5 (Output)**:
- 800-word blog post
- Shared with team
- Applied to current project

### Example 2: Meeting Notes

**Original notes**: 2,000 words

**Layer 1 (Raw)**:
- Full transcript and notes

**Layer 2 (Bold)**:
- 400 words bolded (20%)
- Key decisions
- Action items
- Important discussion points

**Layer 3 (Highlight)**:
- 100 words highlighted (5%)
- Critical decisions
- Urgent action items
- Breakthrough ideas

**Layer 4 (Summary)**:
- 100-word meeting summary
- Sent to stakeholders
- Added to project README

**Layer 5 (Output)**:
- Updated project plan
- Created decision document
- Shared lessons learned

## Best Practices

### DO ✓

- **Apply progressively**: Only distill when you use the information
- **Start with bolding**: Easy first step with high ROI
- **Highlight within bold**: Nested compression for efficiency
- **Write in your own words**: Summary should reflect your understanding
- **Share valuable insights**: Expression creates value for others

### DON'T ✗

- **Distill everything upfront**: Wait until you actually use it
- **Over-highlight**: 5-10% is sufficient for most notes
- **Skip layers**: Each layer builds on the previous
- **Forget to track**: Use tags to know what's been done
- **Hoard without expressing**: Knowledge gains value when shared

## Common Mistakes

### 1. Premature Distillation

❌ Distilling everything immediately after capture
✅ Only distill when you actually reference the note

### 2. Over-Distillation

❌ Highlighting 50% of the content
✅ Highlight only 5-10% - the very best parts

### 3. Skipping Layers

❌ Going from raw to executive summary
✅ Build progressively: bold → highlight → summary

### 4. Not Tracking

❌ Forgetting what distillation level you're at
✅ Use properties or frontmatter to track progress

### 5. Never Expressing

❌ Keeping all distilled knowledge to yourself
✅ Share top 1% to create value for others

## Integration with CETDE

Progressive Summarization is the **Distill** stage of CETDE:

```
CETDE Stage          Progressive Layer
──────────────────────────────────────
Capture     →        Layer 1: Raw
Encode      →        (Metadata added)
Transfer    →        (Connections made)
Distill     →        Layers 2-5
Express     →        Layer 5 output
```

**Workflow integration**:
1. **Capture**: Save information (Layer 1)
2. **Encode**: Add metadata and tags
3. **Transfer**: Create wiki-links
4. **Distill**: Apply progressive layers based on usage
5. **Express**: Share Layer 5 outputs

## Tools and Techniques

### Obsidian Features

**Bolding**: `**bold text**` or `__bold text__`
**Highlighting**: `==highlighted text==`
**Callouts**: For summaries and key points
```markdown
> [!summary]
> Executive summary goes here
```

**Properties**: For tracking distillation level (`distillation: layer*`)
**Frontmatter**: For metadata and progress tracking

### Visual Cues

**Color coding** (optional):
- Yellow: Highlighted text
- Blue: Bolded text
- Green: Your own summaries
- Red: Critical insights

**Icons** (optional):
- ⭐: Key insight
- 💡: Idea to explore
- ✅: Action item
- 🔗: Important connection

## Summary

**Progressive Summarization**:
- **Layer 1**: Raw content (reference)
- **Layer 2**: Bold key passages (20-30%)
- **Layer 3**: Highlight best parts (5-10%)
- **Layer 4**: Executive summary (essence)
- **Layer 5**: Top 1% output (shared value)

**Key principle**: Distill progressively based on actual usage, not upfront perfection. Each layer makes information more accessible and valuable.

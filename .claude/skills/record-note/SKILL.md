---
name: record-note
description: 自动识别内容类型并按项目、领域、周期优先级，记录到LifeOS/Obsidian PKM系统对应笔记（如今日笔记、项目笔记、周记等），自动添加frontmatter、标签、wiki-link，确保聚合与检索。
---

# Record Note Skill

## 触发时机

- 用户希望用自然语言或直接调用技能，快速记录任意类型内容（如会议纪要、灵感、任务、项目进展、习惯打卡等）到LifeOS笔记系统。
- 需要自动判断内容应归属的笔记类型（项目、领域、周期/日/周/月/季/年），并按优先级（项目>领域>周期）插入。
- 需自动处理元数据、topic tag、frontmatter、wiki-link、内容插入等，保证笔记结构和聚合查询正常。

## 工作流程

1. **内容识别**：分析输入内容，自动判断归属（项目、领域、周期/日/周/月/季/年）。优先级：项目>领域>周期。
2. **定位目标笔记**：
   - 项目类：写入`1.Projects/{project}/`下README或相关笔记
   - 领域类：写入`2.Areas/{area}/`下README或相关笔记
   - 周期类：写入`0.PeriodicNotes/{year}/Daily|Weekly|Monthly|Quarterly|Yearly/`下对应日期笔记
3. **内容整理与插入**：
   - 自动添加frontmatter（如日期、归属、标签）
   - 自动生成topic tag（如#work/project-x、#personal-growth等）
   - 自动添加wiki-link（3-7个相关笔记）
   - 按目标笔记格式插入到合适section（如”📝 Daily Record”、”项目进展”等）
   - **工作流属性**：如果插入的内容使目标笔记满足工作流属性条件，自动更新对应属性
     - `transfer: connected`：笔记 wiki-link 总数 ≥3 时设置
     - `distillation: layer2`：笔记正文有意义粗体 ≥3 处时设置
     - `distillation: layer3`：笔记正文有 ≥1 处高亮 `==...==` 时设置
     - `distillation: layer4`：笔记顶部有摘要/总结段落时设置
     - 只标记最高 distillation 层级；Transfer 和 Distillation 属性可共存
4. **聚合与检索保障**：
   - 确保所有任务、记录、bullet等能被TaskListByTag/BulletListByTag/FileListByTag等聚合查询正确识别
   - 保证标签、frontmatter、wiki-link规范
5. **歧义与无法识别处理**：
   - 如果无法准确判断内容归属的项目、领域或周期，或标签(topic tag)存在歧义/不确定，必须主动询问用户，获得明确指示后再插入内容。
   - 询问内容包括：应归属的项目/领域/周期、建议的topic tag、插入位置等。

## 输出格式

- 直接修改目标笔记文件，插入整理后的内容
- 内容需带有frontmatter、topic tag、wiki-link，符合LifeOS聚合与检索规则
- 若有归属或标签不确定，先与用户确认

## 示例

**输入**：
“今天和Oliver对齐了团队能力建设目标，需聚焦自动化和协作。”
**输出**：

- 自动识别为项目/领域相关，插入到今日笔记“📝 Daily Record”区块，并加上#work/devops等topic tag和相关wiki-link。

**输入**：
“记录：‘2026-03-25’未找到合适归属，请问应记录到哪个项目或领域？”
**输出**：

- 系统应主动询问用户归属（项目/领域/周期），并在获得明确指示后再插入内容。

## 依赖

- 需配合note-organizer、tag-system、para-method、cetde-workflow等规则使用

## 测试用例建议

- 记录会议纪要到今日笔记
- 记录项目进展到项目笔记
- 记录习惯打卡到周期笔记
- 记录灵感到资源笔记
- 检查标签、frontmatter、wiki-link是否规范
- 无法判断归属或标签时，系统应主动询问用户

---
name: para-project-lifecycle
description: >
  管理LifeOS/PARA系统中项目的完整生命周期：创建、归档、重新激活。
  当用户要求创建新项目、完成项目、归档项目、关闭项目、重新激活项目、恢复项目时使用此技能。
  也适用于用户说"新开一个项目"、"把XX项目归档"、"XX项目做完了"、"恢复XX项目"等场景。
  基于PARA方法论，项目是"有明确目标和截止日期的短期努力"，存放在1.Projects/，完成后归档到4.Archives/。
---

# PARA 项目生命周期管理

管理 Obsidian LifeOS vault 中 PARA 项目的创建、归档和重新激活。

## 核心概念

PARA 项目 = 有明确结果描述、成功标准和截止日期的短期努力。存放于 `1.Projects/`，完成后归档到 `4.Archives/`。

项目目录命名：`{category}-{name}`（小写，连字符分隔），如 `work-bvf-FY27Q1`。
README 命名：`{name}.README.md`（与目录名中的 name 部分对应）。

## 操作流程

### 一、创建新项目

**触发**：用户说"创建项目"、"新项目"、"开一个项目"等。

**步骤**：

1. **收集项目信息**：向用户确认以下内容（用户可能已部分提供）：
   - 项目名称（英文，用于目录命名）
   - 项目分类前缀（如 work/devops/work-management）
   - 结果描述（项目完成后的具体成果）
   - 成功标准（如何判断项目完成）
   - 截止日期
   - topic tag（格式参考 tag-system.md）

2. **创建项目目录**：
   ```
   1.Projects/{category}-{name}/
   ```

3. **创建 README 文件** `1.Projects/{category}-{name}/{name}.README.md`：

   ```yaml
   ---
   para: projects
   tags:
     - {topic-tag}
   project_name: {项目中文名/显示名}
   project-status: active
   due_date: {YYYY-MM-DD}
   date-created: {today}
   aliases: "#{topic-tag}"
   ---
   ```

   正文结构（参考 8.Templates/Project.md）：
   - 项目概述（结果描述、价值主张、成功标准、截止日期）
   - 任务列表（使用 `TaskListByTag` 查询块）
   - 想法与笔记（使用 `BulletListByTag` 查询块）
   - 相关文件（使用 `FileListByTag` 查询块）
   - 项目进展（本周进展、挑战、下一步）
   - 项目回顾（完成时填写）
   - 相关链接

4. **关联到周期笔记**：在对应的季度笔记中添加指向新项目的 wiki-link，季度笔记的选择遵循财年双标签策略（见记忆 fiscal-calendar-strategy.md）。

5. **确认**：展示创建结果，包括目录路径、topic tag、关联的季度笔记。

---

### 二、归档项目

**触发**：用户说"完成项目"、"归档项目"、"项目做完了"、"关闭项目"等。

**步骤**：

1. **定位项目**：
   - 在 `1.Projects/` 下搜索匹配的项目目录
   - 读取 README 确认项目信息
   - 向用户确认要归档的项目

2. **更新 README frontmatter**：

   变更项：
   - `para`: `projects` → `archives`
   - `project-status`: `active` → `completed`
   - 新增 `archive-date`: 当天日期
   - 新增 `archive-reason`: 用户提供的归档原因

   示例变更：
   ```yaml
   # 变更前
   para: projects
   tags:
     - work/devops/cursor-rollout
   project-status: active

   # 变更后
   para: archives
   tags:
     - work/devops/cursor-rollout
   project-status: completed
   archive-date: 2026-04-01
   archive-reason: "项目目标达成，Cursor已全面落地产研团队"
   ```

3. **移动项目目录**：
   ```
   mv 1.Projects/{project-dir} 4.Archives/{project-dir}
   ```

4. **更新全库 wiki-link 引用**：
   - 搜索所有 `.md` 文件中对 `1.Projects/{project-dir}` 的引用
   - 批量替换为 `4.Archives/{project-dir}`
   - 排除 `.obsidian/` 目录
   - 替换后验证零残留

5. **更新周期笔记中的项目引用**（如有）：
   - 检查季度笔记中是否引用了该项目
   - 如果引用路径是完整路径（`1.Projects/...`），更新为 `4.Archives/...`
   - 如果引用仅用项目名（`[[FY27Q1.README]]`），Obsidian 会自动解析，无需更改

6. **确认**：展示归档结果摘要（状态变更、移动路径、引用更新数量）。

---

### 三、重新激活项目

**触发**：用户说"恢复项目"、"重新激活"、"把XX从归档恢复"等。

**步骤**：

1. **定位项目**：
   - 在 `4.Archives/` 下搜索匹配的项目目录
   - 读取 README 确认项目信息
   - 向用户确认要恢复的项目

2. **更新 README frontmatter**：

   变更项：
   - `para`: `archives` → `projects`
   - `project-status`: `completed` → `active`
   - 移除 `archive-date` 和 `archive-reason`（或改为注释）
   - 更新 `due_date`（如果用户提供了新的截止日期）

3. **移动项目目录**：
   ```
   mv 4.Archives/{project-dir} 1.Projects/{project-dir}
   ```

4. **更新全库 wiki-link 引用**：
   - 搜索所有 `.md` 文件中对 `4.Archives/{project-dir}` 的引用
   - 批量替换为 `1.Projects/{project-dir}`
   - 排除 `.obsidian/` 目录
   - 替换后验证零残留

5. **确认**：展示恢复结果摘要。

---

## 关键规则

- **目录命名**：`{category}-{name}`，全小写，连字符分隔。如 `work-bvf-FY27Q1`、`work-devops-gitlab`
- **README 命名**：`{name}.README.md`，与目录名对应
- **topic tag**：必须与 README 的 `tags` 和 `aliases` 一致，确保 TaskListByTag 等查询能正确聚合
- **引用更新**：归档/恢复时必须更新全库 wiki-link，避免断链
- **PARA 属性**：项目在 `1.Projects/` 时 `para: projects`，归档后 `para: archives`
- **财年归属**：季度笔记中的项目引用，按财年双标签策略确定归属的自然年目录
- **不触碰 `.obsidian/`**：所有批量操作排除 `.obsidian/` 目录

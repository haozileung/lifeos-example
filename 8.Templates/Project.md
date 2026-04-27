---
para: projects
tags: []
name: <% tp.file.title.replace(/\.README$/, "") %>
status: active
due_date: <% tp.date.now("YYYY-MM-DD") %>
date-created: <% tp.date.now("YYYY-MM-DD") %>
aliases: []
---

# <% tp.file.title.replace(/\.README$/, "") %>

- **Outcome**: Description of what success looks like
- **Value**: Why this project matters
- **Success Criteria**: How to measure completion
- **Due Date**: 📅 <% tp.date.now("YYYY-MM-DD") %>

## 🔗 Relations

- depends on: [depends_on:: ]
- part of: [part_of:: ]
- supersedes: [supersedes:: ]
- applies to: [applies_to:: ]

## 📋 Task

```LifeOS
TaskListByTag
```

## 💡 Bullet

```LifeOS
BulletListByTag
```

## 📂 File

```LifeOS
FileListByTag
```
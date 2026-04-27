---
para: archives
tags: []
name: <% tp.file.title.replace(/\.README$/, "") %>
archive-date: <% tp.date.now("YYYY-MM-DD") %>
archive-reason: completed
original-type: project
date-created: <% tp.date.now("YYYY-MM-DD") %>
aliases: []
---

# <% tp.file.title.replace(/\.README$/, "") %>
## 📋 Task
%%Query tasks based on the tags field of the [Properties](https://help.obsidian.md/Editing+and+formatting/Properties) of the current file, extracted from all the notes%%
```LifeOS
TaskListByTag
```

## 💡 Bullet
%%Query bullets based on the tags field of the [Properties](https://help.obsidian.md/Editing+and+formatting/Properties) of the current file, extracted from all the notes%%
```LifeOS
BulletListByTag
```

## 📂 File
%%Query files based on the tags field of the [Properties](https://help.obsidian.md/Editing+and+formatting/Properties) of the current file, extracted from all the notes%%
```LifeOS
FileListByTag
```
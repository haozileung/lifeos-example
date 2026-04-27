---
periodic_type: monthly
date: <% tp.file.title %>
year: <% tp.file.title.split('-')[0] %>
month: <% tp.file.title.split('-')[1] %>
date-created: <% tp.date.now("YYYY-MM-DD HH:mm") %>
---

# <% tp.file.title %>

%%Arrange tasks from the "Priority First Dimension" and the "Role Dimension" respectively%%

# 📋 Task

## 🌟 Priority First Dimension
%%A list of projects experienced during this month, extracted from this month's diary, with automatic statistics on the percentage of time spent on projects%%
```LifeOS
ProjectListByTime
```

## 👤 Role Dimension
### 💼 Employee
%% As an employee, how do you disassemble this month's tasks for this quarter's goals? %%
- [ ] Fill in monthly #work/trivia
- OKR
### 💑 Husband
### 👨‍👧 Father
### 👦 Son
### 🧘 Myself
- Planning for the next month

# 🔍 Review
## 📥 Collected this month
%%List of tasks collected this month from this month's diary%%
```LifeOS
TaskRecordListByTime
```

%%List of bullets/flash notes collected this month from this month's diary%%
```LifeOS
BulletRecordListByTime
```

## ✅ Completed this month
%%List of tasks completed this month, extracted from all notes%%
```LifeOS
TaskDoneListByTime
```

---
periodic_type: weekly
date: <% tp.file.title %>
year: <% tp.file.title.split('-W')[0] %>
week: <% tp.file.title.split('-W')[1] %>
date-created: <% tp.date.now("YYYY-MM-DD HH:mm") %>
---

# <% tp.file.title %>
%%Arrange tasks from the "Priority First Dimension" and the "Role Dimension" respectively%%
# 📋 Task
## 🌟 Priority First Dimension
%%A list of projects experienced during this week, extracted from this week's diary, with automatic statistics on the percentage of time spent on projects%%
```LifeOS
ProjectListByTime
```

## 👤 Role Dimension
### 💼 Employee
%% As an employee, how do you break down this week's tasks for this month's tasks? %%
- OKR
### 💑 Husband
### 👨‍👧 Father
### 👦 Son
### 🧘 Myself
- Planning for the next week

# 🔍 Review
## 📥 Collected this week
%%List of tasks collected this week from this week's diary%%
```LifeOS
TaskRecordListByTime
```

%%List of bullets/flash notes collected this week from this week's diary%%
```LifeOS
BulletRecordListByTime
```

## ✅ Completed this week
%%List of tasks completed this week, extracted from all notes%%
```LifeOS
TaskDoneListByTime
```

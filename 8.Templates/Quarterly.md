---
periodic_type: quarterly
year: <% tp.file.title.split('-Q')[0] %>
quarter: <% tp.file.title.split('-Q')[1] %>
fiscal_year: <% (() => { const y = parseInt(tp.file.title.split('-Q')[0]); const q = parseInt(tp.file.title.split('-Q')[1]); return (q >= 1 && q <= 3) ? `FY${y}` : `FY${y + 1}`; })() %>
fiscal_quarter: <% (() => { const q = parseInt(tp.file.title.split('-Q')[1]); return q >= 1 && q <= 3 ? `Q${q + 1}` : 'Q1'; })() %>
date-created: <% tp.date.now("YYYY-MM-DD HH:mm") %>
---

# <% tp.file.title %>

%%Setting goals from the "Priority First Dimension" and the "Role Dimension" respectively%%

# 🎯 Goals

## 🌟 Priority First Dimension
%%A snapshot of the area this quarter%%
<% LifeOS.Area.snapshot() %>

## 👤 Role Dimension
### 💼 Employee
%% As an employee, what are your annual goals? %%
### 💑 Husband
### 👨‍👧 Father
### 👦 Son
### 🧘 Myself
- Planning for the next quarter

# 🔍 Review
## 🚀 Project List
%%List of tasks collected this quarter from this quarter's diary%%
```LifeOS
ProjectListByTime
```

## 📥 Collected this quarter
%%List of tasks collected this quarter from this quarter's diary%%
```LifeOS
TaskRecordListByTime
```

%%List of bullets/flash notes collected this quarter from this quarter's diary%%
```LifeOS
BulletRecordListByTime
```

## ✅ Completed this quarter
%%List of tasks completed this quarter, extracted from all notes%%
```LifeOS
TaskDoneListByTime
```
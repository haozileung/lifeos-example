---
periodic_type: daily
date: <% tp.file.title %>
year: <% tp.file.title.split('-')[0] %>
month: <% tp.file.title.split('-')[1] %>
day: <% tp.file.title.split('-')[2] %>
date-created: <% tp.date.now("YYYY-MM-DD HH:mm") %>
---
# <% tp.file.title %>
## 🚀 Project List
%%A snapshot of the project today%%
<% LifeOS.Project.snapshot() %>

## 📅 Calendar

%%Today's scheduled meetings and events%%

## 📝 Daily Record

%%💡 **Stress-free Recording**: Record any thoughts, tasks, or flashes of insight. **Key Action**: Be sure to tag each record with the corresponding **#topic tag** (e.g., `#project-name`, `#personal-growth`). The system will automatically aggregate them into topic notes%%

- <% tp.date.now("HH:mm") %> Plan the day #work/time-mgmt

## ⏰ Habits
%%Habit will not be counted as a task%%
- [ ] Drink a glass of water after wake up
- [ ] Breakfast
- Drink water
	- [ ] +1
	- [ ] +1
	- [ ] +1
	- [ ] +1
	- [ ] +1
	- [ ] +1
- [ ] Project time statistics

## 📊 Energy Allocation
%%Today's project list, according to the time consumed, automatic statistics project time consumed percentage%%
```LifeOS
ProjectListByTime
```

## ✅ Today's Completed
%%List of tasks completed today, extracted from all notes%%
```LifeOS
TaskDoneListByTime
```
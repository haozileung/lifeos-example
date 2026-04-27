# Tasks

## Focus
>
> Important || In progress || Due in 7 days || High priority

```tasks
folder includes 0.PeriodicNotes
path does not include Templates
not done
(status.name includes Important) OR (status.name includes In Progress) OR (priority is high) OR (due before in 7 days)
group by due
```

## PARA

```tasks
(folder includes 1.Projects) OR (folder includes 2.Areas) OR (folder includes 3.Resources)
filename regex does not match /Template/
not done
group by folder
```

## PeriodicNotes

```tasks
folder includes 0.PeriodicNotes
path does not include Templates
not done
sort by filename reverse
```

## Cancelled

```tasks
(folder includes 0.PeriodicNotes) OR (folder includes 1.Projects)
filename regex does not match /Template/
status.name includes Cancelled
group by folder
```

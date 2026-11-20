# 📋 Obsidian Tasks Plugin Comprehensive Reference & Syntax Guide

The **Obsidian Tasks** plugin (`obsidian-tasks-group/obsidian-tasks`) enables vault-wide task tracking, recurring schedules, priority weights, task dependencies, and rich query blocks directly inside plain-text Markdown notes.

---

## 1. 🏷️ In-Line Task Formats

Tasks uses signifier emojis to embed metadata into standard Markdown checkboxes (`- [ ]`).

### Standard Emoji Signifiers
| Signifier | Meaning | Syntax Example | Notes |
| :--- | :--- | :--- | :--- |
| `📅` | **Due Date** | `📅 2026-11-05` | The date by which the task must be completed |
| `⏳` | **Scheduled Date** | `⏳ 2026-11-04` | The date on which you plan to work on it |
| `🛫` | **Start Date** | `🛫 2026-11-01` | The earliest date the task can be started |
| `➕` | **Created Date** | `➕ 2026-10-31` | Automatically appended upon task creation |
| `✅` | **Done Date** | `✅ 2026-11-02` | Automatically added when checkbox is ticked |
| `❌` | **Cancelled Date**| `❌ 2026-11-02` | Marked when task is cancelled (`- [-]`) |
| `🔁` | **Recurrence** | `🔁 every day` | Defines repeating schedule rules |
| `🆔` | **Task ID** | `🆔 task-a1` | Unique alphanumeric identifier for dependencies |
| `⛔` | **Depends On** | `⛔ task-a1,task-b2` | Prerequisite task IDs that block this task |
| `🏁` | **On Completion**| `🏁 delete` | Action upon completion (`delete` or `keep`) |

---

## 2. 🔺 Priority Weights
Priority emojis can appear anywhere on the task line:
| Priority | Signifier | Markdown Syntax Example |
| :--- | :---: | :--- |
| **Highest** | `🔺` | `- [ ] #task Urgent surgery review 🔺 📅 2026-11-02` |
| **High** | `⏫` | `- [ ] #task Complete mock exam ⏫ 📅 2026-11-03` |
| **Medium** | `🔼` | `- [ ] #task Review pharmacology flashcards 🔼` |
| **Normal** | *(none)* | `- [ ] #task Read standard syllabus chapter` |
| **Low** | `🔽` | `- [ ] #task Organize study desk 🔽` |
| **Lowest** | `⏬` | `- [ ] #task Archive old notes ⏬` |

---

## 3. 🔁 Recurrence Rules

Recurrence is specified using natural language patterns following `🔁`:
- `🔁 every day`
- `🔁 every weekday`
- `🔁 every 2 weeks on Monday, Wednesday, Friday`
- `🔁 every month on the 1st`
- `🔁 every 3 months on the last Friday`
- `🔁 every year`
- **When Done**: Append `when done` to calculate the next occurrence from the completion date rather than the scheduled date:
  ```markdown
  - [ ] Take Vitamin D3 supplement 🔁 every 7 days when done 📅 2026-11-01
  ```

---

## 4. 🔗 Task Dependencies (Blockers & Blocked-by)

Tasks supports DAG (Directed Acyclic Graph) task chains using `🆔` and `⛔`:
```markdown
- [ ] Read Chapter 4: Cardiovascular Pathology 🆔 cardio-ch4
- [ ] Complete Cardiovascular MCQs ⛔ cardio-ch4 🆔 cardio-mcq
- [ ] Analyze Cardiovascular Mock Exam Errors ⛔ cardio-mcq
```

---

## 5. 🔍 Query Engine (` ```tasks ` Codeblock)

Queries are executed inside fenced `tasks` code blocks. Every line is an instruction (filter, sort, group, layout, or script).

### A. Core Filters
```tasks
# Status filters
not done
done
status.type is TODO
status.type is IN_PROGRESS

# Date filters (Supports relative keywords: today, tomorrow, yesterday, this week, next month)
due before tomorrow
due today
due in or before 2026-11-07
no due date
has scheduled date
starts on or before today

# Path and File filters
path includes 03_Habits_Protocols
filename does not include Template
heading includes Morning Routine

# Tag and Description filters
description includes revision
tag includes #exam
no tags

# Dependency filters
is not blocked
is blocking
```

### B. Boolean Operators
Combine filters with parenthesized Boolean expressions:
```tasks
(priority is high) OR (due before today)
(tag includes #critical) AND NOT (path includes 99_Archive)
```

### C. Grouping Directives
Group tasks visually into accordion collapsible sections:
```tasks
group by priority
group by status.type
group by due
group by folder
group by filename
group by recurrence
```

### D. Sorting Directives
Order tasks deterministically:
```tasks
sort by priority
sort by due
sort by scheduled
sort by path
sort by description reverse
```

### E. View & Layout Configuration
```tasks
# View modes
short mode                  # Compact one-line representation
full mode                   # Default extended layout

# Element toggles
hide tags
hide due date
hide scheduled date
hide backlink
hide edit button
hide postpone button
hide task count

# Pagination / Limits
limit to 20 tasks
limit groups to 5 tasks
```

---

## 6. 💡 Complete Production Tasks Query Example

```tasks
not done
is not blocked
(due on or before today) OR (priority is high)
path does not include Archive
sort by priority
sort by due
group by folder
short mode
hide postpone button
```

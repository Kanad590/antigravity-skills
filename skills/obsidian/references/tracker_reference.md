# 📈 Obsidian Tracker Plugin Comprehensive Reference & Syntax Guide

The **Obsidian Tracker** plugin (`pyrochlore/obsidian-tracker`) extracts numeric metrics, habit completions, tags, frontmatter fields, and Dataview inline fields across notes to generate line charts, bar plots, monthly calendars, bullet charts, and statistical summaries.

---

## 1. ⚙️ Root Parameters

Code blocks use the fenced language `tracker`:
```tracker
searchType: <type>
searchTarget: <target>
folder: <folder_path>
startDate: <start_date>
endDate: <end_date>
<view_type>:
  <view_parameters>
```

### Supported `searchType` Options
| `searchType` | Target Data Source | `searchTarget` Syntax Example |
| :--- | :--- | :--- |
| `frontmatter` | Numeric or string YAML properties | `sleep_hours` (matches `sleep_hours: 7.5`) |
| `frontmatter.exists` | Checks presence of YAML key (1 or 0) | `morning_sunlight` |
| `frontmatterlist` | Specific element inside a YAML array | `habits[yoga]` |
| `dvField` | Dataview inline key-value pairs (`key:: value`)| `pages_read` (matches `pages_read:: 25`) |
| `tag` | Tag frequency or numeric value after colon | `weight` (matches `#weight` or `#weight:72`) |
| `task.done` | Checkbox tasks completed (`- [x]`) | `Morning NSDR` |
| `task.notdone`| Uncompleted tasks (`- [ ]`) | `Evening Stretches` |
| `text` | Regular expression with named capture group | `'walked\s+(?<value>[0-9]+)\s+steps'` |
| `fileMeta` | File properties (`numWords`, `size`, `mDate`) | `numWords` |

---

## 2. 📅 Date & Scope Configuration

- **`folder`**: Path to target notes (e.g. `00_Dashboard/Daily_Notes`).
- **`startDate`**:
  - Absolute: `2026-10-01`
  - Relative: `-30d` (past 30 days), `-12w` (past 12 weeks), `-6m` (past 6 months)
- **`endDate`**: `0d` (today) or fixed date `2026-10-31`.
- **`dateFormat`**: Moment.js format matching note titles (default: `YYYY-MM-DD`).

---

## 3. 📊 Visual Representation Types

### A. Line Chart (`line:`)
```tracker
searchType: frontmatter
searchTarget: deep_work_hours
folder: Daily_Notes
startDate: -30d
endDate: 0d
line:
  title: "Deep Work Hours (Last 30 Days)"
  yAxisLabel: "Hours"
  lineColor: "#38bdf8"
  showPoint: true
  pointColor: "#0284c7"
  yMin: 0
  yMax: 10
```

### B. Bar Chart (`bar:`)
```tracker
searchType: frontmatter
searchTarget: sleep_hours
folder: Daily_Notes
startDate: -14d
endDate: 0d
bar:
  title: "Sleep Duration"
  yAxisLabel: "Hours"
  barColor: "#a855f7"
  yMin: 0
```

### C. Monthly Habit Calendar (`month:`)
Generates a monthly grid showing completed days and streak heatmaps:
```tracker
searchType: task.done
searchTarget: Morning Sunlight & Hydration
folder: Daily_Notes
startDate: 2026-11-01
endDate: 2026-11-30
month:
  startWeekOn: Mon
  color: "#22c55e"
  colorByStreak: true
```

### D. Bullet Graph (`bullet:`)
Compares actual metrics against target ranges:
```tracker
searchType: frontmatter
searchTarget: mock_exam_score
folder: Exam_Tracker
bullet:
  title: "Mock Score Benchmark"
  dataset: 0
  range: [0, 60, 80, 100]
  rangeColor: ["#f87171", "#fbbf24", "#34d399"]
  target: 85
```

### E. Text Summary Statistics (`summary:`)
Calculates mathematical statistics over the dataset:
```tracker
searchType: frontmatter
searchTarget: focus_hours
folder: Daily_Notes
startDate: -30d
endDate: 0d
summary:
  template: "📊 Focus Summary (Last 30 Days):\n- Total Hours: {{sum()}} hrs\n- Daily Average: {{average()}} hrs\n- Peak Day: {{max()}} hrs\n- Current Streak: {{currentStreak()}} days\n- Max Streak: {{maxStreak()}} days"
```

---

## 4. 🔀 Multi-Dataset Tracking
Track multiple metrics simultaneously by providing comma-separated lists:
```tracker
searchType: frontmatter, frontmatter
searchTarget: focus_hours, sleep_hours
folder: Daily_Notes
startDate: -30d
endDate: 0d
line:
  title: "Focus vs Sleep Correlation"
  lineColor: "#38bdf8, #f43f5e"
  yAxisLabel: "Hours"
```

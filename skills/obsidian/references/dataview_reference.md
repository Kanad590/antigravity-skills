# 📊 Dataview Plugin Comprehensive Reference & Query Guide

The **Dataview** community plugin (`blacksmithgu/obsidian-dataview`) turns an Obsidian vault into a high-performance in-memory database. It indexes frontmatter YAML properties, tags, file system metadata, and inline fields across all Markdown documents.

---

## 1. 🔍 Query Types (DQL)

Dataview supports four primary query formats:
1. `TABLE [field1], [field2] ...`
2. `LIST [field]`
3. `TASK`
4. `CALENDAR [dateField]`

### Basic Structure:
```dataview
TABLE file.mtime AS "Modified", tags AS "Tags", status AS "Status"
FROM "03_Habits_Protocols" OR #protocol
WHERE status = "active" AND file.name != "Template"
SORT file.mtime DESC
LIMIT 20
```

---

## 2. 📋 Native TASK Queries

> [!important]
> When external task plugins are not installed, Dataview's native `TASK` query handles task tracking with complete filtering, grouping, and checkbox states.

### Uncompleted Tasks in Vault or Folder
```dataview
TASK
FROM "03_Habits_Protocols" OR "00_Dashboard"
WHERE !completed
SORT file.name ASC
```

### Group Tasks by Source Note
```dataview
TASK
FROM #protocol OR #routine
WHERE !completed
GROUP BY file.link
```

### Tasks Tagged with Specific Keywords
```dataview
TASK
WHERE contains(text, "#critical") AND !completed
```

---

## 3. 📑 Inline Metadata Fields

Dataview allows embedding structured metadata anywhere within body text:

| Inline Format | Syntax | Preview Display | Best Use Case |
| :--- | :--- | :--- | :--- |
| **Visible Key-Value** | `author:: [[Cal Newport]]` | `author: Cal Newport` | Body paragraphs, book notes |
| **Bracketed (Key Hidden)** | `[status:: in-progress]` | `in-progress` | Clean tables, list items |
| **Parenthesized** | `(priority:: 1)` | `(priority: 1)` | Compact note headers |

Querying inline fields in DQL is identical to querying YAML frontmatter properties.

---

## 4. ⚙️ Operators & Built-In Functions

### Logical & Comparison
- `AND`, `OR`, `NOT`, `!`, `=`, `!=`, `<`, `>`, `<=`, `>=`

### Array & String Functions
- `contains(field, "text")`: Checks if string or list contains value.
- `length(list)`: Item count.
- `join(list, ", ")`: Concatenates list elements.
- `lower(str)` / `upper(str)`: String casing.
- `regexmatch("pattern", str)`: Regex testing.
- `default(field, "Fallback")`: Replaces null/empty with fallback value.
- `choice(condition, trueVal, falseVal)`: Ternary conditional.

### Date Functions & Calculations
- `date(today)`: Current date.
- `file.mtime`: File modification datetime.
- `file.ctime`: File creation datetime.
- `file.day`: Date parsed from filename (e.g. `2026-10-25`).
- `date(today) - file.mtime < dur(7 days)`: Files edited in the last 7 days.

---

## 5. 🔤 Inline Dataview Queries

Dataview allows embedding dynamic values directly into body text:
- `= this.file.name`: Current file's title.
- `= this.file.size`: Current file's size in bytes.
- `= length(this.file.outlinks)`: Number of outgoing wikilinks.
- `= default(this.status, "In Progress")`: Dynamic status fallback.
- `$= moment().format("dddd, MMMM Do YYYY")`: Inline DataviewJS execution.

---

## 6. 💻 DataviewJS Scripting API (` ```dataviewjs `)

For complex logic, DataviewJS exposes the full JavaScript environment and the `dv` object:

### Common API Methods:
- `dv.pages(source)`: Returns DataArray of page objects matching query source (`"folder"`, `#tag`, etc.).
- `dv.page(path)`: Returns a single page object for a given path.
- `dv.table(headers, rows)`: Renders a structured HTML table.
- `dv.list(elements)`: Renders an unordered bullet list.
- `dv.taskList(tasks, groupByFile?)`: Renders an interactive task checklist.
- `dv.header(level, text)`: Renders an H1-H6 heading.
- `dv.span(text)` / `dv.paragraph(text)`: Renders raw text or HTML.

### DataviewJS Production Example: Interactive Habit & Task Rollup
```javascript
```dataviewjs
const habits = dv.pages('"03_Habits_Protocols"')
  .where(p => p.status === "active")
  .sort(p => p.priority, "asc");

dv.table(
  ["Habit Protocol", "Category", "Target Frequency", "Status"],
  habits.map(h => [
    h.file.link,
    h.category || "General",
    h.frequency || "Daily",
    h.status === "active" ? "🟢 Active" : "⏸️ Paused"
  ])
);
```
\```

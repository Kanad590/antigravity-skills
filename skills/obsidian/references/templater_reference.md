# ⚡ Obsidian Templater Plugin Reference & Automation Guide

The **Templater** plugin (`silentvoid13/Templater`) enables powerful dynamic template creation using JavaScript execution blocks, user prompts, system integration, file manipulation, and Moment.js date math.

---

## 1. ⚙️ Tag Syntax & Directives

Templater uses opening `<%` and closing `%>` delimiters:

| Tag Syntax | Type | Behavior | Example |
| :--- | :--- | :--- | :--- |
| `<% ... %>` | **Interpolation** | Evaluates expression and prints the result into the note | `<% tp.file.title %>` |
| `<%* ... %>` | **Execution** | Executes JavaScript statements (loops, conditions, async/await). No output unless using `tR += "..."` | `<%* if (tp.file.title.includes("Daily")) { ... } %>` |
| `<%+ ... %>` | **Dynamic** | Keeps tag intact and evaluates live each time the note renders in Preview mode | `<%+ tp.date.now("HH:mm:ss") %>` |
| `<%- ... %>` | **Left Trim** | Strips all leading whitespace and newlines before tag | `<%-\n  let x = 1;\n-%>` |
| `<% ... -%>` | **Right Trim**| Strips trailing whitespace and newlines after tag | `<% tp.date.now() -%>` |

---

## 2. 🧱 Core Internal Modules

### A. `tp.file` (File & Vault Manipulation)
- `tp.file.title`: Current note's title (without `.md`).
- `tp.file.path(relative: boolean = true)`: Full path of the file in the vault.
- `tp.file.folder(relative: boolean = true)`: Parent folder path.
- `tp.file.tags`: Array of tags associated with note.
- `tp.file.creation_date(format: string = "YYYY-MM-DD HH:mm:ss")`: File creation timestamp.
- `tp.file.last_modified_date(format: string)`: Last modification timestamp.
- `tp.file.cursor(order?: number)`: Place cursor jump point after template execution. Tab jumps between `tp.file.cursor(1)` -> `tp.file.cursor(2)`.
- `await tp.file.create_new(template, filename, open_new?, folder?)`: Create a new file from a template.
- `await tp.file.move(new_path)`: Move/rename current note into a target path.
- `await tp.file.rename(new_name)`: Rename current note.

### B. `tp.date` (Date Math & Formatting)
Built on Moment.js:
- `tp.date.now(format = "YYYY-MM-DD", offset?: number, reference?: string, ref_format?: string)`:
  - Today: `<% tp.date.now("YYYY-MM-DD") %>`
  - Yesterday: `<% tp.date.now("YYYY-MM-DD", -1) %>`
  - Next Monday: `<% tp.date.now("YYYY-MM-DD", 7) %>`
  - Parse from title: `<% tp.date.now("dddd", 0, tp.file.title, "YYYY-MM-DD") %>`
- `tp.date.yesterday(format = "YYYY-MM-DD")`
- `tp.date.tomorrow(format = "YYYY-MM-DD")`

### C. `tp.system` (Interactive User Modals & Prompts)
- `await tp.system.prompt(prompt_text, default_value?, multi_line?, throw_on_cancel?)`: Opens a text input modal.
  ```javascript
  <%* const topic = await tp.system.prompt("Enter Study Topic:", "Cardiology"); %>
  ```
- `await tp.system.suggester(text_items, return_items, throw_on_cancel?, placeholder?)`: Searchable dropdown selector.
  ```javascript
  <%*
  const categories = ["⚡ Protocol", "📚 Study Framework", "🛍️ Wardrobe", "💊 Supplement"];
  const selectedCat = await tp.system.suggester(categories, categories, false, "Select category");
  -%>
  ```
- `await tp.system.clipboard()`: Injects system clipboard contents.

### D. `tp.frontmatter` (Read Note YAML)
Access properties of the current note directly:
- `<% tp.frontmatter.status %>`
- `<% tp.frontmatter.tags[0] %>`

### E. `tp.user` (Custom JavaScript Scripts)
Run custom external scripts stored in the configured user scripts folder:
- `<% tp.user.calculateBMI(tp.frontmatter.weight, tp.frontmatter.height) %>`

---

## 3. 📝 Production Template Examples

### Example 1: Daily Protocol Log Note Template
```markdown
<%*
const dateTitle = tp.file.title;
const dayOfWeek = tp.date.now("dddd", 0, dateTitle, "YYYY-MM-DD");
-%>
---
title: "<% dateTitle %>"
date: <% dateTitle %>
day: <% dayOfWeek %>
tags:
  - daily-log
  - protocol
status: active
sleep_hours: 0
deep_work_hours: 0
energy_level: 5
---

# 📅 <% dateTitle %> (<% dayOfWeek %>)

## 🌅 Morning Habits
- [ ] 💧 Hydration + Electrolytes
- [ ] ☀️ 10-min Direct Sunlight
- [ ] 💊 Morning Supplements

## 🎯 Primary Focus Blocks
<% tp.file.cursor(1) %>

## 📊 Evening Reflection
- Wins:
- Friction / Lessons:
```

### Example 2: Active Recall Study Card Template
```markdown
<%*
const title = await tp.system.prompt("Concept / Disease Name:");
const subject = await tp.system.suggester(
  ["Medicine", "Pathology", "General Science", "Aptitude"],
  ["Medicine", "Pathology", "General Science", "Aptitude"],
  false,
  "Select Subject"
);
-%>
---
title: "<% title %>"
subject: "<% subject %>"
tags:
  - active-recall
  - flashcards/<% subject.toLowerCase() %>
last_reviewed: <% tp.date.now("YYYY-MM-DD") %>
sr-due: <% tp.date.now("YYYY-MM-DD") %>
sr-interval: 1
sr-ease: 250
---

# 🧠 <% title %>

> [!question]- ❓ Core Definition & Mechanism
> <% tp.file.cursor(1) %>

> [!tip]- 🎯 Clinical Presentation & High-Yield Triggers
> <% tp.file.cursor(2) %>

> [!danger]- ⚠️ Contraindications / Critical Pitfalls
> <% tp.file.cursor(3) %>
```

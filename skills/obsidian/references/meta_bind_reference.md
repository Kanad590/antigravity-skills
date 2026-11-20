# 🎛️ Obsidian Meta Bind Plugin Comprehensive Reference & Syntax Guide

The **Meta Bind** plugin (`mprojectscode/obsidian-meta-bind-plugin`) turns Obsidian notes into dynamic interactive applications with live two-way data-bound form controls (sliders, toggles, text fields, drop-down menus, date pickers) and buttons that directly modify YAML frontmatter properties.

---

## 1. 🔲 Inline Input Fields (`INPUT[...]`)

Input fields bind directly to a YAML frontmatter property in the current note (or a target file using `path/to/file#property`).

### Syntax Specification
```markdown
INPUT[<inputType>(<arguments>):<bindTarget>]
```

| Input Type | Syntax Example | YAML Type | Description |
| :--- | :--- | :---: | :--- |
| **Toggle** | `INPUT[toggle:is_completed]` | `boolean` | Checkbox toggle switch (`true`/`false`) |
| **Slider** | `INPUT[slider(min=1, max=10, step=1):energy_rating]` | `number` | Numeric interactive slider |
| **Text** | `INPUT[text(placeholder="Enter notes..."):summary]` | `string` | Single-line text input |
| **Number** | `INPUT[number:focus_hours]` | `number` | Numerical spinbox input |
| **Date** | `INPUT[date:review_date]` | `date` | Native date picker popup |
| **Time** | `INPUT[time:wake_up_time]` | `string` | 24-hour time picker |
| **Select** | `INPUT[select(option("todo", "To Do"), option("done", "Completed")):status]` | `string` | Dropdown selection menu |
| **Inline Select**| `INPUT[inlineSelect(option("High", 🔴 High), option("Low", 🟢 Low)):priority]` | `string` | Compact inline dropdown |
| **Progress Bar**| `INPUT[progressBar(min=0, max=100):progress]` | `number` | Visual progress bar indicator |
| **Inline List** | `INPUT[inlineList:tags]` | `list` | Tag/list element editor |

---

## 2. 👁️ Metadata Views (`VIEW[...]`)

Render frontmatter values dynamically in the note body. Any change made via an `INPUT` immediately updates all `VIEW` fields in real time.

### Syntax Specification
```markdown
VIEW[{<expression>}]
```

- **Simple Property Display**: `Current status: VIEW[{status}]`
- **Computed Math Expressions**:
  ```markdown
  Total Cost: ₹VIEW[{quantity} * {unit_price}]
  BMI: VIEW[Math.round({weight} / (({height}/100) * ({height}/100)))]
  ```
- **Conditional Text**:
  ```markdown
  VIEW[{is_completed} ? "✅ Task Completed" : "⏳ Pending Action"]
  ```

---

## 3. 🔘 Buttons (`meta-bind-button`)

Buttons execute discrete operations such as updating YAML properties, executing Obsidian commands, opening files, or running scripts.

### A. Codeblock Button Definition
```meta-bind-button
id: complete-daily-habit
label: Mark Habit Complete
icon: check-circle
style: primary
class: ""
hidden: false
actions:
  - type: updateMetadata
    bindTarget: status
    evaluate: false
    value: "done"
  - type: updateMetadata
    bindTarget: completed_at
    evaluate: true
    value: "moment().format('YYYY-MM-DD HH:mm')"
  - type: command
    command: app:save-current-file
```

### B. Supported Action Types
1. **`updateMetadata`**:
   - `bindTarget`: Target property name (e.g. `status` or `habits.water`).
   - `evaluate`: Boolean (`true` evaluates JavaScript expression, `false` treats `value` as literal).
   - `value`: Target value.
2. **`command`**:
   - `command`: Command ID (found via Command Palette or plugin developer tools).
3. **`open`**:
   - `link`: Vault wikilink or external URL (`[[Dashboard]]` or `https://google.com`).
4. **`js`**:
   - `file`: Path to external JavaScript file to run.

### C. Inline Button Rendering
Reference a button anywhere in your text by its unique `id`:
```markdown
Click here to finish: BUTTON[complete-daily-habit]
```

---

## 4. 💡 Full Interactive Note Architecture Example

```yaml
---
title: "Deep Work Session Protocol"
session_type: "Focused Coding"
energy_level: 8
duration_minutes: 90
completed: false
date: 2026-11-01
---

# ⚡ Focus Session Controller

Type: INPUT[inlineSelect(option("Focused Coding", 💻 Coding), option("Exam Aptitude", 📚 Aptitude), option("Active Recall", 🧠 Recall)):session_type]
Energy Level: INPUT[slider(min=1, max=10):energy_level] (Rating: VIEW[{energy_level}] / 10)
Target Duration: INPUT[number:duration_minutes] mins

Done: INPUT[toggle:completed] Status: VIEW[{completed} ? "🏆 Session Complete" : "⏳ Session Active"]

```meta-bind-button
id: finish-session
label: Complete & Archive Session
style: success
actions:
  - type: updateMetadata
    bindTarget: completed
    value: true
  - type: command
    command: app:save-current-file
```
BUTTON[finish-session]
```

# 🔘 Obsidian Buttons Plugin Reference & Syntax Guide

The **Buttons** plugin (`shabegom/buttons`) adds clickable, customizable action buttons to notes, triggering commands, inserting templates, opening URLs, or evaluating calculations.

---

## 1. ⚙️ Codeblock Syntax

Buttons are constructed inside `button` code blocks using whitespace-separated key-value lines:

```button
name <Button Label>
type <Action Type>
action <Target Command, Template, or URL>
color <Color Name>
```

---

## 2. 🎛️ Supported Button Types

| Type | Action Purpose | Action Example |
| :--- | :--- | :--- |
| `command` | Triggers an Obsidian Command Palette command | `action Open today's daily note` |
| `link` | Opens a web URL or internal Obsidian URI | `action https://google.com` or `action obsidian://vault/...` |
| `template` | Appends or inserts a note template | `action Templates/Study_Review_Card.md` |
| `text` | Appends raw text at cursor or note end | `action - [ ] New uncompleted habit item` |
| `calculate`| Evaluates an arithmetic expression | `action 125 * 1.18` |

---

## 3. 🎨 Visual Colors & Styling Modifiers

- **Available Colors**: `blue`, `green`, `red`, `purple`, `yellow`, `default`
- **Modifiers**:
  - `templater true`: Forces Templater parser to evaluate dynamic tags in the injected template.
  - `remove true`: Destroys the button after it is clicked once (useful for setup wizards or single-use workflows).
  - `class custom-button-style`: Applies a custom CSS class.

---

## 4. 💡 Practical Workflow Examples

### A. Quick Daily Log Launcher
```button
name 🌅 Open Today's Journal
type command
action Daily notes: Open today's daily note
color blue
```

### B. Append Study Task Button
```button
name ➕ Add Revision Task
type template
action 05_Templates/Revision_Task_Snippet.md
templater true
color green
```

# 📋 Obsidian Kanban Plugin Syntax & Architecture Reference

The `obsidian-kanban` plugin converts standard Markdown files into interactive drag-and-drop Kanban boards while keeping all underlying content 100% plain text.

---

## 1. ⚙️ File Header & Frontmatter

To instruct Obsidian to render a note as a Kanban board, the file MUST include the `kanban-plugin` frontmatter property:

```yaml
---
kanban-plugin: basic
tags:
  - kanban
  - productivity
---
```

If the plugin is disabled or viewed on mobile without the plugin, the note cleanly falls back to standard Markdown headings and task checkboxes.

---

## 2. 🧱 Structure: Columns & Cards

### Columns
Columns are defined by Level 2 Markdown headings (`##`):
```markdown
## 🎯 Backlog / Planned
## ⚡ In Progress
## 🔬 Review / Revision
## ✅ Done / Mastered
```

### Cards
Cards are Markdown checkboxes directly under the column heading:
```markdown
## ⚡ In Progress

- [ ] Complete Oakley Focused Session on Quantitative Aptitude
- [ ] 10-Minute Sub-occipital neck stretch & NSDR
- [ ] Review Jan Aushadhi supplement timings
```

### Completed Cards
Completed cards use the standard `- [x]` markdown syntax:
```markdown
- [x] Morning Probiotic (PMBI Code 2149) + Sunlight 10 min
```

---

## 3. 🏷️ Metadata & In-Card Attributes

Obsidian Kanban parses special inline tokens to provide enhanced functionality:

1. **Due Dates**: Appended using `@{YYYY-MM-DD}` (e.g. `@{2026-10-26}`).
2. **Time Tracking**: Appended using `@{YYYY-MM-DD HH:mm}`.
3. **Tags**: Standard hashtag `#urgent`, `#afcat`, `#habit`.
4. **Wikilinks**: Full internal links work within cards (`[[Daily_Routine_Flow_Guide]]`).
5. **Card Notes / Sub-text**: Indented lines under a card list item:
   ```markdown
   - [ ] Math Practice: Ratio & Proportion
     Formula notes: [[Ratio_Formulas]]
     Target: 25 problems within 30 minutes.
   ```

---

## 4. 🗄️ Board Settings Block (Trailing Comment)

Obsidian Kanban stores board view preferences in a trailing Markdown comment block at the end of the file:

```markdown
%% kanban:settings
```json
{
  "kanban-plugin": "basic",
  "hide-tags-display": false,
  "hide-date-display": false,
  "tag-colors": [
    {"tagKey": "#urgent", "color": "#f87171"},
    {"tagKey": "#routine", "color": "#38bdf8"}
  ]
}
```
%%
```

---

## 5. 🛡️ Robustness Best Practices
- Never insert level 1 (`#`) or level 3 (`###`) headings in the card body if they conflict with column parsing.
- Keep column titles descriptive with visual emojis.
- Completed tasks should stay under their respective columns or be moved into an `## Archive` column.

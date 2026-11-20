# 🏛️ Obsidian Multi-Column Layouts Reference & Syntax Guide

Creating multi-column layouts in Obsidian allows side-by-side note comparison, dashboard structuring, and magazine-style presentation. This guide covers both the **Multi-Column Markdown** plugin (`ckrobinson/multi-column-markdown`) and Callout-based multi-column systems (`reiuyuu/obsidian-columns-callout`).

---

## 1. ⚙️ Multi-Column Markdown Syntax (`ckrobinson`)

The plugin uses clean text delimiters:

```markdown
===start-multi-column
```column-settings
Number of Columns: 2
Largest Column: standard
Border: false
Shadow: false
```
### 🧠 Cognitive Loop Slot 1
Focused study block notes and active recall triggers go here on the left side.

===column-break===

### 📊 Performance Metric
Daily sleep, hydration, and habit checkboxes align side-by-side on the right side.

===end-multi-column
```

### Configurable Column Settings
- `Number of Columns`: Integer (e.g. `2`, `3`, `4`).
- `Largest Column`: `standard`, `left`, `right`, or column index.
- `Border`: `true` / `false` (draws vertical separator line).
- `Shadow`: `true` / `false`.
- `Alignment`: `top`, `center`, `bottom`.

---

## 2. 🔲 Callout-Based Multi-Columns

If you prefer pure CSS / native callout compatibility without delimiter comments:

```markdown
> [!multi-column]
> > [!note] Left Pane (Protocol)
> > - Habit 1: Morning Sunlight
> > - Habit 2: Hydration 500ml
>
> > [!tip] Right Pane (Execution)
> > - Task 1: 45m Focused Math slot
> > - Task 2: NSDR Break
```

This guarantees 100% graceful degradation if viewed on mobile or exported to static HTML.

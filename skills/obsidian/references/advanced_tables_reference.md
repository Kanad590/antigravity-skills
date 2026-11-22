# 📑 Obsidian Advanced Tables Plugin Reference & Formula Guide

The **Advanced Tables** plugin (`tgrosinger/advanced-tables-obsidian`) provides spreadsheet-like navigation, automatic pipe alignment, sorting, and formula calculation over Markdown tables.

---

## 1. ⌨️ Core Navigation & Shortcuts

| Action | Shortcut |
| :--- | :--- |
| Move to next cell (auto-formats table) | `Tab` |
| Move to previous cell | `Shift + Tab` |
| Create new row below | `Enter` |
| Insert row above | Command Palette: *Advanced Tables: Insert row above* |
| Delete current row | Command Palette: *Advanced Tables: Delete row* |
| Sort ascending / descending by column | Command Palette: *Advanced Tables: Sort table* |

---

## 2. 🧮 Table Formula Syntax

Advanced Tables supports mathematical calculations across cells. Formulas are placed immediately following the table inside an HTML comment:

```markdown
<!-- tbl-formulas: <formula_1>; <formula_2> -->
```

### Coordinate System
- **Columns**: `c1`, `c2`, `c3` (1-based index)
- **Rows**: `r1`, `r2`, `r3` (Row 1 is the header; Row 2 is the first data row)
- **Cell**: `r2c3` (Row 2, Column 3)
- **Ranges**: `c2:c5` (Column 2 through 5 in current row) or `r2c2:r5c2` (Column 2 across rows 2 to 5)

### Built-in Functions
- `SUM(range)`: Sum of values
- `AVERAGE(range)`: Arithmetic mean
- `MIN(range)` / `MAX(range)`: Minimum and maximum
- `COUNT(range)`: Number of numerical entries
- `round(value, decimals)`: Precision rounding

---

## 3. 💡 Formula Table Example

```markdown
| Item Description | Quantity | Unit Price (₹) | Total (₹) |
| :--- | :---: | :---: | :---: |
| Ashwagandha 500mg | 2 | 120 | 240 |
| Vitamin D3 60k IU | 4 | 35 | 140 |
| Probiotic Capsules | 1 | 280 | 280 |
| **Total Expenditure** | | | **660** |
<!-- tbl-formulas: r2c4 = r2c2 * r2c3; r3c4 = r3c2 * r3c3; r4c4 = r4c2 * r4c3; r5c4 = sum(r2c4:r4c4) -->
```

---

## 4. 🛡️ Critical Table Rules for Vault Health

> [!danger] **Never Escape Pipes in Wikilinks Inside Tables**
> When inserting image embeds or aliased internal links into table cells, write:
> `![[sample.png|150]]` or `[[Target Note|Custom Label]]`
> 
> **NEVER** write `![[sample.png\|150]]` or `[[Target Note\|Custom Label]]`. 
> While legacy Markdown parsers occasionally escaped pipes inside tables, Obsidian's link parser treats the backslash as a literal part of the target filename, failing to find `sample.png|150` on disk.

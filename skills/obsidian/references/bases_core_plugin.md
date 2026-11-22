# 🗄️ Obsidian Bases (Core Plugin) Reference

Introduced in Obsidian v1.8, **Bases** is a core plugin providing native, real-time database views over vault notes using their YAML frontmatter properties. Unlike community plugins, Bases is built directly into Obsidian's core engine, rendering fast interactive tables, cards, lists, and calendar views without external dependencies.

---

## 1. 🏗️ How Bases Works

A Base is a file (typically with a `.base` or markdown embed) that monitors a collection of notes based on folder paths or tag filters.

### Key Concepts:
1. **Source**: Defines which notes are included (`folder: "04_Fashion_Grooming"` or `tag: "#protocol"`).
2. **Properties Schema**: Automatically infers note properties (text, number, date, list, checkbox) from YAML frontmatter.
3. **Views**: Multiple presentations of the same data:
   - **Table View**: Rows represent notes, columns represent properties.
   - **Card / Gallery View**: Visual grid displaying cover images and key summary fields.
   - **List View**: Compact sequential view.
   - **Kanban / Board View**: Groups notes by a single property (e.g. `status: [todo, in-progress, done]`).

---

## 2. 📝 Frontmatter Standards for Base Compatibility

To ensure any markdown note seamlessly renders in a Base view:
```yaml
---
title: "Morning Sunlight & Hydration"
status: "active"
category: "Habit"
priority: 1
energy_level: "high"
tags:
  - protocol
  - routine
last_reviewed: 2026-10-25
---
```

### Best Practices for Property Types:
- **Status / Enum**: Use consistent lowercase strings (`active`, `backlog`, `done`).
- **Numbers / Metrics**: Use raw integers or floats without currency symbols or units in the YAML field (`cost: 120` instead of `cost: ₹120`). Display format can be styled in the view.
- **Dates**: Use ISO-8601 strings (`YYYY-MM-DD`).
- **Images**: Reference vault attachments cleanly (`cover: "Attachments/Kanad_Autumn_Portrait.jpg"`).

---

## 3. 🔄 Interoperability: Bases vs Dataview

| Feature | Obsidian Bases (Core) | Dataview (Community Plugin) |
| :--- | :--- | :--- |
| **Dependency** | None (Native Core Plugin) | Community Plugin (`dataview`) |
| **Editing** | Direct inline property editing in cell | Read-only rendering (requires MetaEdit to write) |
| **Complex Queries** | GUI filters & sorting | Full DQL / SQL-like query language |
| **Computation** | Basic aggregation (count, sum, avg) | Complex custom JS (`dataviewjs`), regex, string manipulation |
| **Mobile Speed** | Instant native load | Script execution overhead |

**Guideline**: Use **Bases** for interactive property updates, daily logging, and visual board views; use **Dataview** for complex cross-folder MOCs, nested task rollups, and dynamic document generation.

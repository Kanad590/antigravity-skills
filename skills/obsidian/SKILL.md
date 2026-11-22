---
name: obsidian
description: >-
  Use this skill whenever working with Obsidian vaults, advanced Markdown syntax, Callouts,
  Dataview DQL & DataviewJS, Obsidian Tasks, Templater, Meta Bind, Tracker, Charts, Excalidraw,
  Canvas (.canvas), Kanban, Breadcrumbs, Spaced Repetition (SRS), Advanced Tables, Multi-Column layouts,
  or vault automation, linting, and knowledge graph structuring. Also triggered by the /obsidian command.
---

# 💎 Obsidian Vault Engineering & Plugin Syntax Master Skill

This skill provides an exhaustive, production-grade guide and programmatic toolset for architecting, querying, visualising, automating, and maintaining high-performance **Obsidian** vaults. It covers the full syntax, code blocks, frontmatter schemas, and formatting rules of the Obsidian core engine and top community plugins.

---

## 🚀 Quick Reference Commands & Tooling

Tool | Purpose | Command
:--- | :--- | :---
**Syntax Helper** | Generate verified plugin syntax & code blocks | `python3 ~/.agents/skills/obsidian/scripts/plugin_syntax_helper.py <plugin> [options]`
**Vault Linter** | Check frontmatter, syntax, broken embed pipes | `python3 ~/.agents/skills/obsidian/scripts/vault_linter.py <vault_path>`
**Auto-Fix Linter** | Automatically repair escaped pipes (`\|` -> `|`) | `python3 ~/.agents/skills/obsidian/scripts/vault_linter.py <vault_path> --fix`
**Link Auditor** | Audit broken wikilinks, missing images, orphans | `python3 ~/.agents/skills/obsidian/scripts/link_auditor.py <vault_path>`
**DQL Generator** | Generate Dataview DQL query snippets | `python3 ~/.agents/skills/obsidian/scripts/dql_generator.py <type> [options]`
**Canvas Builder** | Programmatically generate `.canvas` mind-maps | `python3 ~/.agents/skills/obsidian/scripts/canvas_builder.py <out.canvas>`

---

## 📑 Master Plugin Syntax Cheat Sheet

| Plugin | Downloads | Syntax Delimiter / Codeblock | Key Directives / Tokens | Reference Guide |
| :--- | :---: | :--- | :--- | :--- |
| **Dataview** | 5.2M | ````dataview```` / ````dataviewjs```` | `TABLE`, `TASK`, `LIST`, `FROM`, `WHERE`, `FLATTEN`, `GROUP BY`, inline `key:: value`, `[key:: value]`, `$= ...` | [dataview_reference.md](./references/dataview_reference.md) |
| **Tasks** | 4.5M | ````tasks```` & Checkbox emojis | `📅` Due, `⏳` Sched, `🛫` Start, `➕` Created, `✅` Done, `🔁` Repeat, `🆔` ID, `⛔` Depends, `🔺` Priority | [tasks_plugin_reference.md](./references/tasks_plugin_reference.md) |
| **Templater** | 6.0M | `<% ... %>`, `<%* ... %>`, `<%+ ... %>` | `tp.file.*`, `tp.date.now()`, `tp.system.prompt()`, `tp.system.suggester()`, `tp.frontmatter.*` | [templater_reference.md](./references/templater_reference.md) |
| **Meta Bind** | 590K | `INPUT[...]`, `VIEW[...]`, ````meta-bind-button```` | `INPUT[toggle:prop]`, `INPUT[slider(...):prop]`, `INPUT[select(...):prop]`, `VIEW[{prop}]`, `BUTTON[id]` | [meta_bind_reference.md](./references/meta_bind_reference.md) |
| **Tracker** | 370K | ````tracker```` | `searchType` (frontmatter, dvField, tag, task.done), `searchTarget`, `line:`, `bar:`, `month:`, `summary:` | [tracker_reference.md](./references/tracker_reference.md) |
| **Charts** | 334K | ````chart```` | `type: bar/line/pie/radar`, `labels: [...]`, `series: [{title, data}]`, `window.renderChart()` | [charts_reference.md](./references/charts_reference.md) |
| **Spaced Repetition**| 625K | `Q::A`, `T:::D`, `Q \n ? \n A`, `==cloze==` | `#flashcards`, `#flashcards/deck`, `==hidden::hint==`, frontmatter: `sr-due`, `sr-interval`, `sr-ease` | [spaced_repetition_reference.md](./references/spaced_repetition_reference.md) |
| **Kanban** | 2.8M | `kanban-plugin: basic` | Columns: `## Heading`, Cards: `- [ ] Card @{YYYY-MM-DD}`, Settings: `%% kanban:settings ... %%` | [kanban_plugin_reference.md](./references/kanban_plugin_reference.md) |
| **Excalidraw** | 8.8M | `excalidraw-plugin: parsed` | Embed: `![[drawing.excalidraw|500]]`, Area crop: `![[drawing.excalidraw#^area=Frame]]`, live transclusion | [excalidraw_reference.md](./references/excalidraw_reference.md) |
| **Canvas** | Core | `.canvas` JSON | Nodes (`text`, `file`, `group`), coordinates `(x, y, width, height)`, chromatic tags `"1"` to `"6"`, edges | [canvas_specification.md](./references/canvas_specification.md) |
| **Breadcrumbs** | 429K | ````breadcrumbs```` & Inline fields | `up:: [[Parent]]`, `down:: [[Child]]`, `same:: [[Sibling]]`, `next:: [[Next]]`, `prev:: [[Prev]]`, `type: tree/mermaid` | [breadcrumbs_reference.md](./references/breadcrumbs_reference.md) |
| **Buttons** | 492K | ````button```` | `name <Label>`, `type <command/link/template/text>`, `action <Target>`, `color <blue/green/red>` | [buttons_reference.md](./references/buttons_reference.md) |
| **Advanced Tables**| 3.3M | Markdown Tables + Formulas | `Tab` / `Enter` navigation, formula comments: `<!-- tbl-formulas: r2c4 = r2c2 * r2c3; ... -->` | [advanced_tables_reference.md](./references/advanced_tables_reference.md) |
| **Multi-Column**| 224K | Delimiters & Callouts | `===start-multi-column`, ````column-settings````, `===column-break===`, `===end-multi-column` | [multi_column_reference.md](./references/multi_column_reference.md) |
| **Bases (Core)**| Core 1.8+ | Native `.base` or YAML views | Real-time database table, card gallery, list, and board views over vault note frontmatter properties | [bases_core_plugin.md](./references/bases_core_plugin.md) |
| **Admonition** | 1.0M | ````ad-<type>```` & Callouts | `title: <String>`, `collapse: open/closed`, `color: R, G, B` -> Converts directly to native `> [!type]` | [admonition_reference.md](./references/admonition_reference.md) |
| **Zotero Integration** | 1.5M | Nunjucks `{{ ... }}`, `{% ... %}` | `{{title}}`, `{{annotations}}`, `annot.annotatedText`, `annot.comment`, `annot.desktopURI`, Port `23119` | [zotero_integration_reference.md](./references/zotero_integration_reference.md) |

---

## 🛠️ Core Architectural Disciplines

### 1. Active Recall & Progressive Disclosure Callouts
When writing notes for study, cognition, or revision:
- **Collapsed by default (`-`)**: Enforces active recall:
  ```markdown
  > [!question]- ❓ Question: What causes cerebellar study fatigue?
  > Prolonged forward head tilt causes chronic spasms in the sub-occipital muscles, impinging blood flow.
  ```
- **Expanded by default (`+`)**: Collapsible context that remains visible on load:
  ```markdown
  > [!info]+ 📌 Core Protocol Framework
  > Summary points visible immediately, can be collapsed when reviewing details.
  ```
- **Chromatic Codes**:
  - `> [!danger]` (Red / `"1"`): Critical warnings, contraindications, motive.
  - `> [!tip]` / `> [!question]` (Orange / `"2"`): Study hacks, flashcard questions, actionable items.
  - `> [!warning]` (Yellow / `"3"`): Prerequisites, caveats, attention points.
  - `> [!success]` (Green / `"4"`): Verified results, health, nutrition, completed milestones.
  - `> [!info]` (Cyan-Blue / `"5"`): Systematic frameworks, daily protocols, routines.
  - `> [!note]` (Purple / `"6"`): Aesthetics, luxury styling, wardrobe combinations.

### 2. Embeds & Table Rules (Zero Broken Pipes)
- In standard notes: `![[image.jpg|250]]`
- **Inside Markdown Tables**: NEVER escape the pipe (`![[image.jpg\|250]]` is INVALID). Use `![[image.jpg|250]]` directly. Backslashing breaks Obsidian's link resolver.

### 3. Native Task & Dataview DQL Synergy
Standard Markdown tasks (`- [ ]`) work seamlessly across both Dataview and Tasks:
```dataview
TASK
FROM "03_Habits_Protocols"
WHERE !completed
GROUP BY file.link
```

### 4. Interactive Forms with Meta Bind
Turn static dashboards into dynamic consoles:
```markdown
Energy Level: INPUT[slider(min=1, max=10):energy] (Current: VIEW[{energy}] / 10)
Status: INPUT[inlineSelect(option("active", 🟢 Active), option("done", ✅ Done)):status]
```

### 5. Habit Tracking with Obsidian Tracker
Track numeric daily values across notes without opening spreadsheets:
```tracker
searchType: frontmatter
searchTarget: focus_hours
folder: Daily_Notes
startDate: -30d
endDate: 0d
line:
  title: "Focus Hours Trend"
  yAxisLabel: "Hours"
  lineColor: "#38bdf8"
```

---

## 🔗 Zero-API-Key Ecosystem Integrations (Upgraded Tooling)

In addition to the built-in scripts in [scripts/](./scripts/), pair `/obsidian` directly with these local zero-key tools:

- **Web-to-Vault Clean Clipper ([defuddle](file:///home/saman/.gemini/config/plugins/obsidian-extras/skills/defuddle/SKILL.md)):**
  `defuddle parse "<url>" --md` strips navigation/ads and outputs clean Markdown ready to save in the vault with frontmatter and collapsed recall callouts.
- **YouTube & NotebookLM → Study Note / SRS Deck:**
  Use `youtube` (`yt-dlp` offline captions) or `notebooklm` extracts to generate structured study notes using collapsed Active Recall (`> [!question]-`) + `#flashcards` `Q::A` pairs, optionally pushing revision audio/cards via `/telegram`.
- **Upgraded `.base` & `.canvas` Specs:**
  Use [obsidian-bases](file:///home/saman/.gemini/config/plugins/obsidian-extras/skills/obsidian-bases/SKILL.md) for `.base` formulas/filters/card views, [json-canvas](file:///home/saman/.gemini/config/plugins/obsidian-extras/skills/json-canvas/SKILL.md) alongside `canvas_builder.py`, and [excalidraw-diagram](file:///home/saman/.gemini/config/plugins/visual-design/skills/excalidraw-diagram/SKILL.md) for visual study maps.
- **Live App Control (Obsidian CLI):**
  When desktop `/usr/bin/obsidian` is open, run commands directly via shell:
  ```bash
  obsidian read file="My Note"
  obsidian create name="New Note" content="# Title\nBody" template="Daily" silent
  obsidian append file="My Note" content="New item"
  obsidian search query="search term" limit=10
  obsidian daily:read
  obsidian daily:append content="- [ ] New task"
  obsidian property:set name="status" value="done" file="My Note"
  obsidian tasks daily todo
  obsidian tags sort=count counts
  obsidian backlinks file="My Note"
  # Plugin dev reload & errors:
  obsidian plugin:reload id=<plugin-id>
  obsidian dev:errors
  ```
- **Zotero Desktop & PDF Annotations ([zotero-study-manager](file:///home/saman/.gemini/config/plugins/zotero-study-manager/skills/zotero-study-manager/SKILL.md)):**
  Directly ingest PDF highlights, active recall questions, and figures from local Zotero 10 (port `23119`) using `Zotero Integration` (Nunjucks templating) and auto-map colors to study callouts (`> [!danger]`, `> [!question]`, `> [!success]`).

---

## 📚 Complete Reference Library

The `references/` directory contains deep-dive specifications with edge-case handling and complete code examples:
- [Advanced Markdown & Embeds](./references/markdown_advanced_syntax.md)
- [Dataview & DataviewJS Guide](./references/dataview_reference.md)
- [Obsidian Tasks Plugin Specification](./references/tasks_plugin_reference.md)
- [Templater Automation & API Reference](./references/templater_reference.md)
- [Meta Bind Interactive UI Specification](./references/meta_bind_reference.md)
- [Obsidian Tracker Syntax Guide](./references/tracker_reference.md)
- [Obsidian Charts & Chart.js Integration](./references/charts_reference.md)
- [Spaced Repetition (SRS) Flashcards](./references/spaced_repetition_reference.md)
- [Obsidian Kanban Boards](./references/kanban_plugin_reference.md)
- [Obsidian Canvas (.canvas) JSON Schema](./references/canvas_specification.md)
- [Excalidraw Markdown & Transclusions](./references/excalidraw_reference.md)
- [Breadcrumbs Hierarchy & Directed Graphs](./references/breadcrumbs_reference.md)
- [Buttons Plugin Reference](./references/buttons_reference.md)
- [Advanced Tables & Formula Calculations](./references/advanced_tables_reference.md)
- [Multi-Column Markdown & Callout Layouts](./references/multi_column_reference.md)
- [Admonition Codeblocks & Callouts](./references/admonition_reference.md)
- [Obsidian Bases Core Plugin](./references/bases_core_plugin.md)
- [Zotero Integration Plugin Specification](./references/zotero_integration_reference.md)

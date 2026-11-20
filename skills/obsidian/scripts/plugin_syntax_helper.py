#!/usr/bin/env python3
"""
Obsidian Plugin Syntax Helper & Codeblock Generator
Generates verified, syntactically correct code blocks, frontmatter, and inline fields
for popular Obsidian community plugins: Tasks, Dataview, Tracker, Charts, Meta Bind,
Templater, Spaced Repetition (SRS), Breadcrumbs, Buttons, Kanban, and Multi-Column.
"""

import sys
import argparse
import json

def gen_tasks(due="today", priority=None, folder=None, filter_tag=None, short_mode=True):
    lines = ["```tasks", "not done"]
    if due == "today":
        lines.append("due on or before today")
    elif due == "week":
        lines.append("due this week")
    elif due == "all":
        pass
    else:
        lines.append(f"due on or before {due}")

    if priority:
        lines.append(f"priority is {priority}")

    if folder:
        lines.append(f"path includes {folder}")

    if filter_tag:
        lines.append(f"tag includes {filter_tag}")

    lines.append("sort by priority")
    lines.append("sort by due")
    if short_mode:
        lines.append("short mode")
        lines.append("hide postpone button")
    lines.append("```")
    return "\n".join(lines)

def gen_tracker(search_type="frontmatter", target="focus_hours", folder="Daily_Notes", chart_type="line", days=30):
    if chart_type == "line":
        return f"""```tracker
searchType: {search_type}
searchTarget: {target}
folder: {folder}
startDate: -{days}d
endDate: 0d
line:
  title: "{target.replace('_', ' ').title()} ({days}-Day Trend)"
  yAxisLabel: "Value"
  lineColor: "#38bdf8"
  showPoint: true
  pointColor: "#0284c7"
```"""
    elif chart_type == "bar":
        return f"""```tracker
searchType: {search_type}
searchTarget: {target}
folder: {folder}
startDate: -{days}d
endDate: 0d
bar:
  title: "{target.replace('_', ' ').title()} Daily Metrics"
  yAxisLabel: "Value"
  barColor: "#a855f7"
```"""
    elif chart_type == "month":
        return f"""```tracker
searchType: task.done
searchTarget: {target}
folder: {folder}
month:
  startWeekOn: Mon
  color: "#22c55e"
  colorByStreak: true
```"""
    elif chart_type == "summary":
        return f"""```tracker
searchType: {search_type}
searchTarget: {target}
folder: {folder}
startDate: -{days}d
endDate: 0d
summary:
  template: "📊 Summary for {target}:\n- Total: {{{{sum()}}}}\n- Average: {{{{average()}}}}\n- Max: {{{{max()}}}}\n- Current Streak: {{{{currentStreak()}}}} days"
```"""

def gen_charts(chart_type="bar", title="Focus Distribution", labels="Mon,Tue,Wed,Thu,Fri"):
    lbl_list = [l.strip() for l in labels.split(",")]
    dummy_data = [5, 6.5, 4, 7, 8][:len(lbl_list)]
    while len(dummy_data) < len(lbl_list):
        dummy_data.append(5)
    
    return f"""```chart
type: {chart_type}
labels: {json.dumps(lbl_list)}
series:
  - title: "{title}"
    data: {json.dumps(dummy_data)}
tension: 0.3
fill: true
```"""

def gen_meta_bind(input_type="toggle", prop="status", label="Action"):
    if input_type == "toggle":
        return f"`INPUT[toggle:{prop}]`"
    elif input_type == "slider":
        return f"`INPUT[slider(min=1, max=10, step=1):{prop}]` (Value: `VIEW[{{{prop}}}]`)"
    elif input_type == "select":
        return f'`INPUT[inlineSelect(option("active", 🟢 Active), option("pending", ⏳ Pending), option("done", ✅ Done)):{prop}]`'
    elif input_type == "button":
        btn_id = f"btn_{prop}"
        return f"""```meta-bind-button
id: {btn_id}
label: "{label}"
style: primary
actions:
  - type: updateMetadata
    bindTarget: {prop}
    value: "done"
  - type: command
    command: app:save-current-file
```
BUTTON[{btn_id}]"""
    return f"`INPUT[{input_type}:{prop}]`"

def gen_templater(template_type="daily"):
    if template_type == "daily":
        return """<%*
const title = tp.file.title;
const dayOfWeek = tp.date.now("dddd", 0, title, "YYYY-MM-DD");
-%>
---
title: "<% title %>"
date: <% title %>
day: <% dayOfWeek %>
tags: [daily-log, protocol]
status: active
focus_hours: 0
energy_rating: 7
---

# 📅 <% title %> (<% dayOfWeek %>)

## 🌅 Morning Habits
- [ ] 💧 Hydration + Electrolytes
- [ ] ☀️ 10-min Direct Sunlight

## 🎯 Target Tasks
<% tp.file.cursor(1) %>
"""
    elif template_type == "recall":
        return """<%*
const concept = await tp.system.prompt("Concept / Topic:");
-%>
---
title: "<% concept %>"
tags: [active-recall, flashcards]
last_reviewed: <% tp.date.now("YYYY-MM-DD") %>
sr-due: <% tp.date.now("YYYY-MM-DD") %>
sr-interval: 1
sr-ease: 250
---

# 🧠 <% concept %>

> [!question]- ❓ Mechanism / Core Question
> <% tp.file.cursor(1) %>

> [!tip]- 🎯 Clinical / High-Yield Triggers
> <% tp.file.cursor(2) %>
"""

def gen_srs(srs_type="basic"):
    if srs_type == "basic":
        return "What is the core function of the sinoatrial (SA) node? :: Acts as the primary physiological pacemaker of the heart (~60-100 bpm)."
    elif srs_type == "reversed":
        return "Troponin T/I ::: Highly specific serum biomarkers for myocardial infarction"
    elif srs_type == "cloze":
        return "The normal resting cardiac output is approximately ==5 liters per minute==, calculated by multiplying ==heart rate== by ==stroke volume==."
    elif srs_type == "multiline":
        return """What are the primary triad signs of cardiac tamponade (Beck's triad)?
?
1. Hypotension with narrowed pulse pressure
2. Jugular venous distension (JVD)
3. Muffled / distant heart sounds"""

def gen_breadcrumbs(view_type="tree", direction="down"):
    return f"""```breadcrumbs
type: {view_type}
dir: {direction}
depth: [1, 2]
sort: basename asc
```"""

def gen_buttons(name="Open Today", btn_type="command", action="Daily notes: Open today's daily note", color="blue"):
    return f"""```button
name {name}
type {btn_type}
action {action}
color {color}
```"""

def gen_multicolumn(cols=2):
    return f"""===start-multi-column
```column-settings
Number of Columns: {cols}
Largest Column: standard
Border: false
```
### ⬅️ Column 1
Content for the left side.

===column-break===

### ➡️ Column 2
Content for the right side.

===end-multi-column"""

def gen_kanban(title="Sprint Board"):
    return f"""---
kanban-plugin: basic
tags: [kanban, project]
---

## 🎯 Backlog

- [ ] High-yield concept reading

## ⚡ In Progress

- [ ] Active Recall flashcards @{{2026-11-02}}

## ✅ Done

- [x] Morning protocol routine
"""

def gen_zotero(kind="template"):
    if kind == "macro":
        return """{%- macro calloutType(color) -%}
  {%- if color == "#ff6666" or color == "Red" -%}danger
  {%- elif color == "#5fb236" or color == "Green" -%}success
  {%- elif color == "#2ea8e5" or color == "Blue" -%}info
  {%- elif color == "#ffd400" or color == "Yellow" -%}question
  {%- elif color == "#a28ae5" or color == "Purple" -%}note
  {%- else -%}quote
  {%- endif -%}
{%- endmacro -%}"""
    elif kind == "annotation":
        return """{% for annot in annotations %}
{% if annot.type == "image" %}
> [!info] 🖼️ Diagram / Figure ([Page {{annot.pageLabel}}]({{annot.desktopURI}}))
> ![[{{annot.imageRelativePath}}]]
{% if annot.comment %}> **Note:** {{annot.comment}}{% endif %}
{% elif annot.annotatedText %}
> [!{{calloutType(annot.colorCategory)}}]- 📌 {{annot.colorCategory}} Highlight ([Page {{annot.pageLabel}}]({{annot.desktopURI}}))
> {{annot.annotatedText}}
{% if annot.comment %}
> 
> 💡 **User Note / Active Recall:**
> {{annot.comment}}
{% endif %}
{% endif %}
{% endfor %}"""
    else:
        return """---
title: "{{title}}"
citekey: "{{citekey}}"
item_type: "{{itemType}}"
year: "{{year}}"
authors: "{{authors}}"
collections: [{% for c in collections %}"{{c}}"{% if not loop.last %}, {% endif %}{% endfor %}]
zotero_link: "{{selectLink}}"
pdf_link: "{{pdfZoteroLink}}"
last_imported: "{{importDate | date('YYYY-MM-DD HH:mm')}}"
tags:
  - zotero/imported
  {% for t in tags -%}
  - "exam/{{t.tag | replace(' ', '-') | lower}}"
  {% endfor %}
---

# 📖 {{title}}

> **📌 Bibliographic Metadata:**
> • **Author(s):** {{authors}} ({{year}})
> • **Zotero Item:** [Open in Zotero]({{selectLink}}) | [Open PDF]({{pdfZoteroLink}})
> • **Collections:** {% for c in collections %}`{{c}}`{% if not loop.last %}, {% endif %}{% endfor %}

---

## 🎯 Executive Summary / Overview
{{abstractNote if abstractNote else "No abstract provided in Zotero."}}

---

## 📑 Extracted Notes & Annotations ({{annotations.length}} Highlights)

{%- macro calloutType(color) -%}
  {%- if color == "#ff6666" or color == "Red" -%}danger
  {%- elif color == "#5fb236" or color == "Green" -%}success
  {%- elif color == "#2ea8e5" or color == "Blue" -%}info
  {%- elif color == "#ffd400" or color == "Yellow" -%}question
  {%- elif color == "#a28ae5" or color == "Purple" -%}note
  {%- else -%}quote
  {%- endif -%}
{%- endmacro -%}

{% for annot in annotations %}
{% if annot.type == "image" %}
> [!info] 🖼️ Diagram / Figure ([Page {{annot.pageLabel}}]({{annot.desktopURI}}))
> ![[{{annot.imageRelativePath}}]]
{% if annot.comment %}> **Note:** {{annot.comment}}{% endif %}

{% elif annot.annotatedText %}
> [!{{calloutType(annot.colorCategory)}}]- 📌 {{annot.colorCategory}} Highlight ([Page {{annot.pageLabel}}]({{annot.desktopURI}}))
> {{annot.annotatedText}}
{% if annot.comment %}
> 
> 💡 **User Note / Active Recall:**
> {{annot.comment}}
{% endif %}

{% endif %}
{% endfor %}"""

def main():
    parser = argparse.ArgumentParser(description="Obsidian Plugin Syntax Helper")
    subparsers = parser.add_subparsers(dest="plugin", help="Plugin to generate syntax for")

    # Tasks
    p_tasks = subparsers.add_parser("tasks", help="Obsidian Tasks codeblock")
    p_tasks.add_argument("--due", default="today", help="Due filter (today, week, all, or YYYY-MM-DD)")
    p_tasks.add_argument("--priority", default=None, help="Priority (highest, high, medium, low, lowest)")
    p_tasks.add_argument("--folder", default=None, help="Path filter")
    p_tasks.add_argument("--tag", default=None, help="Tag filter")

    # Tracker
    p_tracker = subparsers.add_parser("tracker", help="Obsidian Tracker codeblock")
    p_tracker.add_argument("--type", default="frontmatter", help="searchType (frontmatter, tag, dvField, task.done)")
    p_tracker.add_argument("--target", default="focus_hours", help="searchTarget property name")
    p_tracker.add_argument("--folder", default="Daily_Notes", help="Target folder")
    p_tracker.add_argument("--chart", choices=["line", "bar", "month", "summary"], default="line", help="Visual chart type")
    p_tracker.add_argument("--days", type=int, default=30, help="Days range")

    # Charts
    p_charts = subparsers.add_parser("charts", help="Obsidian Charts codeblock")
    p_charts.add_argument("--type", choices=["bar", "line", "pie", "doughnut", "radar"], default="bar")
    p_charts.add_argument("--title", default="Study Metrics")
    p_charts.add_argument("--labels", default="Mon,Tue,Wed,Thu,Fri")

    # Meta Bind
    p_mb = subparsers.add_parser("meta-bind", help="Meta Bind inputs and buttons")
    p_mb.add_argument("--type", choices=["toggle", "slider", "select", "button"], default="toggle")
    p_mb.add_argument("--prop", default="status")
    p_mb.add_argument("--label", default="Submit")

    # Templater
    p_tp = subparsers.add_parser("templater", help="Templater templates")
    p_tp.add_argument("--type", choices=["daily", "recall"], default="daily")

    # SRS
    p_srs = subparsers.add_parser("srs", help="Spaced Repetition flashcards")
    p_srs.add_argument("--type", choices=["basic", "reversed", "cloze", "multiline"], default="basic")

    # Breadcrumbs
    p_bc = subparsers.add_parser("breadcrumbs", help="Breadcrumbs codeblock")
    p_bc.add_argument("--type", choices=["tree", "mermaid"], default="tree")
    p_bc.add_argument("--dir", choices=["down", "up", "same", "next", "prev"], default="down")

    # Buttons
    p_btn = subparsers.add_parser("buttons", help="Buttons codeblock")
    p_btn.add_argument("--name", default="Open Daily Note")
    p_btn.add_argument("--type", default="command")
    p_btn.add_argument("--action", default="Daily notes: Open today's daily note")
    p_btn.add_argument("--color", default="blue")

    # Multi-Column
    p_mc = subparsers.add_parser("multi-column", help="Multi-Column layout")
    p_mc.add_argument("--cols", type=int, default=2)

    # Kanban
    p_kb = subparsers.add_parser("kanban", help="Kanban board note")
    p_kb.add_argument("--title", default="Project Board")

    # Zotero Integration
    p_zotero = subparsers.add_parser("zotero", help="Zotero Integration Nunjucks templates")
    p_zotero.add_argument("--kind", choices=["template", "macro", "annotation"], default="template")

    args = parser.parse_args()

    if not args.plugin:
        parser.print_help()
        sys.exit(0)

    if args.plugin == "tasks":
        print(gen_tasks(args.due, args.priority, args.folder, args.tag))
    elif args.plugin == "tracker":
        print(gen_tracker(args.type, args.target, args.folder, args.chart, args.days))
    elif args.plugin == "charts":
        print(gen_charts(args.type, args.title, args.labels))
    elif args.plugin == "meta-bind":
        print(gen_meta_bind(args.type, args.prop, args.label))
    elif args.plugin == "templater":
        print(gen_templater(args.type))
    elif args.plugin == "srs":
        print(gen_srs(args.type))
    elif args.plugin == "breadcrumbs":
        print(gen_breadcrumbs(args.type, args.dir))
    elif args.plugin == "buttons":
        print(gen_buttons(args.name, args.type, args.action, args.color))
    elif args.plugin == "multi-column":
        print(gen_multicolumn(args.cols))
    elif args.plugin == "kanban":
        print(gen_kanban(args.title))
    elif args.plugin == "zotero":
        print(gen_zotero(args.kind))

if __name__ == "__main__":
    main()

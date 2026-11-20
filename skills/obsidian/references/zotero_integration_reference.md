# 📚 Zotero Integration Plugin Specification & Syntax Guide

> **Plugin Name:** Zotero Integration (formerly Zotero Desktop Connector)  
> **Author:** mgmeyers  
> **Plugin ID:** `zotero-desktop-connector`  
> **Downloads:** 1.5M+  
> **Obsidian Community Plugins Search:** `Zotero Integration`

---

## 🚀 1. Setup & Local Connection

This plugin connects Obsidian directly to the user's running **Zotero 10** desktop application via the local HTTP API (`127.0.0.1:23119`).

### Quick Configuration Steps:
1. Open Obsidian **Settings** ➔ **Community plugins** ➔ Search for `Zotero Integration` ➔ **Install** and **Enable**.
2. Go to **Zotero Integration** settings:
   * **Zotero Version:** `Zotero 7+` (compatible with Zotero 10).
   * **Port:** `23119` (matches local server).
   * **Citation Export Format:** `Better BibTeX Quick Copy` or `Default`.
3. Under **Import Formats**, click **Add Import Format** (e.g., name it `Literature Note` or `Gov Exam Book/Paper`).

---

## 📑 2. Nunjucks Templating Syntax

Zotero Integration uses **Nunjucks** (`{{ variable }}`, `{% if ... %}`, `{% for ... %}`) to dynamically format metadata, notes, and annotations.

### 2.1 Essential Top-Level Variables

| Variable | Description | Example Output |
| :--- | :--- | :--- |
| `{{title}}` | Full item title | `RRB ALP CBT-I Official Paper` |
| `{{citekey}}` | Citekey (from BBT or auto) | `singhEnglishGeneralCompetitions2026` |
| `{{itemType}}` | Type of Zotero item | `book`, `journalArticle`, `document` |
| `{{date}}` / `{{year}}` | Publication date / year | `2026` |
| `{{authors}}` | Formatted author string | `Neetu Singh` |
| `{{creators}}` | Array of creators | `[{firstName, lastName, creatorType}]` |
| `{{abstractNote}}` | Abstract or summary | Book description |
| `{{collections}}` | Collections containing item | `["TESTS", "RRB ALP"]` |
| `{{tags}}` | Array of tags on item | `[{tag: "CBT-1"}, {tag: "Official"}]` |
| `{{pdfZoteroLink}}` | URI to open main PDF | `zotero://open-pdf/0_KEY/1` |
| `{{selectLink}}` | Select item in Zotero GUI | `zotero://select/library/items/KEY` |

### 2.2 Annotation & Highlight Variables (`{{annotations}}`)

When extracting highlights from Zotero's built-in PDF reader, iterate through `annotations`:

```jinja2
{% for annot in annotations %}
  • Text: {{annot.annotatedText}}
  • Comment: {{annot.comment}}
  • Color: {{annot.color}} (or {{annot.colorCategory}})
  • Page: {{annot.pageLabel}}
  • Deep Link: [Page {{annot.pageLabel}}]({{annot.desktopURI}})
{% endfor %}
```

Annotation Attributes:
* `annot.annotatedText`: Exact text highlighted by the user in the PDF.
* `annot.comment`: Personal note or active recall question added to the highlight.
* `annot.colorCategory`: Named color (`Yellow`, `Red`, `Green`, `Blue`, `Purple`, `Magenta`).
* `annot.type`: `highlight`, `image`, `underline`, `note`.
* `annot.imageRelativePath`: Extracted rectangular area diagram/image saved in vault attachments folder.
* `annot.desktopURI`: Direct deep link (`zotero://open-pdf/library/items/<key>?page=<n>&annotation=<id>`) opening Zotero straight to that highlighted line.

---

## 🎨 3. Chromatic Callout Mapping (Gov-Exam & Cognitive Strategy)

Align Zotero highlight colors directly with Obsidian Callouts:

* 🔴 **Red (`#ff6666` / `Red`):** Exam Traps, Silly Mistakes, Negative Marking Warnings (`> [!danger]`).
* 🟢 **Green (`#5fb236` / `Green`):** Formulas, Shortcuts, Math Rules, Direct Hacks (`> [!success]`).
* 🟡 **Yellow (`#ffd400` / `Yellow`):** Core Facts, NCERT Concepts, Active Recall Questions (`> [!question]`).
* 🔵 **Blue (`#2ea8e5` / `Blue`):** Frameworks, Historical Dates, Chronology (`> [!info]`).
* 🟣 **Purple (`#a28ae5` / `Purple`):** Vocabulary, Mnemonics, Exceptions (`> [!note]`).

### Color-to-Callout Nunjucks Macro:

```jinja2
{%- macro calloutType(color) -%}
  {%- if color == "#ff6666" or color == "Red" -%}danger
  {%- elif color == "#5fb236" or color == "Green" -%}success
  {%- elif color == "#2ea8e5" or color == "Blue" -%}info
  {%- elif color == "#ffd400" or color == "Yellow" -%}question
  {%- elif color == "#a28ae5" or color == "Purple" -%}note
  {%- else -%}quote
  {%- endif -%}
{%- endmacro -%}
```

---

## 📝 4. Production Master Template (Gov-Exam Prep / Study Note)

Paste this into **Zotero Integration** ➔ **Import Formats** ➔ **Template**:

```jinja2
---
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
{% endfor %}
```

---

## 🧩 5. Companion Plugins to Install

To form a complete study environment:

Plugin | Community Name | Primary Role
:--- | :--- | :---
**Zotero Integration** | `Zotero Integration` | Local Zotero 10 PDF highlights & metadata import.
**Spaced Repetition** | `Spaced Repetition` | Native flashcard review (`#flashcards`, `Q::A`, cloze).
**Templater** | `Templater` | Dynamic `<% tp.* %>` execution for daily notes & exam sprints.
**Dataview** | `Dataview` | Querying imported papers, books, and syllabus mastery.

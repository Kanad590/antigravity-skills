# 🍞 Obsidian Breadcrumbs Plugin Reference & Syntax Guide

The **Breadcrumbs** plugin (`michaelpporter/breadcrumbs`) establishes hierarchical and sequential graph relationships between notes, enabling structured navigation trails, family tree structures, and dynamic roadmaps without cluttering the graph view.

---

## 1. 🧭 Core Navigation Relationship Fields

Breadcrumbs defines five fundamental directional relationships, which can be defined in YAML frontmatter or as Dataview inline fields (`key:: value`):

| Direction | Inline Field | Frontmatter YAML | Semantic Role |
| :--- | :--- | :--- | :--- |
| **Parent** | `up:: [[Hub Note]]` | `up: "[[Hub Note]]"` | Higher abstraction level, parent category, MOC |
| **Child** | `down:: [[Subtopic]]` | `down: ["[[Subtopic 1]]"]` | Granular detail, chapter, subtopic |
| **Sibling** | `same:: [[Related]]` | `same: ["[[Related]]"]` | Peer concepts at the same hierarchy level |
| **Next** | `next:: [[Chapter 2]]` | `next: "[[Chapter 2]]"` | Sequential progression, curriculum next step |
| **Prev** | `prev:: [[Chapter 0]]` | `prev: "[[Chapter 0]]"` | Preceding step or prerequisite |

---

## 2. 🌲 Breadcrumbs Codeblock (` ```breadcrumbs `)

Embed dynamic hierarchy visualizers directly in your note:

### A. Nested Tree View
```breadcrumbs
type: tree
dir: down
depth: [1, 3]
sort: basename asc
```

### B. Mermaid Flowchart View
Automatically renders directional relationships as a native Mermaid diagram:
```breadcrumbs
type: mermaid
dir: down
depth: [1, 2]
```

### C. Sequential Step-by-Step Navigation Bar
```breadcrumbs
type: tree
dir: next
depth: 1
```

---

## 3. 💡 Complete Note Architecture Example

```yaml
---
title: "Heart Failure Pathophysiology"
up: "[[Cardiovascular_System_Hub]]"
prev: "[[Cardiovascular_Hemodynamics]]"
next: "[[Arrhythmias_and_Conduction_Disorders]]"
same:
  - "[[Hypertension_and_Vascular_Diseases]]"
  - "[[Valvular_Heart_Diseases]]"
tags:
  - medicine/cardiology
---

# 🫀 Heart Failure Pathophysiology

## 🧭 Concept Neighborhood
```breadcrumbs
type: mermaid
dir: down
depth: 1
```

## 📖 Content
...
```

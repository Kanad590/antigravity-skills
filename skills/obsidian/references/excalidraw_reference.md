# 🎨 Obsidian Excalidraw Plugin Reference & Architecture Guide

The **Obsidian Excalidraw** plugin (`zsviczian/obsidian-excalidraw-plugin`) integrates infinite-canvas hand-drawn sketching with full bidirectional bi-linking into Obsidian's knowledge base.

---

## 1. 📁 File Architecture (.excalidraw.md)

Excalidraw drawings are stored as 100% human-readable Markdown files with embedded JSON blocks.

```yaml
---
excalidraw-plugin: parsed
tags:
  - excalidraw
  - diagram
---
```

Underneath the frontmatter, the file contains:
1. **Text Elements section**: Plain text representations of all text elements in the drawing (enabling native Obsidian search and backlink indexing).
2. **`%% # Drawing Data %%`**: Compressed JSON payload representing geometric nodes, arrows, colors, and coordinates.

---

## 2. 🔗 Embedding Drawings in Markdown Notes

Embed an Excalidraw drawing into any standard note using Obsidian wikilink syntax:

### Basic Embed
```markdown
![[Cognitive_Loop_Architecture.excalidraw]]
```

### Resized Embed (Width / Aspect Ratio)
```markdown
![[Cognitive_Loop_Architecture.excalidraw|500]]
![[Cognitive_Loop_Architecture.excalidraw|100%]]
```

### Frame & Element Transclusion (Targeted Crop)
Instead of embedding the entire infinite canvas, embed only a specific named frame or group:
```markdown
![[System_Architecture.excalidraw#^area=Auth_Flow_Frame]]
![[System_Architecture.excalidraw#^group=d4f8e21a]]
```

---

## 3. 🔄 Bidirectional Linking inside Drawings

- **Wikilinks on Canvas**: Double-click any element or text block on the Excalidraw canvas and type `[[Note Name]]`. Clicking that element in view mode opens the referenced note.
- **Transcluding Markdown into Drawings**: You can embed live markdown notes directly onto the Excalidraw canvas using `{{[[Note Name]]}}` or `{{[[Note Name#Heading]]}}`. The text on canvas updates whenever the underlying note changes.
- **Exporting Options**: Convert drawings automatically into `.svg` or `.png` attachments on save for compatibility with static site generators and mobile viewers.

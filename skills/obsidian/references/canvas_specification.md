# 🎨 Obsidian Canvas Specification & JSON Architecture

Obsidian Canvas files have the `.canvas` extension and are stored as clean JSON files. They allow spatial arrangement of notes, cards, web embeds, and groups connected by directional arrows.

---

## 1. 📐 Top-Level JSON Schema

An Obsidian Canvas file consists of two primary arrays:
```json
{
  "nodes": [],
  "edges": []
}
```

---

## 2. 🔲 Node Types & Attributes

Every node must have:
- `id`: Unique identifier (typically a 16-character hexadecimal string, e.g. `"6a8f10b2c3d4e5f6"`).
- `x`: Integer X coordinate on canvas.
- `y`: Integer Y coordinate on canvas.
- `width`: Integer width in pixels (e.g. `350`).
- `height`: Integer height in pixels (e.g. `240`).
- `type`: One of `"text"`, `"file"`, `"link"`, or `"group"`.

### A. Text Card Node (`type: "text"`)
Contains raw Markdown text directly on the canvas:
```json
{
  "id": "node_text_01",
  "type": "text",
  "text": "## 🧠 Cognitive Anchor\n- [[Oakley_Learning_Framework]]\n- Focused / Diffuse cycles",
  "x": 100,
  "y": 150,
  "width": 320,
  "height": 220,
  "color": "5"
}
```

### B. File Node (`type: "file"`)
Embeds an entire note or attachment from within the vault:
```json
{
  "id": "node_file_01",
  "type": "file",
  "file": "00_Dashboard/Master_Self_Help_Hub.md",
  "x": 500,
  "y": 150,
  "width": 450,
  "height": 500,
  "color": "4"
}
```

### C. Group Node (`type: "group"`)
A bounding container that visually encloses related nodes:
```json
{
  "id": "group_01",
  "type": "group",
  "label": "🌱 Mindset & Motivation Foundation",
  "x": 50,
  "y": 50,
  "width": 800,
  "height": 600,
  "color": "1"
}
```

---

## 3. 🎨 Chromatic Shorthand (Color Palette)

Obsidian Canvas supports preset color keys as strings `"1"` through `"6"`:
| Value | Standard Theme Color | Semantic Meaning |
| :---: | :--- | :--- |
| `"1"` | 🔴 Red | High Urgency, Motive, Danger alerts |
| `"2"` | 🟠 Orange | Action items, Active Recall questions |
| `"3"` | 🟡 Yellow | Attention points, Cautionary rules |
| `"4"` | 🟢 Green | Verified, Health, Nutrition, Completed |
| `"5"` | 🔵 Cyan / Blue | Information, Study frameworks, Routines |
| `"6"` | 🟣 Purple | Fashion, Luxury combinations, Aesthetics |

---

## 4. 🔀 Edges (Connections & Arrows)

Edges represent lines connecting two nodes:
```json
{
  "id": "edge_01",
  "fromNode": "node_text_01",
  "fromSide": "right",
  "toNode": "node_file_01",
  "toSide": "left",
  "color": "5",
  "label": "informs"
}
```

### Valid Connection Sides:
- `"top"`, `"right"`, `"bottom"`, `"left"`

---

## 5. 🛠️ Programmatic Generation Best Practices
- Node IDs should be generated using `uuid.uuid4().hex[:16]`.
- Spatial padding: Keep at least 60px horizontal and vertical distance between neighboring nodes to prevent overlap.
- Group bounding boxes must encapsulate the coordinates of all member nodes with padding (`min_x - pad`, `min_y - pad`, `max_x - min_x + 2*pad`, `max_y - min_y + 2*pad`).

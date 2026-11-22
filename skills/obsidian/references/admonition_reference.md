# 💬 Obsidian Admonition & Callouts Reference & Syntax Guide

The **Admonition** plugin (`ebullient/obsidian-admonition`) pioneered custom blockquotes in Obsidian and integrates seamlessly with Obsidian's modern native Callout system.

---

## 1. 🧱 Native Callouts vs Admonition Codeblocks

| Feature | Obsidian Native Callouts | Admonition Plugin (`ad-*`) |
| :--- | :--- | :--- |
| **Syntax** | `> [!type] Title` | ````ad-type \n title: Title \n ... ```` |
| **Dependency** | None (Core Markdown) | Community Plugin |
| **Mobile & Publish** | Built-in native rendering | Requires plugin |
| **Custom Types** | CSS snippets | GUI Type Builder & Custom Lucide/FontAwesome Icons |
| **Auto-Convert**| Native standard | Automatically transforms `ad-*` blocks to `> [!type]` |

---

## 2. ⚙️ Admonition Codeblock Syntax

```markdown
```ad-tip
title: 🎯 Active Recall Protocol
collapse: closed
color: 56, 189, 248

Review the question below, conceal the answer, and verbalize the underlying mechanism before expanding.
```
```

### Configurable Keys
- **`title`**: String displayed in the callout header bar.
- **`collapse`**:
  - `closed`: Collapsed by default (click to expand).
  - `open`: Expanded by default (click to collapse).
  - `none`: Static uncollapsible box.
- **`color`**: RGB string (e.g. `255, 99, 132`) or hex code.
- **`icon`**: Lucide or FontAwesome icon identifier (e.g. `lucide-brain`).

---

## 3. 🔄 Modern Recommendation: Native Callouts First

Always write native Obsidian callouts whenever possible for maximum portability:
- Collapsed: `> [!question]- ❓ Question Title`
- Expanded: `> [!tip]+ 🎯 Action Title`
- Static: `> [!danger] ⚠️ Warning`

Use the Admonition plugin primarily to register custom icon sets and custom themes.

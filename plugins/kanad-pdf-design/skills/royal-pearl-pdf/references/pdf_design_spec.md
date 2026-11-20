# 🎨 Kanad PDF Design Specification & Conversion Pitfalls

> **Origin:** Synthesized from `Canada Visa PDF Design Tips` visual/psychological blueprint and production `.md ➔ .pdf` debugging.

---

## 1. Colour Palettes

### Option A (Default): "Royal Pearl & Deep Teal + Warm Gold"
Best for print, study guides, reports, visa/legal briefs, and comfortable long reading:
- **Page Canvas (`@page` + `body`):** Warm Ivory / Pearl `#FAF8F4` (replaces harsh `#FFFFFF`)
- **Hero Banner & Table Headers:** Deep Midnight Teal `#0F3D3E` (gradient to `#13293D`)
- **Accents, Borders & Badges:** Champagne Gold `#C59B27` (`8px` rounded card corners, `1px` soft border `#E2D9C5` — never thick black borders)
- **Body Text:** Charcoal Slate `#222831` (`line-height: 1.54`)
- **Positive / DO Cards:** Soft Sage Emerald (`#2E6F5E` text, `#E9F3F0` background, `#B7DEC9` border)
- **Caution / Exam Trap / DON'T Cards:** Muted Terracotta (`#B84A39` text, `#FBECE9` background, `#E9B9B0` border) — **never harsh `#FF0000` red**

### Option B (Screen-Only Dark): "Modern Executive Dark" (`--theme dark`)
- **Background:** Deep Obsidian Navy `#111827`
- **Card Surface:** Soft Slate `#1E293B`
- **Primary Text:** Soft Pearl `#F1F5F9`
- **Accent:** Warm Gold `#D4AF37` + Ice Teal `#38BDF8`

---

## 2. Layout Anatomy
1. **Page 1 Hook:** High-impact Hero Banner (`Playfair Display` + `Plus Jakarta Sans` + `Noto Sans Bengali`) + **3-Card "At a Glance" Executive Summary KPI Row** right on top.
2. **Scannable Modular Blocks:** Maintain 30–40% breathing room, structured tables with repeating `thead`, color-coded callouts, contextual emojis, and local verified images.
3. **Last Page Action Cheat Sheet:** A compact **"Do's & Don'ts + Next Step"** summary card for 60-second revision.

---

## 3. The 9 `.md ➔ .pdf` Pitfalls (Handled by `scripts/md_to_pdf.py`)
1. **Broken Bengali Conjuncts & `□□□` Emojis:** Solved via Headless Google Chrome (`Plus Jakarta Sans`, `Noto Sans Bengali`, `Lohit Bengali`, `Noto Color Emoji`).
2. **Obsidian Image Embeds Mangled by Wikilink Regex:** Convert `![[img|width]]` and `![alt](path)` **before** stripping `[[Target|Alias]]`; launch Chrome with `--allow-file-access-from-files`.
3. **Raw `dataviewjs` Code Leak:** Parse `QUIZ = [...]` JS arrays into styled static Q&A cards (or strip raw code blocks cleanly).
4. **Raw `#flashcards` `?` Separators:** Transform `#flashcards/...` Q/A/Logic blocks into styled Flashcard boxes.
5. **Unparsed Markdown Inside Callouts:** Pass callout body text through `markdown.markdown(...)` before wrapping in `<div class="callout-body">`.
6. **Adjacent Callouts Merging & Flattened Lists:** Break callout loops when `re.match(r'^>\s*\[!\w+\]', cur)` and ensure `\n\n` precedes `* ` list lines.
7. **Unreadable `flowchart TD` Mermaid Trees:** Auto-convert `flowchart TD` to `flowchart LR` during PDF export when diagrams have wide fan-out.
8. **Whole-Table `break-inside: avoid` & Cross-Cell `*...**`:** Apply `break-inside: avoid` only to `tr` + `thead { display: table-header-group; }`, and forbid `|` inside inline emphasis regexes (`[^*\n|]+?`).
9. **Silent Blank Trailing Pages / Broken Assets:** Always run `pdftoppm -r 150 -png` (`--qa-dir`) and inspect **every page** via `read_file` before delivery.

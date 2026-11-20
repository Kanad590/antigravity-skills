# Universal PDF Design & Conversion Rule (Global Default)

Whenever generating, converting, or exporting ANY PDF (study notes, reports, visa/astrology/project docs, or Markdown files) in ANY project:

1. **Default Design System (`Royal Pearl & Deep Teal + Warm Gold`):**
   - Use **Warm Ivory (`#FAF8F4`)** page canvas (avoid harsh `#FFFFFF`), **Deep Midnight Teal (`#0F3D3E`)** hero banner & table headers, **Champagne Gold (`#C59B27`)** accents (`8px` rounded corners, `1px` soft borders — no thick black borders), **Charcoal Slate (`#222831`)** body text, **Soft Sage (`#2E6F5E` / `#E9F3F0`)** positive cards, and **Muted Terracotta (`#B84A39` / `#FBECE9`)** for warnings/cautions (avoid harsh `#FF0000` red).
   - *(Switch to `Modern Executive Dark` `#111827` / `#1E293B` / `#D4AF37` / `#38BDF8` only when explicitly requested for dark screen-only presentations.)*
2. **Executive Scannable Layout:**
   - **Page 1 Hook:** High-impact Hero Banner + **3-Card "At a Glance" Executive Summary** right on top.
   - **Readability:** 30–40% breathing white space, scannable modular cards/tables, contextual emojis, and authentic visual anchors where helpful.
   - **Last Page:** Include a **One-Page Action Cheat Sheet (`Do's & Don'ts` / `Next Steps`)** for any guide, report, or advisory PDF.
3. **Engine & Pitfall Guards (Zero Broken Bengali / Raw Markdown):**
   - Use the `royal-pearl-pdf` skill (`~/.gemini/config/plugins/kanad-pdf-design/skills/royal-pearl-pdf/scripts/md_to_pdf.py`) via **Headless Google Chrome** (`Noto Sans Bengali`, `Lohit Bengali`, `Plus Jakarta Sans`, `Playfair Display`, `Noto Color Emoji`) — never `weasyprint`/`pandoc`/`reportlab` for Bengali or emoji docs.
   - Resolve `![[image|width]]` and `![alt](path)` embeds before `[[wikilink]]` stripping; pre-render callout Markdown bodies; prevent consecutive callout merging; convert `dataviewjs`/`#flashcards` into static cards; convert wide `flowchart TD` Mermaid diagrams to `flowchart LR`; apply `break-inside: avoid` to `tr` (not whole `table`).
4. **Mandatory Visual Verification:**
   - Always render every PDF page with `pdftoppm -r 150 -png` (or pass `--qa-dir` to `md_to_pdf.py`) and inspect the PNGs via `read_file` (confirming zero blank pages, zero clipped diagrams, zero raw syntax) before delivering to the user or Telegram.

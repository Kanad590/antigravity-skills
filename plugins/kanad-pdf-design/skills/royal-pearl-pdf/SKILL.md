---
name: royal-pearl-pdf
description: >-
  Generate polished, print-ready A4 PDFs from Markdown/Obsidian/HTML in ANY project using
  Kanad's default Royal Pearl & Deep Teal + Champagne Gold design system (or Modern Executive Dark),
  Headless Chrome Bengali+Emoji typography, Mermaid/Callout/Embed support, and mandatory pdftoppm visual QA.
---

# ✨ Royal Pearl PDF Engine (Global Default)

Use this skill whenever generating, converting, or exporting a `.md` note, report, study guide, or document into a PDF in **any** project.

---

## 🚀 Quick Command

```bash
python3 ~/.gemini/config/plugins/kanad-pdf-design/skills/royal-pearl-pdf/scripts/md_to_pdf.py \
  --input "/path/to/input.md" \
  --output "/path/to/output.pdf" \
  --qa-dir "/tmp/pdf_qa"
```

### Key CLI Options

| Flag | Default | Purpose |
| :--- | :--- | :--- |
| `--input`, `-i` | *(required)* | Source `.md` file path |
| `--output`, `-o` | *(required)* | Destination `.pdf` file path |
| `--theme` | `royal_pearl` | `royal_pearl` (default Warm Ivory/Midnight Teal/Gold) or `dark` (Modern Executive Dark) |
| `--title` | Auto from `# H1` / frontmatter | Override hero banner title |
| `--subtitle` | Auto from frontmatter/sections | Subtitle line under hero title |
| `--badge` | Auto from frontmatter | Repeatable pill badges in hero banner (e.g., `--badge "VISA REPORT"`) |
| `--footer` | Auto from title | Custom bottom-left footer text |
| `--vault-root` | Auto-detected | Base directory for resolving `![[...]]` & relative image embeds |
| `--kpi-json` | Auto-generated 3 cards | Path or inline JSON list of 3 `{"label","val","desc"}` KPI cards |
| `--cheat-sheet-json` | Auto / omitted if `--no-cheat-sheet` | Path or inline JSON `{"title","dos":[],"donts":[],"next_step":""}` |
| `--no-cheat-sheet` | `false` | Skip the concluding One-Page Action Cheat Sheet block |
| `--qa-dir` | *(optional)* | Render 150-dpi PNGs (`page-1.png`, ...) via `pdftoppm` for mandatory visual QA |

---

## 🛡️ Enforced `.md ➔ .pdf` Guardrails

For full color tokens, layout anatomy, and the 9 conversion pitfalls avoided by `md_to_pdf.py`, see [pdf_design_spec.md](./references/pdf_design_spec.md):
1. **Never** use `weasyprint`, `pandoc`, or `reportlab` for Bengali or emoji PDFs (Headless Chrome preserves conjuncts & color emojis).
2. **Always** resolve `![[image|width]]` before `[[wikilink]]` stripping and pass `--allow-file-access-from-files` to Chrome.
3. **Always** inspect every PNG generated in `--qa-dir` with `read_file` before sending to the user or Telegram (`tg-bot-send`).

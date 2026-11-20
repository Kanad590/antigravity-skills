---
name: zotero-study-manager
description: >-
  Use this skill whenever the user asks to inspect, search, or query their local Zotero library,
  find study question papers (RRB JE, RRB ALP, NTPC, Banking, SSC, Books), locate attachment PDF paths,
  read PDF pages/outlines, add new question papers/books, or export bibliographic metadata into Obsidian notes.
---

# Zotero Study & Library Manager Skill

This skill enables Antigravity to interface directly with the user's local **Zotero 10** library (`~/Zotero/`) via:
1. **Zotero Local HTTP API (`127.0.0.1:23119`)** with persistent local write authorization (`localAPIKeys.json`).
2. **`zotero-cli` Standalone CLI (`~/.local/bin/zotero-cli`)** for reading PDF pages, extracting outlines, searching collections, and adding new PDFs/books.
3. **`zotero-mcp` Model Context Protocol Server (`~/.gemini/config/mcp_config.json`)** exposing 38 native tools for item metadata, attachments, annotations, notes, and full-text searches.
4. **Fast Local SQLite Snapshots (`zotero_cli.py`)** for zero-latency offline schema lookups even when Zotero is locked.

It provides instant access to 1,300+ items, exam question papers (RRB JE, RRB ALP, NTPC, RPF, Banking, CBT 1 & 2), and books.

---

## 🚀 Quick Reference Commands (`zotero-cli`)

Command | Description
:--- | :---
`~/.local/bin/zotero-cli get collections` | List all collections with keys and counts
`~/.local/bin/zotero-cli search "<query>"` | Search library items by title/metadata
`~/.local/bin/zotero-cli get recent --limit 10` | Show most recently added items
`~/.local/bin/zotero-cli path <item_key>` | Show absolute local path of attached PDF on disk
`~/.local/bin/zotero-cli read <item_key> --start-page 1 --end-page 5` | Extract text from specific PDF pages
`~/.local/bin/zotero-cli outline <item_key>` | Extract Table of Contents / Outline from PDF
`~/.local/bin/zotero-cli add file --filepath <path> --title <title> --collection <coll_key>` | Add local PDF into Zotero collection
`~/.local/bin/zotero-cli annotations list --item-key <item_key>` | View highlights and annotations on PDF
`~/.local/bin/zotero-mcp authorize-local --status` | Check local API write authorization status

---

## 📁 Key Collections

* **RRB ALP (`3JEGWBY4`):** Assistant Loco Pilot Previous Question Papers (CBT-1 & CBT-2).
* **RRB JE (`JY75LUYH`):** Junior Engineer Previous Papers & Engineering Sets.
* **RRB NTPC (`QF53Y4L7`):** Non-Technical Popular Categories CBT-1 (`FY3TU6D9`) & CBT-2 (`5RGTTXDJ`).
* **Books (`AFLFPX7I`):** Reference books (Neetu Singh English, Gagan Pratap Math, Aditya Ranjan Math, etc.).
* **Banking / Insurance:** IBPS RRB (`53FY75Z8`), SBI (`DBHM4JIC`), RBI Grade B (`EPP5MWXH`), NICL (`XAX2BY5L`).

---

## 💡 Capabilities & Integration

1. **Adding & Ingesting Question Papers:**
   To add an exam paper or answer key PDF to Zotero:
   ```bash
   ~/.local/bin/zotero-cli add file \
     --filepath "/path/to/paper.pdf" \
     --title "RRB ALP CBT-I Official Paper (Held On_ DD Mon, YYYY Shift X)" \
     --collection "3JEGWBY4" \
     --tags "RRB ALP,CEN 01/2026,CBT-1,Official Paper"
   ```
2. **Reading PDF Pages Directly:**
   ```bash
   ~/.local/bin/zotero-cli read <item_key> --start-page 1 --end-page 3
   ```
3. **Obsidian Integration:**
   Metadata, extracted PDF highlights, active recall callouts, and cropped diagrams are imported via the **Zotero Integration** Obsidian community plugin (ID: `zotero-desktop-connector`) connecting to port `23119`. See full Nunjucks template and callout color mapping in [zotero_integration_reference.md](file:///home/saman/.agents/skills/obsidian/references/zotero_integration_reference.md).

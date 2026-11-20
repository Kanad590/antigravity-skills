---
name: calibre-manager
description: >-
  Use this skill whenever the user asks to manage, search, list, or curate their Calibre e-book library
  (/home/saman/Calibre Library), inspect book metadata, add new EPUB/PDF files, or fix library cataloging.
---

# Calibre Library Manager Skill

This skill enables Antigravity to interact directly with the user's **Calibre Library** (`/home/saman/Calibre Library`) using `calibredb`.

---

## 🚀 Quick Reference Commands

Helper CLI Script: `~/.gemini/config/plugins/calibre-manager/skills/calibre-manager/scripts/calibre_helper.py`

Task | Command
:--- | :---
**List Recent Books** | `~/.gemini/config/plugins/calibre-manager/skills/calibre-manager/scripts/calibre_helper.py list`
**Search Books by Query** | `~/.gemini/config/plugins/calibre-manager/skills/calibre-manager/scripts/calibre_helper.py list "<search_term>"`
**Show Book Metadata** | `~/.gemini/config/plugins/calibre-manager/skills/calibre-manager/scripts/calibre_helper.py show <book_id>`
**Add Book File to Calibre** | `~/.gemini/config/plugins/calibre-manager/skills/calibre-manager/scripts/calibre_helper.py add "/path/to/book.pdf" --title "Title" --authors "Author"`
**Machine JSON output** | `~/.gemini/config/plugins/calibre-manager/skills/calibre-manager/scripts/calibre_helper.py list --json`

---

## 💡 Capabilities

1. **Catalog Inspection:** Quickly search or filter books by title, author, or tags.
2. **Metadata Enrichment:** Retrieve format details, ISBN, publishers, and tags.
3. **Curation Workflows:** Pairs with the user's curation scripts (`execute_books_curation.py`, `apply_curation_fixes.py`) for clean library maintenance.

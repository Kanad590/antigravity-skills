---
name: exam-quiz-engine
description: >-
  Use this skill whenever the user asks to generate exam quizzes, test their knowledge,
  extract questions from study PDFs (RRB JE, RRB ALP, Manufacturing & Material Science),
  create Obsidian flashcard decks, or send revision quizzes to Telegram.
---

# Exam Quiz & Active Recall Engine Skill

This skill turns study PDFs, question papers, and syllabus topics into active recall quizzes, interactive MCQs, and flashcard decks.

---

## 🚀 Quick Reference Commands

Helper CLI Script: `~/.gemini/config/plugins/exam-quiz-engine/skills/exam-quiz-engine/scripts/quiz_generator.py`

Task | Command
:--- | :---
**Extract PDF Study Segment** | `~/.gemini/config/plugins/exam-quiz-engine/skills/exam-quiz-engine/scripts/quiz_generator.py extract "/path/to/note.pdf" --start 1 --end 5`
**Send Quiz to Telegram** | `~/.gemini/config/plugins/exam-quiz-engine/skills/exam-quiz-engine/scripts/quiz_generator.py send-quiz --topic "Material Science" --question "Q1: What is the carbon % in eutectoid steel? ..."`
**Save Flashcard Deck to Obsidian**| `~/.gemini/config/plugins/exam-quiz-engine/skills/exam-quiz-engine/scripts/quiz_generator.py save-deck --deck "Manufacturing" --content "Question :: Answer"`

---

## 💡 Recommended Workflow

1. **Read & Extract:** Extract a specific section or chapter from the user's study note (e.g. `~/Desktop/🏭 Manufacturing & Material Science Master Study Note.pdf` or Zotero question papers).
2. **Formulate High-Yield Questions:** Create 4-option MCQs with explanations, focusing on exam patterns (RRB JE CBT-2, WBPSC IDO, RRB ALP).
3. **Delivery:**
   - Present interactively in chat.
   - Send question of the day to Telegram via `send-quiz` (or send a spoken Piper voice revision quiz via `tg-bot-send --voice-note`).
   - Save to `/home/saman/Documents/OBSIDIAN/Flashcards/` for Spaced Repetition (SRS), with optional `.base` tracker views (`obsidian-bases`) or `.canvas` mind-maps (`json-canvas`).
   - Turn high-yield PYQs/concepts into 30–40s offline quiz Shorts (`faceless-shorts` `make-short` with `PauseCard` + `gen_voice.py --provider piper` + `gen_sfx_offline.py`) and deliver as playable MP4 via `tg-bot-send --file`.
   - If requested, update Kanboard topic mastery via `kanbanboard` skill!

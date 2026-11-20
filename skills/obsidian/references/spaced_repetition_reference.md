# 🧠 Obsidian Spaced Repetition (SRS) Plugin Reference & Syntax Guide

The **Spaced Repetition** plugin (`st3v3nmw/obsidian-spaced-repetition`) transforms Obsidian Markdown notes into an active-recall study engine, generating flashcards and managing whole-note review intervals using SM-2 or FSRS algorithms.

---

## 1. 🗂️ Deck Organization via Tags

Notes containing flashcards are assigned to study decks using Obsidian hashtags:

- **Root Deck**: `#flashcards`
- **Sub-Decks (Hierarchical)**:
  - `#flashcards/medical/cardiology`
  - `#flashcards/aptitude/quantitative`
  - `#flashcards/general-science/physics`

When you review a sub-deck, parent decks aggregate cards automatically.

---

## 2. 🎴 Flashcard Syntaxes & Card Types

### A. Single-Line Basic (`::`)
The question is on the left, the answer is on the right:
```markdown
What is the primary action of the sub-occipital muscles? :: Stabilize the skull base and coordinate fine head movements.
In RRB NTPC, what is the weightage of General Awareness in CBT-1? :: 40 questions (out of 100).
```

### B. Single-Line Bidirectional (`:::`)
Tests the connection in both directions (creates two distinct sibling cards):
```markdown
Metformin ::: First-line biguanide oral hypoglycemic agent
Ascorbic Acid ::: Vitamin C
```

### C. Multi-Line Basic (`?` on isolated line)
Ideal for multi-paragraph explanations, diagrams, or lists:
```markdown
What are the symptoms and classic diagnostic triphasic colors of Raynaud's phenomenon?
?
1. **White (Pallor)**: Vasospasm of digital arterioles.
2. **Blue (Cyanosis)**: Deoxygenation of static blood pool.
3. **Red (Rubor)**: Reactive hyperaemia upon rewarming.
```

### D. Multi-Line Bidirectional (`??` on isolated line)
Generates two sibling cards for complex bidirectional memorization:
```markdown
Boyle's Law
??
For a fixed mass of gas at constant temperature, pressure is inversely proportional to volume: $P \propto \frac{1}{V}$ or $P_1 V_1 = P_2 V_2$.
```

---

## 3. 🧩 Cloze Deletions (Fill-in-the-Blank)

Cloze cards hide critical terms during testing:

### Standard Syntax (`==highlight==` or `{{braces}}`)
```markdown
The powerhouse of the cellular energy cycle is the ==mitochondrion==, generating ATP through ==oxidative phosphorylation==.
```
*(Obsidian SRS creates two independent review cards: one testing `mitochondrion`, the other testing `oxidative phosphorylation`.)*

### Cloze with Custom Hint (`::hint`)
```markdown
The normal resting adult heart rate is ==60 to 100::bpm range== beats per minute.
```

---

## 4. 📚 Whole-Note Spaced Repetition (Review Schedules)

Entire notes can be queued for periodic spaced review without turning them into atomic flashcards. The plugin records schedule metrics in the note's YAML frontmatter:

```yaml
---
title: "Cardiovascular Pharmacology Master Summary"
tags:
  - review
  - pharmacology
sr-due: 2026-11-04
sr-interval: 6
sr-ease: 250
---
```

- **`sr-due`**: Next scheduled review date (`YYYY-MM-DD`).
- **`sr-interval`**: Number of days until next review.
- **`sr-ease`**: Difficulty factor (base 250 = 250%). Higher ease increases intervals faster.

---

## 5. 💡 Integration with Active Recall Collapsible Callouts

Combine Spaced Repetition with Obsidian's native collapsible callouts to maintain pristine note readability while retaining flashcard parsing:

```markdown
#flashcards/pathology

> [!question]- ❓ Pathophysiology of Atherosclerosis
> What is the initial trigger for plaque formation? :: Endothelial injury followed by LDL oxidation and macrophage foam cell infiltration.
```

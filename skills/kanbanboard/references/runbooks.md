# Kanboard Operator Runbooks

## Runbook 1: View Overview & Active Board Summary
To view active project counts, column task distributions, and high-level health:
```bash
~/.agents/skills/kanbanboard/scripts/kanban_cli.py summary
```

---

## Runbook 2: Managing Competitive Examination Tasks (Project 4)
### List all active exams grouped by lifecycle stage:
```bash
~/.agents/skills/kanbanboard/scripts/manage_exam_tasks.py list
```

### Move an exam to a new stage (with optional AI comment):
```bash
# Example: Move RRB JE 2026 to "CBT 1 Done"
~/.agents/skills/kanbanboard/scripts/manage_exam_tasks.py set-stage 92 "CBT 1 Done" --comment "CBT 1 completed on Oct 18, 2026."

# Example: Move an exam to "Applied"
~/.agents/skills/kanbanboard/scripts/manage_exam_tasks.py set-stage 85 "Applied" --comment "Application form submitted and fee paid."
```

### View complete exam card with all subtasks and description:
```bash
~/.agents/skills/kanbanboard/scripts/kanban_cli.py task <task_id>
```

---

## Runbook 3: Tracking & Promoting Syllabus Topics (Project 5)
### Check subject-wise syllabus mastery breakdown:
```bash
~/.agents/skills/kanbanboard/scripts/manage_syllabus_tasks.py progress
```

### Search topics by keyword across subjects:
```bash
~/.agents/skills/kanbanboard/scripts/manage_syllabus_tasks.py search "Trigonometry"
~/.agents/skills/kanbanboard/scripts/manage_syllabus_tasks.py search "Buddhism"
```

### Promote a topic to the next mastery level:
```bash
# Moves from e.g. "Concept Clear" -> "Strong Level 1" -> "Strong Level 2"
~/.agents/skills/kanbanboard/scripts/manage_syllabus_tasks.py promote <task_id>
```

---

## Runbook 4: Creating Tasks, Comments, and Subtasks
### Create a new task in Project 4 or Project 5:
```bash
~/.agents/skills/kanbanboard/scripts/kanban_cli.py create 4 "New Notification Title" --tags "RRB,2027,Engineering" --priority 2 --due "2027-02-15"
```

### Post a comment as 🤖 AI (User #2):
```bash
~/.agents/skills/kanbanboard/scripts/kanban_cli.py comment <task_id> "🤖 Study reminder: Review mock test solutions tonight."
```

### Add and toggle subtasks:
```bash
~/.agents/skills/kanbanboard/scripts/kanban_cli.py subtask-add <task_id> "Solve 50 PYQs"
~/.agents/skills/kanbanboard/scripts/kanban_cli.py subtask-toggle <subtask_id>
```

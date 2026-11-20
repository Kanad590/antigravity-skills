---
name: kanbanboard
description: >-
  Use this skill whenever the user asks to view, manage, create, update, or track tasks,
  exams, or syllabus topics on their self-hosted Kanboard instance (http://192.168.1.100:1337/
  or Tailscale http://100.x.y.z:1337/). Supports Project #4 (Govt Exam Tracker) and
  Project #5 (All Subjects Syllabus Tracker), moving stages, subtasks, tags, and AI comments as User #2 (🤖 AI).
  Also triggered by the /kanbanboard command.
---

# Kanboard Management & Automation Skill

This skill empowers Antigravity to interact directly with the user's self-hosted **[Kanboard](https://kanboard.org/)** instance (version 1.2.54), operating as **User #2 (`🤖 AI`)** with full administrative privileges.

---

## 🚀 Quick Reference Commands

All CLI helper scripts automatically fail over between **LAN (`http://192.168.1.100:1337/jsonrpc.php`)** and **Tailscale (`http://100.x.y.z:1337/jsonrpc.php`)**.

Task | Command
:--- | :---
**Full Board Status Summary** | `~/.agents/skills/kanbanboard/scripts/kanban_cli.py summary`
**List All Projects** | `~/.agents/skills/kanbanboard/scripts/kanban_cli.py projects`
**List Active Exams (by Stage)** | `~/.agents/skills/kanbanboard/scripts/manage_exam_tasks.py list`
**Move Exam Stage** | `~/.agents/skills/kanbanboard/scripts/manage_exam_tasks.py set-stage <task_id> "<stage>"`
**Syllabus Mastery Report** | `~/.agents/skills/kanbanboard/scripts/manage_syllabus_tasks.py progress`
**Search Syllabus Topics** | `~/.agents/skills/kanbanboard/scripts/manage_syllabus_tasks.py search "<keyword>"`
**Promote Topic Mastery** | `~/.agents/skills/kanbanboard/scripts/manage_syllabus_tasks.py promote <task_id>`
**View Task Details** | `~/.agents/skills/kanbanboard/scripts/kanban_cli.py task <task_id>`
**Create New Task** | `~/.agents/skills/kanbanboard/scripts/kanban_cli.py create <project_id> "<title>" [options]`
**Add Comment as 🤖 AI** | `~/.agents/skills/kanbanboard/scripts/kanban_cli.py comment <task_id> "<text>"`
**Toggle Subtask Status** | `~/.agents/skills/kanbanboard/scripts/kanban_cli.py subtask-toggle <subtask_id>`

---

## 🛠️ Workflows

### 1. Daily Overview & Progress Briefing
When the user asks *"What's on my kanban board?"*, *"Check my exam status"*, or runs `/kanbanboard`:
1. Run [`kanban_cli.py summary`](./scripts/kanban_cli.py) to view high-level counts.
2. If the user specifically asks about exam updates, run [`manage_exam_tasks.py list`](./scripts/manage_exam_tasks.py).
3. If the user asks about study/syllabus coverage, run [`manage_syllabus_tasks.py progress`](./scripts/manage_syllabus_tasks.py).
4. Present a clear, concise bulleted summary organized by project.

### 2. Managing Exam Tracking (Project #4: `🎯 Govt Exam Tracker (Auto)`)
* **Project Structure:** 18 lifecycle columns spanning from `📥 To Apply` to `🎉 Selected`.
* **Moving Exam Stages:** When an application is submitted, admit card released, or CBT completed:
  ```bash
  ~/.agents/skills/kanbanboard/scripts/manage_exam_tasks.py set-stage <task_id> "CBT 1 Done" --comment "CBT 1 held on [Date]."
  ```
* **Real-time Priority Telegram Alerts:** `kanboard-stage-watcher.service`, `kanboard_automator_v3.py` (daily 9 PM grounded search), and `proactive-scheduler.service` (60s SQLite sentinel + deadline radar) share `kanboard_helper.py` to push priority-weighted `@SamanAssist96_bot` alerts for Results, Admit Cards, City Intimation Slips, Answer Keys, Exam/Result Dates, Stage Changes, and T-3d/T-1d/Today deadlines across Project #4 while filtering out `over-aged`, `❌ Not Selected`, and negative "not yet released" noise.
* **Exam Reference:** See [Project 4 Specification](./references/project_4_exam_tracker.md) for complete column mappings and tag definitions.

### 3. Tracking Syllabus & Chapter Mastery (Project #5: `All Subjects Syllabus Tracker 📋`)
* **Project Structure:** 191 syllabus topics across 12 subjects (History, Geography, Polity, Economy, Science, Math, Reasoning, English, etc.).
* **Mastery Stages:**
  `Level 0 (Backlog)` $\to$ `Level 1 (Concept Clear)` $\to$ `Level 2 (Strong L1)` $\to$ `Level 3 (Strong L2)` $\to$ `Level 4 (Exam Ready)` $\to$ `Level 5 (Mastered)`
* **Promoting a Chapter:** When the user finishes studying or revising a chapter:
  ```bash
  ~/.agents/skills/kanbanboard/scripts/manage_syllabus_tasks.py promote <task_id>
  ```
* **Syllabus Reference:** See [Project 5 Specification](./references/project_5_syllabus_tracker.md) for all categories and topic lists.

### 4. Creating Tasks & Checklists
* **Create Task:**
  ```bash
  ~/.agents/skills/kanbanboard/scripts/kanban_cli.py create <project_id> "Task Title" --tags "tag1,tag2" --priority 2 --due "YYYY-MM-DD"
  ```
* **Add Subtasks Checklist:**
  ```bash
  ~/.agents/skills/kanbanboard/scripts/kanban_cli.py subtask-add <task_id> "Read NCERT Chapter 4"
  ```
* **Operator Procedures:** See [Maintenance Runbooks](./references/runbooks.md) for comprehensive step-by-step guides.

---

## 📚 Detailed Reference Documentation
* **[Kanboard Architecture & JSON-RPC Specs](./references/kanboard_architecture.md):** Protocol details, endpoints, authentication tokens, and user credentials.
* **[Project 4: Exam Tracker Specification](./references/project_4_exam_tracker.md):** 18 stages, 35 tags, and active examination catalog.
* **[Project 5: Syllabus Tracker Specification](./references/project_5_syllabus_tracker.md):** 6 mastery levels, 12 categories, and 191 chapters.
* **[Operator Runbooks](./references/runbooks.md):** Practical runbooks for task management, moving cards, and automated AI comments.

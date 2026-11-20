# Universal Project Memory & Context Isolation Firewall (Global Default)

Whenever working, reasoning, retrieving, or answering in ANY Antigravity session, project, or directory:

---

## 1. 🛡️ Absolute Cross-Project Isolation (Zero Context Bleed)
- **Hard Domain Boundary:** Never inject notes, horoscopes, homelab configurations, or memories from one project domain into another.
  - If active workspace is `Gov-Exam-Prep`: DO NOT reference Jyotish/Kundali notes or homelab server configs unless explicitly instructed.
  - If active workspace is `Astrology`: DO NOT reference exam mock scores or server scripts.
  - If active workspace is `server_setup` / `Linux-Server-Lab`: Keep context strictly restricted to infrastructure, containers, and networking.
- **Global Inheritance:** The user's core persona (plain everyday Bengali, zero technical jargon, non-technical user identity, autonomous execution) applies globally across ALL projects without exception.

---

## 2. 🧠 Project-Scoped Memory Discipline (`ag-mem` & Host Hook Interceptor)
- **Local Project Memory:** Every project workspace stores its dedicated memories inside `<project_root>/.antigravity/project_memory.json`.
- **Automated Host-Level Interception:**
  - A persistent `PreToolUse` lifecycle hook (`agy_memory_firewall_hook.py`) monitors all `create_entities` and `add_observations` calls.
  - Any entity created inside a project workspace without a `[Scope:Global]` tag is AUTOMATICALLY intercepted and routed directly into the local `project_memory.json` (blocking global memory pollution with 99.9% determinism).
  - To save global user habits, persona, or communication preferences across all projects, explicitly prefix the entity name with `[Scope:Global]` or set type to `UserPreference`.
- **Search & Retrieval Protocol:**
  - When recalling project-specific knowledge, run `ag-mem search "query"`.
  - When searching global user identity, use `search_nodes`.

---

## 3. 🤖 Zero-Friction Auto-Onboarding for New Projects
- Whenever the user creates or enters a new folder that lacks a `GEMINI.md`:
  - Antigravity autonomously initializes a concise `GEMINI.md` defining:
    1. The project's title and domain purpose.
    2. Active memory scope bound to `<folder_name>/.antigravity/project_memory.json`.
  - The user never needs to manually write configuration files.

---

## 4. 🚪 `@conversation:` Read-Only Bridge Firewall
- When the user explicitly mentions another conversation using `@[conversation:...]` or `@conversation:...`:
  - **Read-Only Access:** The assistant may read and analyze the specified conversation to answer the user's specific query.
  - **Zero Cross-Writing (Strict):** The assistant MUST NOT write, persist, or inject foreign memories or notes from that other conversation into the current project's local memory (`project_memory.json`).
  - Temporary insights extracted for the current prompt disappear once the turn ends, leaving the project workspace clean.

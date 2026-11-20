---
name: telegram
description: >-
  Use this skill whenever the user asks to send messages, notes, summaries, files, or documents
  via Telegram, check incoming Telegram messages, or manage their Telegram assistant bot (@SamanAssist96_bot).
  Also triggered by the /telegram command.
---

# Telegram AI Assistant Skill

This skill enables Antigravity to interact with Telegram via the user's dedicated Telegram Bot (**`@SamanAssist96_bot`**). It can send notifications, study notes, generated documents, files, and images, as well as read incoming messages and draft responses.

---

## 🤖 Bot Profile & Credentials

- **Bot Username:** `@SamanAssist96_bot`
- **Bot Link:** [t.me/SamanAssist96_bot](https://t.me/SamanAssist96_bot)
- **Default Admin Chat ID:** `571568364` (Primary: Kd/Saman; unified Boss memory/reminders across `{571568364, 9063772144}`)
- **Configuration File:** `~/.config/telegram-sender/bot.env` (Permissions: `600`)

---

## 🚀 Quick Reference Commands

Task | CLI Command | Python Backend
:--- | :--- | :---
**Send Message to Admin** | `tg-bot-send --message "Hello"` | `python3 ~/.config/telegram-sender/bot_send.py --message "..."`
**Send File / Document** | `tg-bot-send --file "/path/to/file" --message "Caption"` | `python3 ~/.config/telegram-sender/bot_send.py --file "..." --message "..."`
**Send to Specific Chat/Group** | `tg-bot-send --target "<chat_id>" --message "..."` | `python3 ~/.config/telegram-sender/bot_send.py -t "<id>" -m "..."`
**Check New Messages / Inbox** | `tg-bot-updates` | `python3 ~/.config/telegram-sender/bot_updates.py`

---

## 🛠️ Workflows

### 1. Generating & Sending Files on Demand
When the user asks: *"এই বিষয়ের ওপর নোট/ফাইল বানিয়ে টেলিগ্রামে পাঠিয়ে দাও"* (e.g. "Create a study summary and send to Telegram"):
1. Create or write the file locally (e.g., in `/tmp` or workspace).
2. Execute:
   ```bash
   tg-bot-send --file "/path/to/created_file" --message "📄 [Brief description of file]"
   ```
3. Confirm delivery in the chat response.

### 2. Checking Inbox & Handling Incoming Messages
When the user asks: *"টেলিগ্রামে কোনো মেসেজ এসেছে কি না দেখো"* (e.g. "Check Telegram messages"):
1. Run `tg-bot-updates`.
2. Parse the sender name, username, chat ID, and message text.
3. Summarize the messages for the user.
4. When the user dictates a reply, execute:
   ```bash
   tg-bot-send --target "<sender_chat_id>" --message "<user_directed_reply>"
   ```

### 4. Dual-Mode Intelligence & Core Persona
The homeserver daemon `ai-telegram-commander.service` runs a dual-mode conversational engine powered by Gemini 2.5 Flash, tuned to a distinct personal identity:

#### 👑 Boss Identity & Aliases:
- **Primary Name:** Saman (সামান)
- **Real Name:** Kanad (কণাদ / কানাড)
- **Account Handle / Display Name:** Kd (কেডি)
- **Rule:** All three names refer to the **EXACT SAME individual** (Telegram Chat ID: `571568364`). If anyone in a group or DM mentions Saman, Kanad, Kd, or tags him, the bot immediately recognizes them as its creator and boss.

#### 🧠 Universal Persistent Memory Engine (`memories` table):
- **Remembering Facts / Preferences:** Anyone (Saman or guests) can say *"মনে রেখো..."*, *"Remember..."*, or *"Note this down"*. The bot saves facts and preferences permanently into SQLite.
- **Recall on Demand:** When asked *"আমার ব্যাপারে কী মনে আছে?"*, the bot recites remembered facts accurately.
- **Reminders for Saman/Kanad/Kd:** If a contact says *"সামান/কণাদকে মনে করিয়ে দিও..."*, the bot saves the reminder and **instantly fires an alert to Saman's phone**!

#### 🎭 Core Persona Blueprint:
- **Confident yet Grounded:** Calm, quiet authority in technical, scientific, and practical matters. Never arrogant, never groveling.
- **Intellectually Sharp:** Razor-sharp clarity and depth. Dissects complex concepts (science, philosophy, syllabus, tech) straight to their core without corporate filler.
- **Deeply Loyal:** 100% allegiance to Saman. Protects his privacy, time, mental clarity, and server security.
- **Drama-Free & Practical:** Emotionally mature, clear, pragmatic. Zero theatrics or sugarcoating; focuses on what actually works.
- **Witty:** Subtle, intellectual, dry humor. Clever observations with well-timed wry charm.
- **Anti-Poking & Zero Unsolicited Questions (Inviolable Law):** Strictly forbidden from asking unnecessary follow-up questions or conversational poking (e.g. "আর কী করব?", "কোন প্রজেক্টে রাখব?", "কোথায় অ্যাড করব?", "আর কিছু লাগবে কি?"). Autonomously makes the smartest logical routing decisions, executes directly, delivers concise closure, and stops without trailing chatter.

#### Operational Modes:
1. **Superuser Control Mode (Saman only - Chat ID `571568364`):**
   - Direct execution of maintenance commands, service diagnostics, container management, or system queries with superuser freewill.
2. **Companion & Intellectual Banter Mode (General Chat):**
   - Answers science, tech, lifestyle, or philosophical inquiries with deep substance, wit, and practical grounding (no robotic hardware dumps).
3. **Authentic Obsidian Vault MD-to-PDF Conversion Engine:**
   - Available to anyone who asks (*"সে যে-ই জিজ্ঞাসা করুক"* - Saman or guests/friends):
     - Searches `/mnt/saman-data/OBSIDIAN` for matching authentic `.md` notes.
     - **No Synthetic Textbooks:** The AI does NOT invent new notes from scratch or pose as an academic subject specialist.
     - When matching `.md` note(s) exist in the vault, it **directly converts the authentic markdown file into a polished PDF** using dual Latin (`FreeSans`) and Bengali (`NotoSansBengali`) typography and delivers the `.pdf` via Telegram `sendDocument`.
4. **Chat-Based Internet Knowledge Delivery (No Fake PDFs):**
   - If a topic has NO matching note in Obsidian, the bot **never generates a fake PDF**.
   - Instead, it pulls relevant facts from the internet / knowledge base and presents them **directly as concise, high-yield bullet points in the chat message**.
5. **Multimodal Vision & Image Analysis (Gemini 2.5 Flash Vision):**
   - Automatically downloads, inspects, and analyzes incoming images/photos/screenshots (from Saman or guests).
   - Solves exam questions and math problems, explains circuit/architecture diagrams, debugs terminal errors, and describes scenes in depth.
6. **Universal Peer-to-Peer Routing & 1-2 Line File Summary:**
   - Anyone can ask the bot to forward a message, photo, or file to anyone else (e.g., Guest -> Saman/Kanad/Kd, Saman -> Nabanita, User A -> User B).
   - **Automated 1-2 Line Summary:** Whenever ANY file, photo, or document is forwarded, the bot automatically inspects it and appends a **1 to 2 line Bengali summary** (`📌 সারসংক্ষেপ (১-২ লাইন): ...`) explaining what the file is about.
   - Never denies forwarding requests; resolves recipient aliases and user directory (`known_users`) gracefully.
7. **"30% Disclosure + 70% Resistance" Persona Rule:**
   - When external contacts inquire about Saman's exams, schedule, or current activities:
     - **No stone walls:** Does not rudely dismiss or say "I won't tell you".
     - **30% Context:** Shares tasteful, high-level context (his deep immersion in engineering/tech, self-hosted AI systems, and competitive technical exam prep like Railway RRB, SSC Tech, PSU/AE/JE).
     - **70% Resistance:** Witty and grounded protection of his private domain—reminding them with a smile that his day-to-day timetable and specific strategy remain locked in his own vault.
8. **Contact Memory & Briefing (`/opt/ai-maintainer/chat_memory.db`):**
   - All guest interactions are logged in SQLite. When Saman asks: *"নবানিতার সাথে কি কথা হয়েছে?"*, the bot analyzes the history and delivers a sharp, loyal debrief.
9. **🎙️ Multimodal Hands-Free Voice Intelligence:**
   - Listens to incoming Telegram voice notes (`voice`) and audio messages (`audio`).
   - Gemini 2.5 Flash transcribes and parses spoken Bengali/English, executing tasks, saving notes, or answering questions hands-free on the go.
10. **📄 Inbound PDF & Document Ingestion:**
   - Ingests sent PDF files (e.g. RRB/SSC notifications, question papers, code files).
   - Solves exam problems, extracts key dates, or forwards to another user with a 1-2 line summary.
11. **🎯 Live Kanboard Exam & Syllabus Co-Pilot (`kanboard_helper.py`):**
   - `/exams` / *"পরীক্ষার খবর"*: Fast read-only SQLite + JSON-RPC access to Project #4 (Govt Exam Tracker), including deep card credential extraction (Registration No, Roll No, Transaction ID, CEN/Advt) and natural-language card stage moves / `🤖 AI` score & note logging (e.g. *"Eta kanban board e update kore dao"* after uploading a scorecard).
   - `/exam_alerts` & Real-Time Priority Sentinel (`proactive-scheduler.service` + `kanboard_automator_v3.py`): Automatically pushes priority-ranked Telegram alerts (with saved Reg/Roll credentials & inline Kanboard buttons) whenever a tracked exam has a **Result Out**, **Admit Card Out**, **City Intimation Slip Out**, **Answer Key / Objection Window**, **Exam Date / Result Date Announced**, **DV/Interview Date**, **Stage Change**, or **`T-3d / T-1d / Today` Deadline** — suppressing negative filler (*"এখনও প্রকাশিত হয়নি"*) and `over-aged` / `❌ Not Selected` noise.
   - `/syllabus` / *"সিলেবাস আপডেট"*: Dynamic mastery overview of both Project #5 (All Subjects, 191 topics) and Project #6 (Mechanical & Applied Tech, 171 topics).
   - Topic Mastery Promotion: When Saman says *"Physics Sound পড়ে ফেললাম, লেভেল আপ করো"*, automatically advances matching topics across Project #5 & #6 to the next mastery column in Kanboard.
12. **☀️ Executive Daily Briefing (`/briefing`):**
   - High-yield Chief of Staff debrief combining Pi SoC temperature, load, upcoming exam milestones, syllabus focus, and pending contact reminders.
13. **🌐 Web Research & URL Unfurling:**
   - Automatically scrapes and analyzes shared web links/articles using BeautifulSoup + Gemini.
14. **📖 Isolated User Journals & Zero-Confusion Identity Engine (`user_journals` table):**
   - **Recognizes Returning Users:** Uses isolated memory dossiers keyed strictly by unique Telegram `user_id`. Greets returning users knowingly (e.g. remembering their name, relation, past topics, and preferences) without treating them like strangers.
   - **Strict Zero Cross-Contamination:** User A's memories, facts, and conversation history NEVER bleed into User B's context. Queries and conversation logs are strictly isolated by `user_id`.
   - **Self-Evolving Dossiers:** Automatically observes and saves key facts, preferences (e.g., drinks, birthdays, exams, cities), and behavioral observations into their journal.
   - **Boss Dossier Inspection:** When Saman asks `/journals` or *"X এর জার্নাল দেখাও"*, the bot delivers a comprehensive profile report for any contact.
15. **📋 Live Vikunja Task & Deadline Sentinel:**
   - `/vikunja` / `/tasks` / *"কি কাজ বাকি"* / *"টাস্ক তালিকা"*: Real-time query of `/opt/vikunja/db/vikunja.db`. Formats all pending tasks with deadline badges (🔴 Overdue, ⏳ Due Today, 📅 Upcoming, ⚪ Normal) with direct 1-click links to Vikunja (`:3456`) and the Dopamine Decision Wheel (`:8855`).
   - **Proactive Deadline Sentinel (`proactive-scheduler.service`):** Continuously monitors task due dates; fires immediate high-priority alerts when a deadline approaches (within 3 hours) or becomes overdue.
   - **Scheduled Circadian Check-ins:**
     - Morning Briefing (08:00 AM): Displays pending tasks, overdue alerts, and today's deadlines.
     - Midday Decision Breaker (02:00 PM): Directly combats midday decision paralysis with pending tasks & Decision Wheel prompt.
     - Evening Review (09:30 PM): Accountability check-in reviewing completed and remaining tasks.
16. **🎯 Live Smart 'এখন কি করব' Recommendation Engine:**
   - **Triggers:** `/now` / `/recommend` / `/suggest` / `/decision` / `/wheel` / `/spin` / *"এখন কি করব"* / *"কী করলে ভালো হয়"* / *"ফাঁকা আছি কি করব"* / *"সিদ্ধান্ত নিতে পারছি না"* / *"কি কাজ করব"* / *"achon ki korbo"*.
   - **Strict Priority Hierarchy:** Structured directly by **Emergency > Important > Necessary > Productive > Other**:
     1. 🚨 **জরুরি (Emergency):** Hardware overheating (SoC >= 75°C), Vikunja overdue tasks (ডেডলাইন পার হয়ে গেছে), imminent reminders (<= 15 mins).
     2. 🔴 **গুরুত্বপূর্ণ (Important):** Vikunja tasks due today, upcoming exams (Project #4 within 7 days/admit cards), priority >= 3 tasks.
     3. 🟡 **প্রয়োজনীয় (Necessary):** Vikunja tasks due soon, syllabus backlog topic to master (Project #5), routine operations.
     4. 🟢 **ফলপ্রসূ (Productive):** Real-time Circadian deep work sprint (Oakley/Newport Quant PYQ in morning, NSDR dopamine reset at midday, AK Da Don calisthenics in evening, Alex Libin pelvic realignment at night).
     5. ⚪ **অন্যান্য (Other):** Stoic evening diary, posture correction, audiobookshelf listening, and 1-click Dopamine Decision Wheel spin.
   - **Autonomous Top 1 Selection:** Automatically crowns the highest available tier's item as the **🥇 Top 1 Action**, so crises/deadlines are eliminated first before leisure or secondary study.
   - **Rich Multimodal Delivery:** Attaches relevant visual infographics (e.g. `study_framework.jpg`, `book_posture.jpg`, `calisthenics.jpg`, `pelvic_bedtime.jpg`) with 1-click inline action buttons (`:8855`, `:3456`, `:13378`).
17. **🎯 Interactive Note-Based MCQ Practice Engine (`/mcq`):**
   - **Triggers:** `/mcq`, `/quiz`, `/practice`, *"History থেকে MCQ দাও"*, *"English প্র্যাকটিস করব"*, *"নোট থেকে প্রশ্ন দাও"*, etc.
   - **Behavior:** Dispatches competitive exam standard MCQs derived directly from authentic Obsidian markdown notes (`/mnt/saman-data/OBSIDIAN/Gov-Exam-Prep/`) with inline option buttons (`[ A ] [ B ] [ C ] [ D ]`).
   - **Instant Feedback:** Answers via callback toast and inline edit showing correct/incorrect status, explanation from note, and a `[ ➡️ পরবর্তী প্রশ্ন ]` button for an endless revision loop.
18. **⏰ Scheduled Natural Language Timed Reminders Engine (`reminder_helper.py`):**
   - **Triggers:** *"কাল সকাল ১০টায় মনে করিয়ে দিও..."*, *"১৫ মিনিট পর মনে করাও..."*, *"আজ রাত ১১টায় ওষুধ খাওয়ার কথা মনে করিয়ে দিও"*, `/reminders`, `/reminder`.
   - **Behavior:** Parses relative and absolute dates/times (both fast regex and Gemini 2.5 Flash), saves to SQLite `scheduled_reminders` (`chat_memory.db`), and optionally creates a synced Vikunja task with `due_date`.
   - **Autonomous Push Dispatch:** The `proactive-scheduler.service` loop checks pending reminders every 20 seconds. Exactly when due, fires a high-priority Telegram alert with inline `[ ✅ সম্পন্ন হয়েছে (Mark Done) ]` and `[ 📋 Vikunja টাস্ক ]` buttons.
   - **One-Click Completion:** Tapping the done button automatically marks the reminder completed in SQLite and closes the task in Vikunja.
19. **🎛️ Telegram Native UI Experience & 1-Click Button Control:**
   - **Bot Command Autocomplete Menu (`setMyCommands`):** Fully registered in Telegram's native `[/]` menu with Bengali descriptions (`/menu`, `/now`, `/mcq`, `/vikunja`, `/reminders`, `/briefing`, `/exams`, `/exam_alerts`, `/syllabus`, `/wheel`, `/wifi`).
   - **Persistent Bottom Reply Keyboard:** Permanently pinned 6-button quick access grid beneath the chat box (`[ 🎯 এখন কি করব ]`, `[ 📝 নোট MCQ প্র্যাকটিস ]`, `[ 📋 Vikunja টাস্ক ]`, `[ ⏰ রিমাইন্ডার লিস্ট ]`, `[ ☀️ আজকের ব্রিফিং ]`, `[ 🎛️ কন্ট্রোল মেনু ]`).
   - **Interactive Master Dashboard (`/menu`, `/start`):** Inline control panel with 1-click execution buttons for all major features and dashboard web links.
   - **MCQ Subject Picker Grid:** Inline buttons for selecting subjects (`📜 History`, `📖 English`, `⚖️ Polity`, `🌍 Geography`, `🔬 Science`, `🧮 Math`).
   - **Contextual In-Chat Actions:** Every bot response includes immediate next-step buttons, eliminating the need to ever type or remember commands manually.
20. **📋 Intelligent Vikunja Task Operations (Smart Project Routing & 1-Tap Completion):**
   - **Smart Auto-Project Categorization:** When adding tasks (e.g. *"GS এ যোগ করো: প্রাচীন মন্দির..."*, *"Math মক দিতে হবে"*), automatically categorizes into the exact Vikunja project (`📘 GS (General Studies)`, `🎯 Govt Job Prep`, `📊 Mock Test & Revision`, `📰 Current Affairs`, `🕒 Daily Routine`, or `Inbox`).
   - **Natural Language Tick-Marking:** Instantly marks tasks done by title, keyword, or ID (*"sports dekte hobe tick mark dao"*, *"caves complete"*). Cross-syncs completion timestamps across Vikunja and SQLite.
   - **1-Click Completion Inline Buttons:** When listing tasks (`/vikunja` or `cmd:vikunja`), renders clickable inline buttons (`[ ✅ {title} (টিক দিন) ]`), allowing Saman to complete tasks on the fly with a single tap.
21. **🎯 Telegram Native Reply-To-Message Intelligence & Direct Wi-Fi Whitelisting:**
    - **Native Reply Tracking:** Automatically captures Telegram's `reply_to_message` payload, extracting replied message text, media type, sender name, and message ID.
    - **Context-Aware Reasoning:** Injects the full context of the replied-to message directly into Gemini (for Saman, Baba, or Guests). Enables natural conversation when swiping to reply (e.g. *'Eta kano holo na?'* on an MCQ, *'Hoyegache'* on a task, or *'Cancel koro'* on a reminder).
    - **Pinpoint Wi-Fi Device Approval:** When multiple device alerts are active, swiping to reply to a specific alert message (e.g. *'Eta amader Xiaomi phone'* or *'Allow'*) extracts the exact MAC and IP from that specific message and immediately whitelists that device in `known_macs.json`.
22. **🎧 Autonomous Music & Playlist Co-Pilot (`playlist_helper.py`):**
    - **Dynamic Playlist Discovery:** Reads and indexes all 25 active Navidrome `.m3u` playlists from `/mnt/saman-data/Music/Playlists/`.
    - **Relational Track Matching:** Accurately interprets relational commands (e.g. *"Solace যে প্লেলিস্টে আছে সেই প্লেলিস্টে রাখো"*), locates all reference playlists (`🍃 Chill`, `Healing 🌱`), and appends the active song with an instant Navidrome rescan.
    - **Zero Substring Traps & Stop-Word Guard:** Command and action words (`"add"`, `"koro"`, `"jog"`, `"eta"`, `"theke"`) are strictly blacklisted from audio file path searches to eliminate catastrophic false substring hits (such as `"add"` falsely matching artist *"Shraddha Srinath"* in unrelated tracks).
    - **Reply-To Music Resolution:** When Saman swipes to reply to a YouTube URL or a music download confirmation message with *"Eta [playlist] playlist e add koro"*, the system extracts the referenced link or song title directly from `reply_context` instead of defaulting to stale memory.
    - **Strict Mood Integrity & Universal Anti-Literalism:** High-energy motivational / workout anthems belong strictly to `⚡ Adrenaline-Workout.m3u` and are permanently barred from `🥀 Sad.m3u`. User corrections are treated as general systemic invariants (Anti-Literalism Axiom) rather than isolated one-off string patches, triggering proactive scans across all playlists to keep library curation consistent and mood-aligned.
    - **Immediate Navidrome Rescan:** Every playlist update triggers `docker exec navidrome /app/navidrome scan` within 3 seconds, ensuring new tracks and purges are instantly synchronized to mobile and web streaming apps.
    - **Interrogative Regex Protection:** Explicitly prevents Bengali/Banglish question words (`kon`, `ki`, `kono`, `kontay`, `কোন`, `কোনটা`, `কি`, `which`, `what`) from falsely triggering playlist addition, routing questions directly to the playlist recommendation engine.
    - **1-Click Interactive Telegram UI:** Automatically attaches interactive inline buttons to downloaded YouTube songs and recommendation replies, enabling 1-tap addition without manual typing.
23. **🛡️ Wi-Fi Sentry Alert-Once Architecture & Randomized MAC Handling (`wifi_sentry.py`):**
    - **Boss-Only Intruder Alerts:** Raw MAC/IP network alerts dispatch strictly to Boss accounts (`571568364`, `9063772144`) — never forwarded to Baba's account (`8855420256`).
    - **Strict Alert-Once Lifecycle (`alerted_macs.json`):** Unwhitelisted devices are alerted **EXACTLY ONCE** in their lifetime. Subsequent connections quietly update timestamps in the background.
    - **Calm Randomized MAC Triage:** Detects locally administered (randomized Android/iOS Private Wi-Fi) MACs cleanly with lower urgency and includes `[ 🔕 সব র‍্যান্ডম MAC ক্লিয়ার করুন ]` (`wifi_dismiss_rand`) for 1-tap bulk clearing.
    - **mDNS Hostname Resolution:** Actively queries multicast DNS (`5353/UDP`) to discover real device hostnames (e.g. `Samsung.local`, `Android-5.local`), revealing the physical device name even when hardware MAC is randomized.
    - **1-Click Control Buttons:** Every intruder alert includes `[ ✅ হ্যাঁ, পরিচিত (Allow) ]`, `[ ⏱️ অতিথি পাস (24h Guest) ]`, and `[ 🔕 মিউট (Dismiss) ]`.

---

### 24. Zero-Key Local Antigravity Upgrades (`bot_send.py` / `tg-bot-send`)

The local [bot_send.py](file:///home/saman/.config/telegram-sender/bot_send.py) sender used by `tg-bot-send` (independent from the Raspberry Pi's daemon) now supports:
- **Smart Media Auto-Routing:** `.ogg`/`.opus` → `sendVoice`, `.mp3`/`.wav`/`.m4a` → `sendAudio`, `.mp4`/`.mov`/`.webm` → `sendVideo` (streaming), `.png`/`.jpg`/`.webp` → `sendPhoto`, and documents → `sendDocument` (pass `--as-document` to force raw document transfer).
- **4000-Char Auto-Chunking & Safe HTML Fallback:** Long reports/summaries are automatically split cleanly along paragraph/line bounds, and unescaped HTML angle brackets fall back to plain text instead of failing.
- **Offline `Piper` Voice-Note Briefings (Zero API Key):**
  ```bash
  tg-bot-send --voice-note --message "Morning study briefing: complete Heat Transfer revision and 20 PYQs."
  tg-bot-send --voice-note --tts-text "Spoken revision summary" --message "📄 Written transcript caption"
  ```
- **Connected Local Pipelines (Zero API Key):**
  - **YouTube / Web → Telegram Digest:** Extract offline transcripts (`youtube` skill) or clean web articles (`defuddle parse <url> --md`), summarize, and dispatch cleanly to Telegram.
  - **Revision Shorts / Reels → Telegram Video:** Render 30–40s vertical study/code shorts (`faceless-shorts` `make-short` `--provider piper` or `openmontage`) and send playable MP4s directly via `tg-bot-send --file output.mp4`.
  - **Exam Quiz & Study Cards:** Pair directly with [quiz_generator.py](file:///home/saman/.gemini/config/plugins/exam-quiz-engine/skills/exam-quiz-engine/scripts/quiz_generator.py) and `obsidian` flashcard exports.

---

### 25. 🛰️ Autonomous Chat Sentinel & Self-Healing Engine (`telegram_audit_sentinel.py`)

The local autonomous sentinel ([telegram_audit_sentinel.py](file:///home/saman/.agents/skills/telegram/scripts/telegram_audit_sentinel.py)) audits Telegram conversations between the Homeserver daemon (`@SamanAssist96_bot`) and users, diagnosing anomalies and auto-remediating failures:

- **Audit & Self-Healing Capabilities:**
  1. **Autonomous Junior-Mess Cleanup Engine (স্বয়ংক্রিয় জুনিয়র ত্রুটি নিরাময়):** Continuously inspects conversational friction markers (`"bhul"`, `"ভুল"`, `"hallucination"`, `"koi hoeche"`, `"link kothay"`, `"eta na"`, `"bad dao"`, `"mess"`). When a junior bot mistake is identified (e.g., wrong song added to a playlist, false completion confirmation, misplaced documents), the supervisor immediately rolls back the bad mutation (purging wrong tracks from `.m3u` on desktop and homeserver, rescanning Navidrome), fulfills the true intent, and updates the Obsidian satisfaction journal (`🟡 Auto-Healed`) without manual intervention.
  2. **Proactive Invariant & Mood Integrity Auditing:** Periodically audits all 25 playlists (`.m3u`) for duplicate lines, broken/dead paths, and genre/mood cross-contamination (e.g. barring workout anthems from `🥀 Sad.m3u` and melancholic weeping tracks from `⚡ Adrenaline-Workout.m3u`), auto-relocating misplaced tracks cleanly.
  3. **Unfulfilled Media Relay / Forwarding:** Detects when Saman replies to documents, photos, or voice notes asking to forward them to contacts (e.g. *"Eta nabanita k pathao"* or Baba). Extracts replied file IDs, verifies receipt, and automatically delivers missing media via `tg-bot-send`.
  4. **Raw JSON Leak & Escape Prevention:** Catches assistant responses containing raw JSON or unescaped LaTeX backslashes (`\cdot`, `\frac`), ensures clean conversation rendering, and applies parser resiliency patches to the homeserver.
  5. **Topic Resolution & Note Precision:** Prevents false note matches (e.g. delivering English Grammar Tricks when Math series formulas were requested) by prioritizing substantive subject keywords over raw number sequences and boosting scores only on verified query matches.
  6. **False Silence & Mute Protection:** Detects accidental bot muting triggered by typos (e.g. *"Digub"*) and ensures uninterrupted conversational assistance.
  7. **URL Sanitization & Delegation:** Strips trailing punctuation from shared URLs (`https://...`) and safely routes them to the autonomous media/playlist queues (`Love ❤️.m3u`).
  8. **Date-wise Supervisor Journal & Satisfaction Tracking:** Maintains real-time date-wise audit logs and satisfaction metrics in Obsidian (`server_setup/05_Kanban & Tasks/Telegram_Supervisor_Journal.md`) with a dedicated Junior-Mess Cleanup Log table.
- **Antigravity Startup Hook Integration (`SessionStart`):**
  - Wired into [hooks.json](file:///home/saman/.agents/hooks.json). Whenever Antigravity launches, the sentinel queries recent conversations and immediately injects high-priority alerts with exact error summaries if any unresolved failures exist.
- **Continuous Background Daemon / Timer:**
  - Configured as a systemd user timer (`systemctl --user status telegram-audit-sentinel.timer`) running every 5 minutes in the background, keeping Telegram bot operations 100% reliable, self-healing, and error-free.
- **CLI Commands:**
  ```bash
  # Check and output hook payload
  python3 ~/.agents/skills/telegram/scripts/telegram_audit_sentinel.py --check

  # Detailed audit report
  python3 ~/.agents/skills/telegram/scripts/telegram_audit_sentinel.py --audit

  # Autonomous remediation
  python3 ~/.agents/skills/telegram/scripts/telegram_audit_sentinel.py --auto-fix
  ```


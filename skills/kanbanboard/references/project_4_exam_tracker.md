# Project #4: 🎯 Govt Exam Tracker (Auto) Specification

## 1. Project Overview
* **Project ID:** `4`
* **Name:** `🎯 Govt Exam Tracker (Auto)`
* **Status:** Active (`is_active: 1`)
* **Purpose:** Centralized, automated tracker for government competitive examinations across Central & State boards (UPSC, SSC, RRB, DRDO, WBPSC, State departments).
* **Automator Integration:** Synced with `/opt/kanbanboard_automator/kanboard_automator_v2.py` running daily on the homeserver.

---

## 2. Examination Lifecycle Columns (18 Stages)

Position | Column ID | Column Title | Description
:--- | :--- | :--- | :---
1 | `28` | 📥 To Apply | Upcoming exams or notifications identified for future application.
2 | `29` | 🟢 Application Ongoing | Active application window currently open.
3 | `30` | 📝 Applied | Application submitted; registration number/fee confirmed.
4 | `31` | 🗺️ City Slip Out | Advance city intimation slip released by exam board.
5 | `32` | 🎫 Admit Card Out | Hall ticket / admit card available for download.
6 | `33` | 💻 CBT 1 Done | Computer Based Test 1 completed.
7 | `34` | ⏳ Awaiting CBT 1 Result | Awaiting tier-1 cutoff and merit list.
8 | `35` | ✅ CBT 1 Qualified | Cleared tier-1; preparing for tier-2.
9 | `36` | 🎫 CBT 2 Admit Out | Tier-2 admit card issued.
10 | `37` | 🧪 CBT 2 Done | Computer Based Test 2 completed.
11 | `38` | ⏳ Awaiting CBT 2 Result | Awaiting tier-2 / mains marks & merit list.
12 | `39` | ✅ CBT 2 Qualified | Qualified tier-2; proceeding to document verification/interview.
13 | `40` | 👨‍💼 DV/Interview Scheduled | Call letter received for DV or Interview.
14 | `41` | 🪪 DV/Interview Done | Verification and physical test completed.
15 | `42` | ⏳ Final Result Awaited | Waiting for final selection roll list.
16 | `43` | 🎉 Selected | Final merit selection achieved!
17 | `44` | ❌ Not Selected | Archive for cycles that concluded without selection.
18 | `45` | 🚫 Cancelled/Postponed | Notifications withdrawn, stayed, or rescheduled.

---

## 3. Registered Tags Taxonomy (35 Tags)
* **Exam Categories:** `SSC`, `cgl`, `chsl`, `mts`, `JE`, `RRB`, `ntpc`, `ALP`, `GroupD`, `DRDO`, `CEPTAM`, `UPSC`, `WBCS`, `WBPSC`, `FoodSI`, `STATE`, `IES`, `ESE`, `MIS`
* **Educational Qualification:** `10thPass`, `12thPass`, `Graduate`, `UnderGraduate`, `Engineering`, `CSE`, `Science`
* **Notification Years:** `2024`, `2025`, `2026`, `2027`
* **Regions / Context:** `Guwahati`, `Bengali`, `central`, `backup`

---

## 4. Current Examinations Roster (Sample)
* `Task #75`: 🛡️ DRDO CEPTAM Admin & Allied (A&A) - Late 2026 / 2027 (📥 To Apply)
* `Task #81`: 🏆 SSC MTS 2026 (📥 To Apply)
* `Task #90`: 🇮🇳 UPSC Civil Services Exam 2027 (📥 To Apply)
* `Task #95`: 🚂 RRB ALP 2027 (📥 To Apply)
* `Task #85`: 🏛️ WB Gram Panchayat Recruitment 2026 (🟢 Application Ongoing)
* `Task #89`: 🏛️ WBCS Exam 2027 (🟢 Application Ongoing)
* `Task #96`: 🏛️ Food SI 2026 WBPSC (🟢 Application Ongoing)
* `Task #77`: 🚂 RRB NTPC 2026-27 (📝 Applied)
* `Task #82`: 🏛️ WBPSC Clerkship 2026 (📝 Applied)
* `Task #86`: 🚂 RRB ALP 2026 (📝 Applied)
* `Task #92`: 🚂 RRB JE 2026 (📝 Applied)
* `Task #91`: 🚂 RRB Section Controller 2026 (💻 CBT 1 Done)
* `Task #74`: 🚂 RRB Level-1 Group D (⏳ Awaiting CBT 1 Result)

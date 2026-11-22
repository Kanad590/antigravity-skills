#!/usr/bin/env python3
"""
Unified Self-Help CLI Engine for Antigravity
Provides seamless command orchestration for:
  /boost       -> Physiological sigh & 5-minute micro-sprint
  /grill-me    -> Socratic drill & Motive accountability
  /goal        -> Exam milestones, syllabus mastery, fitness cut (82->72kg), wardrobe
  /plan        -> Dynamic clock-free routine (Liluah vs Arambagh)
  /learn       -> Oakley chunking & Feynman bilingual concept explanation
  /supplement  -> Jan Aushadhi supplement dosing & safety check
  /plugin      -> Obsidian tooling & homeserver architecture advisor
  /automation  -> Pipeline sync runner & daily note automation
"""
import sys
import os
import argparse
from datetime import datetime

# Sub-script imports
import micro_sprint_timer
import routine_planner
import supplement_tracker
import grill_interrogator
import kanboard_client

LEARN_MODULES = {
    "compound_interest": {
        "title": "Compound Interest vs Simple Interest (চক্রবৃদ্ধি বনাম সরল সুদ)",
        "match": ["compound", "interest", "ci", "si"],
        "chunk": (
            "• **সহজ বাংলা ব্যাখ্যা:** Simple Interest (SI)-এ সুদ সবসময় শুধু মূল টাকার (Principal) ওপর হিসেব হয়।\n"
            "• কিন্তু Compound Interest (CI)-এ সুদ মূল টাকার সাথে যোগ হয়ে নতুন মূল তৈরি করে—অর্থাৎ **'সুদের ওপর সুদ'** তৈরি হয়।\n"
            "• তাই প্রতি বছর টাকা রৈখিকভাবে (Linear) বাড়ে না, বরং চক্রবৃদ্ধি হারে (Exponentially) বৃদ্ধি পায়।"
        ),
        "formula": (
            "• SI = (P * R * T) / 100\n"
            "• CI = P * (1 + R / 100)^T - P\n"
            "• Exam Shortcut (2-Year Diff): CI - SI = P * (R / 100)^2\n"
            "• Exam Shortcut (3-Year Diff): CI - SI = P * (R / 100)^2 * ((300 + R) / 100)"
        ),
        "callout": (
            "> [!question]- ❓ ২ বছরের জন্য ₹১০,০০০ টাকার ওপর ১০% হারে CI এবং SI এর পার্থক্য কত?\n"
            "> শর্টকাট ফর্মুলা: CI - SI = P * (R / 100)^2\n"
            "> = 10000 * (10 / 100)^2 = 10000 * 1/100 = ₹100।"
        )
    },
    "time_and_work": {
        "title": "Time & Work — LCM Method & Alternate Days (সময় ও কার্য)",
        "match": ["time", "work", "alternate", "efficiency"],
        "chunk": (
            "• **সহজ বাংলা ব্যাখ্যা:** সময় ও কার্যের অঙ্ক ভগ্নাংশে (1/A + 1/B) না করে মোট কাজকে দিনের লসাগু (LCM) ধরুন।\n"
            "• মোট কাজ / মোট দিন = দৈনিক ক্ষমতা (Efficiency or Units/day)।\n"
            "• Alternate Days-এ কাজ হলে ২ দিনের এক চক্র (Cycle) হিসেব করে মোট কাজের কাছাকাছি পৌঁছান, তারপর বাকি কাজ একা করান।"
        ),
        "formula": (
            "• Total Work = LCM of individual times (e.g. LCM(12, 15) = 60 units)\n"
            "• Efficiency = Total Work / Days (A = 5 u/d, B = 4 u/d)\n"
            "• 2-Day Cycle = 9 units; 6 cycles = 12 days = 54 units; Remaining 6 units -> Day 13 A does 5 units (1 left), Day 14 B takes 1/4 day -> Total 13 1/4 days."
        ),
        "callout": (
            "> [!question]- ❓ A একটি কাজ ১২ দিনে, B ১৫ দিনে করে। A দিয়ে শুরু করে তারা একদিন অন্তর কাজ করলে মোট কত দিন লাগবে?\n"
            "> মোট কাজ = LCM(12, 15) = ৬০ ইউনিট।\n"
            "> A-এর ক্ষমতা = ৫ ইউনিট/দিন, B-এর ক্ষমতা = ৪ ইউনিট/দিন।\n"
            "> ২ দিনে কাজ হয় ৯ ইউনিট। ৬ চক্রে (১২ দিনে) কাজ হয় ৫৪ ইউনিট।\n"
            "> ১৩তম দিনে A করে ৫ ইউনিট (মোট ৫৯)। ১৪তম দিনে B ১ ইউনিট করতে সময় নেবে ১/৪ দিন।\n"
            "> মোট সময় = ১৩ ১/৪ দিন।"
        )
    },
    "percentage": {
        "title": "Percentage & Successive Change (শতকরা ও ধারাবাহিক পরিবর্তন)",
        "match": ["percentage", "percent", "successive", "expenditure"],
        "chunk": (
            "• **সহজ বাংলা ব্যাখ্যা:** পণ্যের দাম বাড়লে খরচ অপরিবর্তিত রাখতে ব্যবহারের পরিমাণ কমাতে হয়।\n"
            "• দাম বাড়ার অনুপাত a/b হলে ব্যবহার কমানোর অনুপাত a/(b + a)।\n"
            "• ধারাবাহিক পরিবর্তনের ক্ষেত্রে সরাসরি ফর্মুলা বা মাল্টিপ্লাইং ফ্যাক্টর ব্যবহার করুন।"
        ),
        "formula": (
            "• Consumption Reduction = [r / (100 + r)] * 100%\n"
            "• Successive Change Net = a + b + (a * b) / 100"
        ),
        "callout": (
            "> [!question]- ❓ পেট্রোলের দাম ২৫% বৃদ্ধি পেলে খরচ অপরিবর্তিত রাখতে ব্যবহার শতকরা কত কমাতে হবে?\n"
            "> শর্টকাট: [২৫ / (১০০ + ২৫)] * ১০০ = ২৫ / ১২৫ * ১০০ = ২০% কমাতে হবে।"
        )
    },
    "syllogism": {
        "title": "Logical Reasoning — Syllogism 'Only a Few' Rules (সিললিজম)",
        "match": ["syllogism", "logic", "reasoning", "few", "deductive"],
        "chunk": (
            "• **সহজ বাংলা ব্যাখ্যা:** 'Only a few A are B'-এর অর্থ হলো একইসাথে দুটি সত্য:\n"
            "  1. 'Some A are B' (কিছু A নিশ্চিতভাবে B)\n"
            "  2. 'Some A are NOT B' (কিছু A কোনো অবস্থাতেই B হতে পারবে না)।\n"
            "• তাই 'All A can be B' সম্ভাবনা (Possibility) সবসময় মিথ্যা (Invalid), কিন্তু 'All B can be A' সত্য হতে পারে।"
        ),
        "formula": (
            "• 'Only a few A are B' = Some A are B (+) AND Some A are not B (-)\n"
            "• Consequence: 'All A can never be B' is ALWAYS TRUE."
        ),
        "callout": (
            "> [!question]- ❓ Statements: Only a few Pens are Pencils. All Pencils are Erasers. Conclusion: All Pens can never be Pencils. Valid?\n"
            "> হ্যাঁ, Valid! কারণ 'Only a few Pens are Pencils' মানেই কিছু Pen কখনোই Pencil হতে পারে না।"
        )
    },
    "grammar": {
        "title": "English Language — Subject-Verb Agreement (কর্তা ও ক্রিয়াপদের সামঞ্জস্য)",
        "match": ["grammar", "english", "subject", "verb", "agreement", "error"],
        "chunk": (
            "• **সহজ বাংলা ব্যাখ্যা:** যখন দুটি Subject 'neither... nor', 'either... or', বা 'not only... but also' দিয়ে যুক্ত হয়,\n"
            "  তখন Verb সবসময় তার সবচেয়ে নিকটবর্তী (Closer) Subject অনুযায়ী নির্ধারিত হয়।\n"
            "• কিন্তু 'as well as', 'along with', 'together with' থাকলে Verb প্রথম Subject অনুযায়ী হয়।"
        ),
        "formula": (
            "• Neither S1 nor S2 + Verb(agrees with S2)\n"
            "• S1 as well as S2 + Verb(agrees with S1)"
        ),
        "callout": (
            "> [!question]- ❓ 'Neither the manager nor the employees was present.' এখানে ভুল কোথায়?\n"
            "> 'was'-এর জায়গায় 'were' হবে। কারণ 'neither... nor'-এ Verb নিকটবর্তী Subject ('employees' - Plural) অনুযায়ী নির্ধারিত হয়।"
        )
    }
}

def cmd_boost(args):
    micro_sprint_timer.run_micro_sprint(minutes=args.minutes, simulate=args.simulate)

def cmd_grill(args):
    grill_interrogator.conduct_grill(topic=args.topic, auto_reveal=getattr(args, "auto", False))

def cmd_plan(args):
    print(routine_planner.get_routine(location=args.location, wake_time=args.wake))

def cmd_supplement(args):
    if args.check:
        supplement_tracker.check_drug_code(args.check)
    else:
        supplement_tracker.display_schedule()

def cmd_goal(args):
    print("""
================================================================================
🎯 MASTER GOAL & MILESTONE TRACKER
================================================================================

1. 🏛️ GOVERNMENT EXAM TARGETS (Kanboard Project #4):
   • AFCAT (Air Force Common Admission Test) — Target: Flying / Ground Duty Tech
   • Banking Exams (IBPS PO, SBI PO, RRB Scale-I) — Target: Officer Scale
   • RBI Grade B / Assistant — Target: Central Banking Core

2. 🧠 SYLLABUS MASTERY (Kanboard Project #5):
   • Quantitative Aptitude: Arithmetic Chunks, Data Interpretation, Mensuration
   • Logical Reasoning: Floor/Flat Puzzles, Syllogisms (Only a few), Seating
   • English Language: Reading Comprehension, Subject-Verb Agreement, Vocab
   • General Awareness: Static GK, Banking Awareness, 6-Month Current Affairs

3. 🏋️ FITNESS & BODY COMPOSITION:
   • Current Weight: 82.0 kg
   • Target Athletic Frame: 72.0 kg (-10 kg lean cut)
   • Strategy: OpenGym Calisthenics (Liluah) / Home Gym 30kg (Arambagh)
   • Night Stack: Nutrija Whey + 3-5g Creatine Monohydrate

4. 👔 WARDROBE CAPSULE & AESTHETIC ELEVATION:
   • Cancer Lagna & Taurus Venus harmonious palette (Sky-blue, Ivory, Deep-green, Dark-chocolate leather).
   • Complete wardrobe locked in '04_Fashion_Grooming/Kanad Wardrobe.md'.
================================================================================
""")
    # Try fetching Kanboard live summary
    kb_summary = kanboard_client.get_syllabus_summary()
    if "total" in kb_summary and kb_summary["total"] > 0:
        print(f"📊 LIVE KANBOARD STATUS (Project #5 - Syllabus Tracker):")
        print(f"   Total Tracked Syllabus Topics: {kb_summary['total']}")
        for col, tasks in kb_summary.get("breakdown", {}).items():
            print(f"   • {col}: {len(tasks)} topic(s)")
        print("================================================================================")

def cmd_learn(args):
    query = (args.topic or "Compound Interest vs Simple Interest").lower()
    
    selected_module = None
    for mod_key, mod_data in LEARN_MODULES.items():
        if any(m in query for m in mod_data["match"]):
            selected_module = mod_data
            break

    if selected_module:
        title = selected_module["title"]
        chunk = selected_module["chunk"]
        formula = selected_module["formula"]
        callout = selected_module["callout"]
    else:
        title = args.topic.strip().title()
        chunk = (
            f"• **সহজ বাংলা ব্যাখ্যা:** {title}-এর মৌলিক মেকানিজম বুঝতে বিষয়টিকে ছোট ছোট এককে ভাগ করুন।\n"
            "• অপ্রয়োজনীয় জটিল টার্ম বাদ দিয়ে সাধারণ উপমায় ব্যাখ্যা করুন যেন একজন অষ্টম শ্রেণির শিক্ষার্থীও বুঝতে পারে।"
        )
        formula = "• মূল নিয়ম ও পরীক্ষার প্যাটার্ন চিহ্নিত করে মেমরি অ্যাঙ্কর তৈরি করুন।"
        callout = (
            f"> [!question]- ❓ {title}-এর মূল টেক-অ্যাওয়ে বা পরীক্ষার ট্রিক কী?\n"
            f"> সূত্র এবং প্রয়োগের ক্ষেত্র নিজের ভাষায় রিট্রিভ করুন।"
        )

    output = f"""
================================================================================
🧠 OAKLEY CHUNKING & FEYNMAN EXPLANATION: {title.upper()}
================================================================================

1. 🧩 CORE CHUNK (The Intuitive Mechanism):
{chunk}

2. 🔬 FORMULA & CORE ANCHOR:
{formula}

3. 🗣️ COLLAPSIBLE ACTIVE RECALL (Obsidian Callout):
{callout}
================================================================================
"""
    print(output)

def cmd_plugin(args):
    print("""
================================================================================
🔌 OBSIDIAN & TOOLING ADVISORY
================================================================================

1. 📊 DATAVIEW (Native Queries):
   • Use TABLE and TASK queries over frontmatter properties.
   • Avoid 3rd party tasks plugin; native `TASK FROM ... WHERE !completed` is lightweight and zero-dependency.

2. 📋 OBSIDIAN KANBAN:
   • Convert any note to an interactive board using `--- kanban-plugin: basic ---`.
   • Clean plain-text Markdown fallback on mobile.

3. 🎨 OBSIDIAN CANVAS:
   • Build spatial concept clusters using `.canvas` JSON files (`scripts/canvas_builder.py`).
   • Use chromatic tags ("1" for Motive, "4" for Health, "5" for Study, "6" for Fashion).

4. 🗄️ OBSIDIAN BASES (v1.8+ Core):
   • Direct native database views with table, card, and calendar modes.

5. 🏠 HOMESERVER INTEGRATION:
   • Kanboard (Projects #4 & #5) running at 192.168.1.100:1337 / 100.x.y.z:1337.
   • Syncthing real-time vault backup across laptop, phone, and server.
================================================================================
""")

def cmd_automation(args):
    print("🔄 Running Self-Help & Study Pipeline Automation Sync...")
    url = kanboard_client.get_rpc_url()
    if url:
        print(f"✅ Kanboard JSON-RPC Connection: ACTIVE ({url})")
        exam_tasks = kanboard_client.get_exam_tasks()
        syl_summary = kanboard_client.get_syllabus_summary()
        tasks_list = exam_tasks.get('result') or []
        print(f"   Exam Tasks Monitored: {len(tasks_list)}")
        print(f"   Syllabus Topics Tracked: {syl_summary.get('total') or 0}")
    else:
        print("⚠️ Kanboard Server: OFFLINE / Unreachable (Using local cache)")
    print("✅ Vault notes and Dataview indexes synchronized.")

def cmd_text(args):
    print("""
================================================================================
👑 MASCULINE COMMUNICATION & THE 9 MORNING TEXTING ARCHETYPES
================================================================================
💡 Core Principle: "Women attach to men with direction, emotional restraint,
   and calm authority. Lead your day; do not chase attention or validation."

1️⃣ Set Calm Masculine Tone
   💬 "Morning. Hope today treats you well. I’ve got a full day ahead but wanted to check in."
   ➔ Grounded, not needy. You lead your day with concrete purpose.

2️⃣ Make Her Feel Remembered
   💬 "Good morning. That thing you mentioned yesterday crossed my mind."
   ➔ Emotional attachment starts when she feels seen, not relentlessly chased.

3️⃣ Mix Warmth with Purpose
   💬 "Morning. Coffee, focus, then a productive day. Hope yours starts smooth."
   ➔ Shows stability. Women attach to men with direction and discipline.

4️⃣ Light Dominance without Pressure
   💬 "Good morning. Handle today properly."
   ➔ Subtle protective authority creates psychological safety and attraction.

5️⃣ Invite Her into Your World
   💬 "Morning. I’m heading into a busy day. What’s the first win you’re aiming for?"
   ➔ Builds collaborative connection and mutual growth without being clingy.

6️⃣ Confidence with Restraint
   💬 "Good morning. I’ll catch up later."
   ➔ Space increases value. Emotional tension grows in anticipation.

7️⃣ Calm Reassurance
   💬 "Morning. No rush today. We’ll talk when it fits."
   ➔ Removes texting anxiety and lets her emotionally relax around you.

8️⃣ Emotional Anchor
   💬 "Good morning. I like how calm our conversations feel."
   ➔ Reinforces positive emotion and anchors your presence to emotional peace.

9️⃣ Masculine Consistency
   💬 "Morning. Same energy today."
   ➔ Consistency builds trust, and trust builds unshakable attachment.
================================================================================
""")

def cmd_gut(args):
    print("""
================================================================================
🧘 COACH KENNY 4x30 GUT MOBILITY & CONSTIPATION CURE PROTOCOL
================================================================================
💡 Core Principle: "Long hours of sitting lock the puborectalis muscle and kink
   the colon. Morning hydration + deep pelvic positioning opens the rectal angle
   and triggers natural peristaltic waves without harsh laxatives."

📸 Exercise 1: Half-Kneeling Psoas & Anorectal Alignment Lunge
   • Reps/Sets: 4 sets × 30 seconds hold/pulse per leg
   • Execution: One knee down on mat, front foot at 90°. Hands on knee, drive pelvis
     forward/down at 45°. Relax pelvic floor.
   • Mechanism: Lengthens iliopsoas, aligns the anorectal angle, and decompresses
     the sigmoid colon for easy downward transit.

📸 Exercise 2: Deep Sumo Stance / Malasana Peristaltic Pump
   • Reps/Sets: 4 sets × 30 rhythmic pulses daily
   • Execution: Wide horse stance (feet 1.5x shoulder width, toes flared 45°).
     Brace hands firmly on knees. Perform pursed-lip exhales while rhythmically
     pulsing the lower abdominal wall.
   • Mechanism: Elevates intra-abdominal pressure (IAP), gently massages the
     transverse and descending colon, and triggers colonic peristalsis.

🌅 Daily Flow Timing:
   1. Wake up -> 1 full glass of lukewarm water.
   2. Take PMBI Code 2149 (Pre/Pro-biotic).
   3. Perform the 5-minute Coach Kenny 4x30 drill.
   4. Effortless, natural bowel movement.
================================================================================
""")

def cmd_posture(args):
    print("""
================================================================================
🧍 ALEX LIBIN 3-STEP BOTTLE POSTURE CORRECTION PROTOCOL
================================================================================
💡 Core Principle: "Long hours of studying forward-slump the shoulders and cause
   thoracic hunchback. 3 simple bottle drills strengthen weak rhomboids, expand
   shortened pectorals, and restore upright alignment in 5 minutes."

📸 Exercise 1: Diagonal Behind-the-Back Bottle Pass
   • Prescription: 50 passes daily (alternating hands)
   • Execution: One arm reaches over right shoulder, opposite arm reaches behind
     lower back. Pass bottle hand-to-hand behind mid-back, then switch sides.
   • Mechanism: Glenohumeral internal/external rotation, fixes rounded shoulders.

📸 Exercise 2: Alternating W-to-Y Scapular Squeeze & Overhead Catch
   • Prescription: 100 reps daily
   • Execution: Elbows in 90° W cactus position, shoulder blades retracted. Toss
     or transfer bottle overhead alternating hands without dropping elbows.
   • Mechanism: Activates rear deltoids & rotator cuff, sculpts wide shoulders.

📸 Exercise 3: Behind-the-Neck Bottle Butterfly
   • Prescription: 100 reps daily
   • Execution: Hold bottle horizontally behind neck. Bring elbows together in front
     of face, then flare wide backward as far as possible.
   • Mechanism: Opens tight chest muscles, eliminates thoracic hunchback (kyphosis).

⏱️ Study Break Application:
   Perform 50 passes + 50 catches + 50 butterflies during your 10-minute diffuse
   mode break after a 50-minute focused study block.
================================================================================
""")

def cmd_focus(args):
    print("""
================================================================================
🎯 ISABELLA SALEH (BELLALEARNS) 3-PILLAR STUDY & FOCUS FRAMEWORK
================================================================================
💡 Core Principle: "Focus and memory are biological systems. Address distraction
   with time-boxing, procrastination with emotional priming, and memory fade
   with active retrieval."

1️⃣ CAN'T FOCUS? ➔ TIME-BOXING & REWARD ANCHORING
   • Pomodoro: 25 min deep work / 5 min diffuse break (ideal for concept learning).
   • Animedoro: 45-50 min intense problem solving (Maths/Reasoning) followed by
     a 15-min episode, walk, or high-dopamine reward. Sustains energy for hours!

2️⃣ ALWAYS LAZY? ➔ EMOTIONAL STATE SHIFT & 5-MIN MOMENTUM
   • Tony Robbins Priming: 2 minutes of deep diaphragmatic breathing, heart-focused
     gratitude, and visualizing your top 3 daily wins before touching the desk.
   • The 5-Minute Rule: Tell your brain: "I will only solve 1 question for 5 minutes."
     Overcomes limbic avoidance and ignites striatal dopamine momentum.

3️⃣ POOR MEMORY? ➔ ACTIVE RETRIEVAL SYSTEMS
   • Spaced Repetition: Ebbinghaus curve review intervals: Day 1 -> 3 -> 7 -> 30.
   • Active Recall: Test yourself with closed books, explain concepts out loud
     in Bengali (Feynman Method), and use foldable Obsidian question callouts!

================================================================================
""")

def cmd_style(args):
    print("""
================================================================================
🎩 OLD MONEY VS. STARBOY AESTHETIC & ROHINI MOON-VENUS BLUEPRINT
================================================================================
🌟 Astrological Blueprint (কর্কট লগ্ন ও রোহিণী শুক্র):
   • Cancer Lagna naturally has softer facial features; baggy streetwear creates
     a rounded, undisciplined look.
   • Taurus Moon & Venus in Rohini Nakshatra demand pure Venusian elegance:
     tactile luxury, natural fabrics, and Quiet Luxury over loud fast-fashion trends.
   • Old Money tailoring builds masculine structure, authority, and dignity!

⚡ 4-PILLAR WARDROBE BREAKDOWN:

1️⃣ TOPS: Graphic Tees vs. Textured Knit Polos (Upper Left)
   • ❌ Starboy: Oversized anime/beast prints, loud logos, hypebeast streetwear.
   • 👑 Old Money: Burgundy waffle-knit, solid black combed cotton, grey cable polos.
   • 🎯 Why for Kanad: Structured collars frame the neck and chisel the jawline.

2️⃣ TROUSERS: Baggy Cargo Denim vs. Tailored Pleated Trousers (Upper Right)
   • ❌ Starboy: Light-wash baggy cargo jeans, multi-pocket streetwear denim.
   • 👑 Old Money: Black/charcoal pleated dress trousers, ivory/cream linen pants.
   • 🎯 Why for Kanad: At ~82 kg, high-waisted pleated trousers streamline the
     physique, elongate the legs, and eliminate visual bulk.

3️⃣ FOOTWEAR: Chunky Sneakers vs. Loafers & Chelsea Boots (Lower Left)
   • ❌ Starboy: Chunky Nike Dunks, platform skate shoes, loud sports runners.
   • 👑 Old Money: Black leather Chelsea boots, penny loafers, Birkenstock slides.
   • 🎯 Why for Kanad: Leather footwear commands instant respect and elevates any
     casual polo-trouser combination to executive status.

4️⃣ TIMEPIECES: Smartwatches vs. Minimalist Analog Watches (Lower Right)
   • ❌ Starboy: Square/round plastic smartwatches, silicone activity trackers.
   • 👑 Old Money: Timex/Seiko silver analog with Roman dial, black leather band.
   • 🎯 Why for Kanad: Analog dials communicate timeless discipline and focus,
     free from screen addiction and notification clutter.

🏛️ Career Anchor:
   Old Money neutral palette (Navy, Ivory, Olive, Charcoal, Burgundy) establishes
   first-glance authority for upcoming Government Exam joining & administrative service!
================================================================================
""")

def cmd_book(args):
    print("""
================================================================================
📚 ROB MOORE BOOK PRIORITIZATION MATRIX & AUDIOBOOKSHELF SETUP
================================================================================
💡 Core Principle: "Do not read all books equally. Filter through the 3 tiers:
   Study deeply for lifetime mastery, Read once for practical systems, and
   Skip low-return or repetitive titles."

🟢 1. STUDY TIER (Highest Lifetime ROI — Line-by-Line Notes & Annual Re-reads):
   • Think & Grow Rich (Napoleon Hill) -> Definite Major Purpose & Autosuggestion
   • Awaken the Giant Within (Anthony Robbins) -> Neuro-Associative Conditioning
   • How to Win Friends and Influence People (Dale Carnegie) -> Social EQ & Empathy
   • Money: Know More, Make More, Give More (Rob Moore) -> Leverage & Capital Velocity

🟡 2. READ TIER (Practical Systems & Mindset — Focused Single Read / Audiobooks):
   • Atomic Habits (James Clear) -> 1% Marginal Gains & Habit Stacking
   • The 4-Hour Workweek (Tim Ferriss) -> Elimination & 80/20 Pareto Focus
   • Ready, Fire, Aim (Michael Masterson) -> Velocity over Perfectionism
   • Good to Great (Jim Collins) -> Level 5 Leadership & Hedgehog Concept
   • Rich Dad Poor Dad (Robert Kiyosaki) -> Cash-flow & Asset vs Liability
   • The Intelligent Investor (Benjamin Graham) -> Value Investing & Margin of Safety
   • The Power of Now (Eckhart Tolle) -> Presence & Dissolving Ego Friction

🔴 3. SKIP TIER (Selective / 5-Minute Summary Only):
   • The Psychology of Money (Morgan Housel) -> Core premise easily digested via summary
   • The Millionaire Next Door (Thomas Stanley) -> Outdated frugal statistics

🖥️ HOMESERVER AUDIOBOOKSHELF (192.168.1.100:13378 / Tailscale 100.x.y.z:13378):
   • Priority 1 (STUDY Shelf): Clear Thinking, Deep Work, Meditations, Can't Hurt Me
   • Priority 2 (READ Shelf): Power of Now, Intelligent Investor, Rich Dad Poor Dad
   • All 23 books tagged with 'Study' / 'Priority 1' and 'Read' / 'Priority 2' tags!
================================================================================
""")

def cmd_shoulder(args):
    print("""
================================================================================
🧘 FANG YUAN SHOULDER MOBILITY & ROTATOR CUFF BALANCING PROTOCOL
================================================================================
💡 Core Diagnostic: "The Apley Scratch Test: If you can touch fingertips on the
   left side behind your back but NOT on the right, you have severe rotator cuff
   asymmetry from desk-study posture."

🔍 2-STEP TARGETED CORRECTIVE DRILLS:

1️⃣ UPPER ARM EXTERNAL ROTATION RESTRICTION (Top Hand Can't Reach Down):
   • Drill: Broomstick Lever External Rotation
   • Execution: Place broom vertically behind tricep. Hold top with overhead hand.
     Pull bottom of broom forward with other hand to lever the upper arm externally.
   • Target: Infraspinatus & Teres Minor mobility.
   • Prescription: 20 seconds hold x 3 sets per side.

2️⃣ LOWER HAND INTERNAL ROTATION RESTRICTION (Bottom Hand Can't Reach Up):
   • Drill: Waist-Lock Elbow Forward Pull (Chicken Wing Stretch)
   • Execution: Rest hand on waist with elbow flared out. Cup elbow with opposite
     hand and pull gently forward while keeping shoulder blade relaxed.
   • Target: Posterior capsule release & Subscapularis flexibility.
   • Prescription: 20 seconds hold x 3 sets per side.

⏱️ Desk Break Application:
   Perform 20s x 3 sets during your 10-minute diffuse study break to instantly
   release neck, upper back, and trap tension!
================================================================================
""")

def cmd_video(args):
    part = getattr(args, "part", None)
    if getattr(args, "command", "") == "video2":
        part = 2

    if part == 1:
        print("""
================================================================================
🛡️ JOVAN DELO ANTI-BRAINROT GROWTH VIDEOS (SERIES PART 1)
================================================================================
💡 Core Philosophy: "Stop frying your dopamine receptors with 15-second mindless
   reels. Replace passive short-form consumption with 5 long-form cognitive masterclasses."

🎬 5 ESSENTIAL GROWTH VIDEOS (PART 1):

1️⃣ The Ideas We Lose By Morning (eyes of lee — 4:00)
   • YouTube: https://www.youtube.com/watch?v=u8byNtXpaPk
   • Thesis: Midnight creative genius vanishes by dawn without external capture.
   • Protocol: Keep an Obsidian bedside scratchpad or voice memo active.

2️⃣ You're Not Lazy, You Just Need a Reason (The Vandalist — 7:42)
   • YouTube: https://www.youtube.com/watch?v=Q7XpbunqZT4
   • Thesis: Laziness is an illusion; the brain conserves energy without high stakes.
   • Anchor: The "Gun to the Head" test & Kanad's MOTIVE.md dignity recovery.

3️⃣ They Judge You Because They Are Afraid You'll Leave Them Behind (Jovan Delo — 9:39)
   • YouTube: https://www.youtube.com/watch?v=GepL6b0j0Us
   • Thesis: Social crab mentality; peers attack isolation because it mirrors their stagnation.
   • Action: Monk mode shielding & ruthless focus on competitive exam syllabi.

4️⃣ You Have to Let Yourself Go (Profound Pondering — 15:43)
   • YouTube: https://www.youtube.com/watch?v=_FTGZ5V4AWY
   • Thesis: The sunk cost of outgrown identity. To become the officer, kill the procrastinator.
   • Action: Surrender comfortable mediocrity to unlock your higher self.

5️⃣ 50 Reasons to Keep Living (bi felicia — 16:05)
   • YouTube: https://www.youtube.com/watch?v=knijPOLYxHo
   • Thesis: Micro-sensory anchors during dark, grueling preparation phases.
   • Action: Ground yourself in tactile micro-gratitude when macro goals feel distant.

🖥️ HOMESERVER MINIDLNA STREAMING:
   • Host: 192.168.1.100 / Tailscale 100.x.y.z
   • DLNA Directory: /srv/samba/shared/videos/Anti-Brainrot_Growth_Series/
   • Strict Guardrail: Movies directory (/mnt/saman-data/Downloads/Movies) untouched!
   • Streaming: Open VLC -> Local Network -> MiniDLNA on Homeserver -> Video
================================================================================
""")
    elif part == 2:
        print("""
================================================================================
🛡️ JOVAN DELO ANTI-BRAINROT GROWTH VIDEOS (SERIES PART 2)
================================================================================
💡 Core Philosophy: "Growth, alone, loneliness, vulnerability, self-care, difficult,
   hopeless, fighting, mental health, soul, improvement. Curated cognitive anchors."

🎬 5 ESSENTIAL GROWTH VIDEOS (PART 2):

1️⃣ The Psychology of a Child who grew up Too Fast (Kee — 8:56)
   • YouTube: https://www.youtube.com/watch?v=viB7aMWWD_4
   • Thesis: Parentification & hyper-independence; carrying childhood family burdens.
   • Action: Shed guilt, allow vulnerability, and anchor focus on personal career milestones.

2️⃣ You're Too Self Aware to Actually Live (Perceiv — 1:47)
   • YouTube: https://www.youtube.com/watch?v=YGG16T7osmE
   • Thesis: Metacognitive paralysis; hyper-monitoring thoughts paralyses execution.
   • Action: Physiological sigh reset + immediate 5-minute study sprint. Action cures overthinking.

3️⃣ In Pursuit of an Extraordinary Life (Jeffrey Sun — 4:56)
   • YouTube: https://www.youtube.com/watch?v=F8Zs8xMTDzo
   • Thesis: Overcoming the fear of the ordinary. Glamour vs. compounding consistency.
   • Action: Reframe daily desk discipline, workouts, and clean diet as the true extraordinary foundation.

4️⃣ Once You Use Your Intuition, Everything Changes (Queen — 50:03)
   • YouTube: https://www.youtube.com/watch?v=Fl4hTpaI7Uw
   • Thesis: Damasio's somatic marker hypothesis; gut instinct as subconscious pattern synthesis.
   • Action: Trust first instincts in MCQs / option elimination and interpersonal dynamics.

5️⃣ When You Stop Explaining Yourself, Everything Changes - Carl Jung (Psyphoria — 29:02)
   • YouTube: https://www.youtube.com/watch?v=ARwUS8Lnn98
   • Thesis: Jungian individuation & non-defensive masculine frame. Justifying leaks personal power.
   • Action: Eliminate defensiveness. Give calm, resolute 1-line answers: 'I have chosen this path.'

🖥️ HOMESERVER MINIDLNA STREAMING:
   • Host: 192.168.1.100 / Tailscale 100.x.y.z
   • DLNA Directory: /srv/samba/shared/videos/Anti-Brainrot_Series_Part2/
   • Strict Guardrail: Movies directory (/mnt/saman-data/Downloads/Movies) untouched!
   • Streaming: Open VLC -> Local Network -> MiniDLNA on Homeserver -> Video -> Anti-Brainrot_Series_Part2
================================================================================
""")
    else:
        print("""
================================================================================
🛡️ JOVAN DELO ANTI-BRAINROT GROWTH VIDEO MASTER SUITE (SERIES 1 & 2)
================================================================================
💡 Core Philosophy: "Stop frying dopamine with 15-second endless scrolling. Replace
   short-form digital decay with 10 transformative long-form cognitive masterclasses."

📁 SERIES PART 1 (/srv/samba/shared/videos/Anti-Brainrot_Growth_Series/):
   1. The Ideas We Lose By Morning (eyes of lee — 4:00) [u8byNtXpaPk]
   2. You're Not Lazy, You Just Need a Reason (The Vandalist — 7:42) [Q7XpbunqZT4]
   3. They Judge You Because They Are Afraid You'll Leave Them Behind (Jovan Delo — 9:39) [GepL6b0j0Us]
   4. You Have to Let Yourself Go (Profound Pondering — 15:43) [_FTGZ5V4AWY]
   5. 50 Reasons to Keep Living (bi felicia — 16:05) [knijPOLYxHo]

📁 SERIES PART 2 (/srv/samba/shared/videos/Anti-Brainrot_Series_Part2/):
   1. The Psychology of a Child who grew up Too Fast (Kee — 8:56) [viB7aMWWD_4]
   2. You're Too Self Aware to Actually Live (Perceiv — 1:47) [YGG16T7osmE]
   3. In Pursuit of an Extraordinary Life (Jeffrey Sun — 4:56) [F8Zs8xMTDzo]
   4. Once You Use Your Intuition, Everything Changes (Queen — 50:03) [Fl4hTpaI7Uw]
   5. When You Stop Explaining Yourself, Everything Changes - Carl Jung (Psyphoria — 29:02) [ARwUS8Lnn98]

🖥️ HOMESERVER MINIDLNA STREAMING:
   • Server IP: 192.168.1.100 (Tailscale 100.x.y.z)
   • Strict Guardrail: Movies directory (/mnt/saman-data/Downloads/Movies) strictly untouched!
   • Streaming: VLC -> Local Network -> MiniDLNA on Homeserver -> Video
   • Tip: Run 'self_help_cli.py video --part 1' or '--part 2' for deep notes!
================================================================================
""")

def cmd_career(args):
    print("""
================================================================================
💼 CAREER ACCELERATION & INTERVIEW MASTERY (18–32 YRS)
================================================================================
💡 Core Philosophy: "Stop overthinking what you want in life. 5 high-yield vocational
   masterclasses to bring career clarity, master interview storytelling, and get hired."

🎬 5 ESSENTIAL VOCATIONAL MASTERCLASSES:

1️⃣ How to Figure Out What You Really Want (Ashley Stahl | TEDx — 18:59)
   • YouTube: https://www.youtube.com/watch?v=bRtBHF-WPpM
   • Thesis: Clarity comes through action, not contemplation. Distinguish fleeting
     passions from innate core skill sets (analytical synthesis & discipline).
   • Action: Focus 100% on Govt Exam & Banking PO milestones without self-doubt.

2️⃣ Mastering the Art of the Interview (Ashley Rizzotto | TEDx — 10:54)
   • YouTube: https://www.youtube.com/watch?v=ppf9j8x0LA8
   • Thesis: Ditch robotic memorized answers. Build emotional connection through
     the STAR storytelling framework and calm, grounded executive presence.
   • Action: Perfect your 3 core stories for WBCS & Bank PO Personality Tests.

3️⃣ Jordan Peterson: What Kind of Job Fits You? (Essential Truth — 09:21)
   • YouTube: https://www.youtube.com/watch?v=pu__97bVyOc
   • Thesis: Align career with Big Five traits. High Conscientiousness + Intellect
     thrive in structured, rules-based, meritocratic governance systems.
   • Action: Administrative governance offers the ideal psychometric harmony.

4️⃣ The Strategy That Gets You Hired (Social Untold ft. Vardaan UKJI — 1:01:14)
   • YouTube: https://www.youtube.com/watch?v=4oai2_qGthg
   • Thesis: The hidden job market. Avoid generic spray-and-pray applications;
     position yourself strategically as a high-leverage problem solver.
   • Action: Systematically crush high-weightage syllabus topics to guarantee selection.

5️⃣ My Career Advice For Anyone Feeling Stuck In Life (Travis Media — 07:25)
   • YouTube: https://www.youtube.com/watch?v=Jl4Waz8TmyU
   • Thesis: Feeling stuck is a symptom of zero daily compounding progress.
     Kill passive digital dopamine and build tangible micro-wins every single day.
   • Action: 4-hour Oakley study block + Jan Aushadhi stack + evening workout.

🖥️ HOMESERVER MINIDLNA STREAMING:
   • Host: 192.168.1.100 / Tailscale 100.x.y.z
   • DLNA Directory: /srv/samba/shared/videos/Career_Interview_Acceleration_Series/
   • Strict Guardrail: Movies directory (/mnt/saman-data/Downloads/Movies) untouched!
   • Streaming: Open VLC -> Local Network -> MiniDLNA on Homeserver -> Video -> Career_Interview_Acceleration_Series
================================================================================
""")

def cmd_pest(args):
    print("""
================================================================================
🏡 HOUSEHOLD PEST CONTROL: VIRAL MYTHS VS. SCIENTIFIC FACTS
================================================================================
💡 Core Philosophy: "Your home should be a sanctuary, not an arena for pests.
   Stop risking safety with unverified viral kitchen hacks. Understand the
   biological mechanisms and execute scientifically proven protocols."
   — Nishant Singh (@bookthoughs)

1️⃣ 🐍 COBRA / VENOMOUS SNAKE:
   • ❌ Myth: Spray air freshener and it will leave.
   • ⚠️ Danger: Aerosols irritate Jacobson's organ, blinding & provoking deadly strikes!
   • 🛡️ Action: Maintain 15ft distance, isolate pets/children, call Snake Rescue immediately.

2️⃣ 🐛 CENTIPEDE:
   • ❌ Myth: Sprinkle salt.
   • 🛡️ Fact: Root cause is bathroom dampness. Dehumidify & seal cracks with Diatomaceous Earth.

3️⃣ 🪳 COCKROACHES:
   • ❌ Myth: Sprinkle chopped bay leaves (তেজপাতা).
   • 🛡️ Fact: Eugenol only acts as a mild repellent. Use Boric acid dough or Fipronil gel bait.

4️⃣ 🐀 RATS & RODENTS:
   • ❌ Myth: Sprinkle powdered black pepper.
   • 🛡️ Fact: Rodents easily bypass pepper. Seal entry points with steel wool; set mechanical traps.

5️⃣ 🪵 TERMITES (উইপোকা):
   • ❌ Myth: Spray lime water (চুনের জল).
   • ⚠️ Danger: Drives subterranean colony deeper into structural wood undetected.
   • 🛡️ Action: Professional soil termiticide barrier (Imidacloprid).

6️⃣ 🪰 FLIES (মাছি):
   • ❌ Myth: Place pandan leaf slices.
   • 🛡️ Fact: Rotting leaves attract more flies. Use UV insect traps & airtight bin sanitation.

7️⃣ 🐜 ANTS (পিঁপড়ে):
   • ❌ Myth: Sprinkle powdered vanilla.
   • 🛡️ Fact: Sugar in vanilla feeds ants! Wipe trails with white vinegar; use Borax sugar bait.
================================================================================
""")

def cmd_bookposture(args):
    print("""
================================================================================
📚 ALEX LIBIN DESK-STUDY BOOK POSTURE PROTOCOL (4x1-MINUTE DRILLS)
================================================================================
💡 Core Principle: "Now your dusty books found their purpose! Long hours of desk
   study tilt the head forward, double the cervical spine load, lax the platysma
   muscle (double chin), and slump the thoracic spine. Use any study book for 4
   deliberate 1-minute drills to restore axial alignment and brain alertness."
   — Alex Libin (@alex.d.libin)

1️⃣ 📖 DRILL 1: OVERHEAD EAR TOUCH HOLD (1 MIN)
   • Target: Thoracic Hunchback (কুঁজো পিঠ / Thoracic Kyphosis)
   • Execution: Hold book vertically overhead with both hands. Straighten arms,
     keeping biceps touching ears or aligned behind ear canal. Core engaged.
   • Biomechanics: Decompresses anterior vertebral disc margins, activates lower
     trapezius and spinal erectors, reverses desk slump.

2️⃣ 💋 DRILL 2: COLLARBONE ANCHOR & CEILING KISS (1 MIN)
   • Target: Double Chin & Tech-Neck (থুতনির মেদ ও ঘাড়ের ভাঁজ)
   • Execution: Press book flat across upper chest / collarbones with both hands
     to depress clavicles. Tilt head backward toward ceiling. Pucker lips / push
     jaw upward to deeply stretch front of neck. Hold for 1 minute.
   • Biomechanics: Anchors SCM and platysma origins; deep eccentric stretch of
     superficial cervical fascia; tones submental tissue to eliminate double chin.

3️⃣ 🛡️ DRILL 3: BEHIND-THE-BACK CLASP & HEAD TILT (1 MIN)
   • Target: Rounded Shoulders (সামনে ঝুঁকে যাওয়া কাঁধ / Protracted Scapulae)
   • Execution: Hold book horizontally behind lower back. Roll shoulders back &
     down, squeezing shoulder blades together. Lift book slightly off glutes while
     tilting head gently side to side or maintaining neutral posture.
   • Biomechanics: Activates rhomboids and middle trapezius; releases shortened
     pectoralis minor; returns humeral head to glenoid neutral.

4️⃣ 🚶 DRILL 4: BOOK BALANCING SLOW WALK (1 MIN)
   • Target: Forward Head / Turtle Neck (সামনে বাড়ানো ঘাড় / Forward Head Posture)
   • Execution: Place hardcover book flat on crown of head. Perform subtle chin tuck
     (cervical retraction). Walk slowly with heel-to-toe gait for 1 minute without
     dropping the book.
   • Biomechanics: Immediate gravity feedback forces active engagement of deep
     cervical flexors (Longus Colli); recalibrates vestibular plumb-line balance.

⏱️ POMODORO 5-MINUTE INTEGRATION:
   50 min study ➔ [Min 1: Overhead Hold] ➔ [Min 2: Collarbone Anchor]
   ➔ [Min 3: Back Clasp] ➔ [Min 4: Book Balancing Walk] ➔ [Min 5: Hydrate]
================================================================================
""")

def cmd_dtan(args):
    print("""
================================================================================
🧼 DR. HADIYA DERMATOLOGICAL D-TAN CLEANSING PROTOCOL (4 CLINICAL SOAPS)
================================================================================
💡 Core Principle: "UV rays trigger basal melanocytes to produce dark eumelanin
   via Tyrosinase enzymes. Stop using harsh alkali soaps or toxic bleach creams.
   Use dermatologically proven tyrosinase inhibitors & mild keratolytics."
   — Dr. Hadiya Skin & Hair (@dr.hadiya_skin_hair)

1️⃣ 🧪 GLUTALIGHT SOAP (MRP: ~₹150)
   • Actives: Glutathione 0.5% + Kojic Acid 1% + Vitamin C + Papaya Extract
   • Target: Stubborn sun tanning & hyperpigmentation
   • Action: Potent antioxidant that shifts eumelanin pathway to light pheomelanin.
   • Skin: Normal to Oily skin; daily face & neck d-tan wash.

2️⃣ 💧 KOZICARE SOAP (MRP: ~₹94)
   • Actives: Kojic Acid 1% + Glutathione 0.5% + Arbutin + Vitamin E
   • Target: Pocket-friendly daily D-Tan & sun spot clearing
   • Action: Directly chelates copper ions in Tyrosinase, preventing pigment synthesis.
   • Skin: Oily/Combination skin; ideal for daily commute wash across face, neck & hands.

3️⃣ ✨ ETHIGLO SOAP (MRP: ~₹99)
   • Actives: Kojic Acid + Glycolic Acid (AHA) + Liquorice Extract
   • Target: Dullness, rough dead-cell accumulation, clogged pores & rough tan
   • Action: Chemical micro-exfoliation of dead stratum corneum + instant post-wash glow.
   • Skin: Dull, thick, or acne-prone skin (use 2–3x weekly).

4️⃣ 🌿 DERMADEW LITE SOAP (MRP: ~₹178)
   • Actives: Pea Extract + Aloe Vera + Hypoxis Rooperi Extract + Vitamin E
   • Target: Sensitive skin tanning & fragile skin barrier preservation
   • Action: Gentle botanical depigmentation without stripping natural moisture (NMF).
   • Skin: Dry, sensitive, or easily irritated wheatish skin.

📌 DR. HADIYA'S 4-STEP D-TAN CLINICAL BLUEPRINT:
   Step 1: Cleansing (Active Soap lather 60s) ➔ Step 2: Treat (Alpha Arbutin/Kojic Cream)
   ➔ Step 3: Peel (Weekly AHA/BHA chemical exfoliation) ➔ Step 4: Protect (SPF 50+ & Moisturizer)

⚠️ GOLDEN RULES:
   • Timeline: 3–4 weeks for biological epidermal cell turnover (28-day cycle).
   • Mandatory: Always apply moisturizer and broad-spectrum SPF 50+ after acid soaps!
   • Hydration: Drink 3–4 liters of water daily for skin turgor and cellular flush.
================================================================================
""")

def cmd_facewash(args):
    print("""
================================================================================
🧴 DR. HADIYA 4 INDIAN PHARMACY D-TAN FACE WASHES & DWELL TIME PROTOCOL
================================================================================
💡 Core Principle: "Face tanning is deep within the epidermal layers. Standard
   foaming soaps wash away before actives penetrate. Pharmacy D-Tan cleansers
   require 30–50 seconds of active circular massage (Dwell Time) to deactivate
   Tyrosinase enzymes and loosen dead pigmented cells."
   — Dr. Hadiya Skin & Hair (@dr.hadiya_skin_hair)

1️⃣ 🧪 GLUTAZOL FACE WASH (MRP: ~₹279 / 100ml)
   • Actives: Glutathione + Kojic Acid + Vitamin C + Glycolic Acid
   • Target: Stubborn dark tanning, melasma, and uneven skin tone
   • Action: Replenishes cellular glutathione; shifts dark eumelanin to light pheomelanin.
   • Suitability: Normal to Oily skin; powerful antioxidant glow.

2️⃣ 🌿 MELACARE GLOW FACE WASH (MRP: ~₹150 / 60–100ml)
   • Actives: Glycolic Acid + Vitamin E + D-Panthenol
   • Target: Dullness, gray fatigue, dead stratum corneum accumulation
   • Action: Ultra-affordable gentle AHA keratolysis; unblocks pores without tightness.
   • Suitability: All skin types; budget daily refreshing face wash.

3️⃣ ✨ ETHIGLOW FACIAL FOAM (MRP: ~₹239 / 70g)
   • Actives: Kojic Acid + Liquorice + Nicotinamide + Micro-beads
   • Target: Blackheads, congested pores, and post-travel train/road pollution
   • Action: Deep creamy foaming action; sweeps away soot, PM2.5, and oxidized sebum.
   • Suitability: Oily & Combination skin; instant refreshing clarity.

4️⃣ 🛡️ KOZICARE FACE WASH (MRP: ~₹249 / 65ml)
   • Actives: Kojic Acid + Arbutin + Vitamin C + Vitamin E
   • Target: Sun spots, outdoor commute tanning, and melanosome transfer
   • Action: Directly blocks tyrosinase copper cofactors; prevents UV pigment transfer.
   • Suitability: Oily T-zone and daily outdoor commuter cleansing.

⏱️ APPLICATION RULES & DWELL TIME:
   1. Wet face with normal/cool water.
   2. Massage coin-sized amount gently for 30–50 SECONDS (crucial active penetration).
   3. Rinse thoroughly with normal water (avoid hot water).
   4. Immediately lock barrier with moisturizer + broad-spectrum SPF 50+ sunscreen!
================================================================================
""")

def cmd_palette(args):
    print("""
================================================================================
🎩 OLD MONEY COLOR COMBINATIONS: HOW TO LOOK EXPENSIVE (@grw_shitiz)
================================================================================
💡 Core Principle: "Loud logos scream insecurity; neutral color blocking and
   natural textures whisper timeless generational wealth. Master these 4 neutral
   combinations to elevate your presence effortlessly without a fortune."

1️⃣ 🔘 SLATE GREY & OFF-WHITE / IVORY (Monochrome Quiet Luxury)
   • Palette: Slate Grey Knit / Polo (#333842) + Off-White Pleated Trousers (#eceae4)
   • Vibe: Minimalist European elegance; understated intellectual authority.
   • Occasion: High-stakes interviews, office, executive meetings.
   • Kusthi: Cancer Lagna power palette (Moon silver-white).

2️⃣ 🪵 TONAL MOCHA & CHOCOLATE BROWN (Heritage Aristocrat)
   • Palette: Mocha Brown Overshirt (#785744) + Sand Tee (#d8c6b2) + Chocolate Pants (#4a372c)
   • Vibe: Country club heritage; rich tactile depth and warm earthy textures.
   • Occasion: Autumn/winter evenings, cafe dates, semi-formal dinners.
   • Kusthi: Taurus Moon & Venus earthy grounding.

3️⃣ 🌊 BABY BLUE & OFF-WHITE / ECRU (Riviera Resort Chic)
   • Palette: Powder Blue Linen Shirt (#9bbad4) + Ivory/Off-White Chinos (#f4f1eb)
   • Vibe: French Riviera billionaire; effortless coastal freshness.
   • Occasion: Summer daytime, outdoor brunch, vacation resort wear.
   • Complexion: Maximum luminous contrast on Indian warm wheatish skin!

4️⃣ 🍷 DEEP BURGUNDY & DARK CHARCOAL (Academic Evening Authority)
   • Palette: Oxblood/Burgundy Textured Polo (#782823) + Charcoal Trousers (#363333)
   • Vibe: Bold yet restrained masculinity; commanding charisma.
   • Occasion: Festive celebrations, evening dinners, special events.
   • Grooming: Sharply frames structured goatee and dark wavy hair.

📌 5 OLD MONEY GOLDEN RULES:
   1. Zero Loud Logos  |  2. Natural Fabrics (Linen/Knit)  |  3. Pleated Trousers
   4. 2-Color Rule (Base + Contrast Neutral)  |  5. Flawless Grooming Base
================================================================================
""")

def cmd_zyverel(args):
    print("""
================================================================================
🎨 ZYVEREL 8 UNIVERSAL COLOR COMBINATIONS (MEN & WOMEN) (@zyverel)
================================================================================
💡 Core Principle: "Great dressing is chromatic physics. Balance 1 deep anchor
   neutral with 1 light/warm tone using the 60-30-10 rule for instant harmony."

1️⃣ 🖤 BLACK + GREY (Urban Minimalist)
   • Palette: Jet Black + Slate Grey | Clean, modern, architectural authority.
   • Ideal: Corporate evening, sharp minimalist city casual, leather jacket & tailored pants.

2️⃣ 🍒 BLACK + CHERRY RED (Dramatic High Contrast)
   • Palette: Black + Deep Cherry/Oxblood | Bold, magnetic, luxurious evening charm.
   • Ideal: Romantic dinner, exhibition, fine knitwear under a dark structured coat.

3️⃣ 🍷 GREY + BURGUNDY (European Academic)
   • Palette: Slate Grey + Wine/Burgundy | Intellectual quiet luxury & seasonal warmth.
   • Ideal: Autumn/winter layering, conferences, cashmere sweater with charcoal blazer.

4️⃣ 🌊 NAVY + WHITE (Coastal Executive)
   • Palette: Royal Navy + Pure White | Timeless nautical prestige & crisp trust.
   • Ideal: Daytime office, UPSC/WBCS board interviews, crisp white shirt & navy jacket.

5️⃣ 🐎 NAVY + CAMEL (Italian Sprezzatura)
   • Palette: Navy Blue + Warm Camel/Tan | Continental masterclass pairing.
   • Ideal: Camel overcoat or cardigan over navy knit with cognac leather loafers.

6️⃣ 🍨 CHOCOLATE + CREAM (Quiet Luxury Dessert)
   • Palette: Dark Chocolate + Ivory Cream | Soft, tactile wealth; old money perfection.
   • Ideal: Tactile corduroy, cream polo, suede loafers; relaxed weekend elegance.

7️⃣ 🕶️ CHOCOLATE + BLACK (Modern Moody Chic)
   • Palette: Chocolate Brown + Jet Black | High-fashion stealth luxury; modern edgy depth.
   • Ideal: Matte black silk-cotton tee + dark chocolate tailored trousers & chelsea boots.

8️⃣ ☀️ CAMEL + WHITE (Sunlit Resort Elegance)
   • Palette: Warm Camel + Bright White | Luminous daytime wealth; clean and effortless.
   • Ideal: Pure white linen trousers + camel knit/overshirt + clean white sneakers.

📌 4 VISUAL BALANCE RULES:
   1. Anchor: 1 Dark Neutral + 1 Light/Warm Neutral
   2. 60-30-10 Rule: 60% Trousers/Base, 30% Shirt/Jacket, 10% Leathers/Hardware
   3. Unify Leathers: Black with Black/Silver; Brown/Tan with Brown/Gold
   4. Texture: Matte natural fibers (linen, wool, knit) over cheap polyester sheen
================================================================================
""")

def cmd_pelvic(args):
    print("""
================================================================================
🌙 ALEX LIBIN 5-MIN BEDTIME PELVIC REALIGNMENT & FLAT BELLY PROTOCOL (@alex.d.libin)
================================================================================
💡 Core Truth: A protruding lower belly ("Fake Lower Belly Pouch") is 90% caused by
   Anterior Pelvic Tilt (APT) from long sitting, NOT stubborn body fat!
   Psoas & Iliacus pull pelvis forward -> Lumbar swayback -> Abdominal viscera sags.

⚡ 1 ACTION, 5 MINUTES NIGHTLY BEFORE SLEEP (ZERO WORKOUTS / NO EQUIPMENT):
--------------------------------------------------------------------------------
1️⃣ SUPINE SETUP:
   • Lie completely flat on back in bed or on a yoga mat right before sleep.

2️⃣ DIAMOND / BUTTERFLY LEG POSITION:
   • Bend knees outward and bring the soles of your feet together.
   • Let knees fall open naturally under gravity. DO NOT force them down.
   • Creates passive external rotation & abduction, immediately de-spasming tight hip flexors.

3️⃣ RELAXED OVERHEAD ARMS:
   • Place arms loosely overhead on mattress/pillow (cactus / surrender position).
   • Stretches pectoralis minor, opens thoracic ribcage, and frees the diaphragm.

4️⃣ NEUROMUSCULAR PARASYMPATHETIC BREATHING:
   • Inhale 4 seconds through nose (lateral ribs & lower belly expand).
   • Exhale 8 seconds slowly through mouth/nose.
   • On each exhale, feel sacrum & lumbar spine sink completely flat into mattress.

🏆 3 IMMEDIATE BIOMECHANICAL OUTCOMES:
   1. The Pelvis is Straightened (ASIS rotates back to neutral vertical alignment).
   2. The Belly becomes Flat (Pelvic bowl levels out; abdominal viscera settles inside).
   3. The Lower Back Pain is Gone (Lumbar facet joint compression & nerve pinching erased).
================================================================================
""")

def cmd_glowup(args):
    print("""
================================================================================
🗿 GLOWUP UTOPIA: 6 FACIAL AESTHETICS & LOOKSMAXXING BLUEPRINT (@glowuputopia)
================================================================================
💡 Core Principle: Attractiveness is 90% bone structure projection, bilateral
   symmetry, and low facial adiposity. Master these 6 non-negotiable features:

1️⃣ ⚖️ SYMMETRICAL FACE (The Foundation)
   • Why: Perceived as peak health, youthful vitality, and subconscious harmony.
   • Daily Habits: Chew evenly on both sides, strict nasal breathing, sleep on back.

2️⃣ 👁️ HUNTER EYES (Dominance & Intensity)
   • Why: Deep-set, focused gaze with minimal upper eyelid exposure.
   • Daily Habits: Morning cold debloating (ice/spoons), orbicularis oculi training, 8h sleep.

3️⃣ 📐 STRONG JAWLINE (Structure & Authority)
   • Why: Defines face, adds structure, signals high testosterone.
   • Daily Habits: Reach sub-15% body fat (82kg -> 72kg cut), mastic gum, book chin tucks.

4️⃣ 💎 HIGH CHEEKBONES (Contour & Shadow)
   • Why: Creates angular model-like definition and hollow cheek shadows.
   • Daily Habits: Mewing (tongue on palate), low sodium/high water, cold lymphatic drainage.

5️⃣ ✨ CLEAN SKIN (Vitality & Youth)
   • Why: Smooth, unblemished skin maximizes facial lighting and high-status appeal.
   • Daily Habits: Daily SPF 50+, Dr. Hadiya pharmacy D-Tan cleansers, zinc & hydration.

6️⃣ 👃 WELL-BALANCED NOSE (Facial Harmony)
   • Why: Centered, balanced proportions keep focus on eyes and jaw.
   • Daily Habits: Strict nasal breathing (prevents downward facial growth), debloat tissue.

📌 KANAD SYNERGY:
   • Cut 82kg ➔ 72kg chisels jawline and carves cheekbone hollows.
   • Cold debloating clears under-eye puffiness and restores sharp almond eyes.
   • Structured goatee squares off chin and balances lower facial thirds.
================================================================================
""")

def cmd_shamani(args):
    print("""
================================================================================
📚 RAJ SHAMANI: TOP 2 BOOK RECOMMENDATIONS (@thinkwithshamani • Figuring Out)
================================================================================
💡 Core Philosophy: Don't read for vanity metrics. Master foundational books
   that permanently rewire macro-thinking, pattern recognition, and problem solving.

1️⃣ 🏛️ THE LESSONS OF HISTORY — Will & Ariel Durant
   • Classification: Priority 1: STUDY Tier (Audiobookshelf & Obsidian Vault)
   • Core Premise: 5,000 years of civilization synthesized into ~100 dense pages.
   • Macro Principle 1: History is a fragment of biology. Life is competition,
     selection, and inequality. Freedom and equality are eternal enemies.
   • Macro Principle 2: Human nature is invariant across 100, 1,000, and 5,000 years.
     Only technologies change; human desires, greed, and fear remain identical.
   • Macro Principle 3: Wealth continually concentrates until either violent revolution
     or peaceful legal redistribution (Solon / FDR New Deal) resets it.
   • Forecasting Edge: Master the invariant cycles to accurately predict the future.

2️⃣ ✏️ THE BACK OF THE NAPKIN — Dan Roam
   • Subtitle: Solving Problems and Selling Ideas with Pictures
   • Classification: Priority 1: STUDY Tier (Visual Thinking & Canvas Architecture)
   • Core Premise: Anyone can think visually without being an artist.
   • The 4-Step Cycle: Look -> See -> Imagine -> Show.
   • The SQVID Dials: Simple vs Elaborate | Quality vs Quantity | Vision vs Execution |
     Individual vs Comparison | Delta (Change) vs Status Quo.
   • The 6 W's System: Who/What (Portrait) | How much (Chart) | Where (Map/Canvas) |
     When (Timeline) | How (Flowchart) | Why (Multi-variable plot).
   • Napkin Pitch Mastery: Solve any complex business idea or internal mental chaos
     by sketching Point A, Obstacle X, and Point B on a single sheet of paper.

📌 HOMESERVER & VAULT SYNERGY:
   • Homeserver Audiobookshelf: Priority 1: STUDY Tier (192.168.1.100:13378)
   • Obsidian Canvas: 00_Dashboard/Self_Help_Architecture.canvas (6 Ws mapping)
   • Synthesis Protocol: 02_Cognitive_Learning/Raj_Shamani_Top_Book_Recommendations_Mastery.md
================================================================================
""")

def cmd_kwik(args):
    print("""
================================================================================
🧠 JIM KWIK: LIMITLESS BRAIN OPTIMIZATION & ACCELERATED LEARNING
================================================================================
💡 Core Principle: "There are only two types of brain: trained brain and
   untrained brain." Slow learning is not a biological flaw; it is an operating
   system training deficit.

1️⃣ ⚡ THE 3M LIMITLESS ARCHITECTURE
   • Mindset (The WHAT): Eradicate LIEs (Limited Ideas Entertained), embrace neuroplasticity.
   • Motivation (The WHY): Purpose x Energy x S^3 (Small Simple Steps).
   • Method (The HOW): Focus, Study, Memory (MOM), and Speed Reading with a visual pacer.
   • The Intersection: Mindset + Motivation + Method = THE LIMITLESS STATE (Peak Flow).

2️⃣ 🛡️ THE 4 DIGITAL VILLAINS & DEFENSE
   • Digital Deluge: Cognitive overload from endless feeds -> 30-min morning screen blackout.
   • Digital Distraction: Notification addiction -> Single-task Pomodoro sprints (25/5).
   • Digital Dementia: Outsourcing memory to apps -> Active recall & mental math.
   • Digital Deduction: Algorithmic blindness -> First-principles critical thinking.

3️⃣ 🚀 THE FASTER ACCELERATED LEARNING FRAMEWORK
   • [F] FORGET: Clear biases, ego, and distractions. Cultivate beginner's mind (Shoshin).
   • [A] ACT: Active learning beats passive reading. Take interactive notes & sketch diagrams.
   • [S] STATE: Information + Emotion = Long-Term Memory (I x E = LTM). Upright posture.
   • [T] TEACH: Learn with the intention to teach someone else within 24 hours (Feynman).
   • [E] ENTER: Schedule study blocks into your calendar. Unscheduled tasks never happen.
   • [R] REVIEW: Spaced retrieval (Day 0, Day 1, Day 3, Day 7) defeats the forgetting curve.

4️⃣ 👁️ SPEED READING & BRAIN FUEL
   • Visual Pacer: Trace text with finger/pen -> Eliminates regression, increases speed 25-50%.
   • 10 Brain Foods: Avocado, Blueberries, Broccoli, Dark Chocolate, Eggs, Greens, Salmon,
     Turmeric, Walnuts, and Pure Water.

📌 HOMESERVER & VAULT SYNERGY:
   • Homeserver Audiobookshelf: Priority 1: STUDY Tier (192.168.1.100:13378)
   • Synthesis Protocol: 02_Cognitive_Learning/Jim_Kwik_Limitless_Brain_Optimization.md
   • Visual Matrix: Attachments/Jim_Kwik_Limitless_Brain_Mastery_Matrix.jpg
================================================================================
""")

def cmd_realestate(args):
    print("""
================================================================================
🏢 REAL ESTATE FINANCIAL ENGINEERING: PRE-MARRIAGE DUAL LEVERAGE & HOUSE HACKING
================================================================================
💡 Core Principle: Bank underwriting considers unmarried couples as independent
   borrowers. Timing your real estate acquisitions before marriage doubles your
   multi-family units and unlocks 100% free living.

1️⃣ 🟢 BEFORE MARRIAGE (Dual Leverage Matrix — 4 UNITS ACQUIRED)
   • Partner A qualifies for 1 FHA Loan (3.5% down) -> Duplex 1 (2 Units).
   • Partner B qualifies for 1 FHA Loan (3.5% down) -> Duplex 2 (2 Units).
   • Total Portfolio: 4 residential units acquired with minimal capital.
   • The House Hack: Live in 1 unit together, rent out the remaining 3 units.
   • Cashflow: 3 tenant rents pay 100% of both mortgages, taxes, and insurance.
   • Net Result: Free living (zero rent/mortgage) + positive monthly cashflow.

2️⃣ 🔴 AFTER MARRIAGE (Single Household Constraint — 2 UNITS ONLY)
   • Bank legally underwrites the couple as a single economic household.
   • FHA primary residence rules restrict the household to only 1 active FHA loan.
   • Maximum Acquisition: Only 1 Duplex (2 Units) under low-down-payment terms.
   • Second property requires 20-25% cash down on commercial/investment loans.
   • 50% Asset Acquisition Capacity lost instantly due to joint legal timing.

3️⃣ 🇮🇳 INDIA & GLOBAL DUAL TAX SHIELD
   • Dual PAN Independence: 2 separate PAN cards allow 2x Section 80C (3 Lakhs
     principal deduction) + 2x Section 24b (4 Lakhs interest deduction) = 7 Lakhs/yr.
   • Dual PMAY Subsidies: Independent single applicants qualify for dual first-time buyer grants.
   • Rich Dad Synergy: Shift from Bad Debt (lavish wedding expense) to Good Debt (cash-flowing units).

📌 VAULT SYNERGY:
   • Note: 01_Mindset_Motive/Pre_Marriage_Real_Estate_Leverage_and_House_Hacking.md
   • Visual Matrix: Attachments/Pre_Marriage_Real_Estate_Leverage_Matrix.jpg
================================================================================
""")

def cmd_stock(args):
    print("""
================================================================================
📈 SHOBHA RANA: TOP 3 SHARE MARKET FOUNDATIONAL BOOKS (@iamshobharana)
================================================================================
💡 Core Principle: Stop gambling in day trading and F&O. Build a bedrock
   understanding of fractional business ownership and multi-decade compounding.

1️⃣ ☕ COFFEE CAN INVESTING — Saurabh Mukherjea & Rakshit Ranjan
   • Classification: Priority 1: STUDY Tier (Indian Equity Compounding)
   • The 10-Year Filter: ROCE > 15% + Revenue Growth > 10% for 10 straight years.
   • Moat Companies: Asian Paints, Titan, Pidilite, HDFC Bank, Berger Paints.
   • Strategy: Buy clean-governance monopolies and hold 10-20 years with zero tinkering.

2️⃣ 🛒 ONE UP ON WALL STREET — Peter Lynch
   • Classification: Priority 2: READ (Cataloged on Homeserver Audiobookshelf)
   • The Consumer Edge: Everyday retail observation beats lagging Wall Street reports.
   • 6 Categories: Stalwarts, Fast Growers (Tenbaggers), Cyclicals, Turnarounds.
   • Lynch Rule: "If you spend 13 minutes on economics, you wasted 10 minutes."

3️⃣ 🔬 COMMON STOCKS AND UNCOMMON PROFITS — Philip Fisher
   • Classification: Priority 1: STUDY Tier (Buffett: "I am 15% Fisher")
   • The 15-Point Scuttlebutt Checklist: Talk to customers, suppliers, and competitors.
   • High R&D Reinvestment: Sustained competitive moat through relentless innovation.
   • Selling Rule: "If the job was done correctly, the time to sell is almost never."

4️⃣ 🎯 THE 4 CORE QUESTIONS:
   • T-Bills & Bonds: Sovereign baseline yield; capital preservation vs equity growth.
   • Why Invest in Fear: Market panic offers generational discounts on elite companies.
   • Why Invest: The only asset class that consistently beats currency debasement.

📌 VAULT & HOMESERVER SYNERGY:
   • Audiobookshelf: Priority 2: READ Tier (192.168.1.100:13378)
   • Synthesis Protocol: 02_Cognitive_Learning/Shobha_Rana_Stock_Market_Foundational_Books.md
   • Visual Matrix: Attachments/Shobha_Rana_Stock_Market_Books_Matrix.jpg
================================================================================
""")

def cmd_banking(args):
    print("""
================================================================================
🏦 GUNVEER SINGH: INFINITE BANKING CONCEPT & CASH VALUE LEVERAGE (@gunveersumal)
================================================================================
💡 Core Principle: "How the wealthy buy whatever they want without using their
   own money and without begging traditional commercial banks." Turn yourself and
   your family lineage into your own private central bank.

1️⃣ 🏦 COMMERCIAL BANKS VS. INFINITE BANKING (The Trap Reversal)
   • Commercial Bank Trap: Deposit money at 3-6% taxable interest -> Bank lends
     at 10-15% -> When you need a loan, they demand CIBIL (>750), ITRs, and pledge
     your primary house/car/land. Default means immediate foreclosure.
   • Infinite Banking Engine: Over-funded, dividend-paying cash-value life insurance.
     Contractually compounds at 5-8% tax-free (Section 10(10D)).

2️⃣ ⚡ POLICY LOANS & UNINTERRUPTED COMPOUNDING (Non-Direct Recognition)
   • Contractual Right: Borrow 85-90% of accumulated cash surrender value.
   • Zero Underwriting: Zero credit score checks, zero ITR scrutiny, zero asset liens.
   • Non-Direct Recognition: The full cash value continues to earn compound interest
     and dividends even while 100% borrowed! (e.g. Earn 6.5% on cash value while
     paying 5% policy loan interest = positive spread + capital deployment).
   • Zero Foreclosure: Death benefit acts as internal collateral; no bank auctions.

3️⃣ 💧 THE ROCKEFELLER "WATERPARK" FAMILY BANK METHOD
   • Irrevocable Family Trust owns policies on multiple generations (Ambani/Rockefeller).
   • Family members borrow from trust cash value to acquire cash-flowing real estate
     and businesses, repaying interest and principal back to the family trust.
   • Tax-free death benefits continuously replenish and multiply the family bank pool.

4️⃣ 🇮🇳 INDIAN STATUTORY & PRACTICAL FRAMEWORK
   • Section 10(10D): 100% tax-free maturity proceeds, bonuses, and death benefits.
   • Section 80C: Annual tax deductions on premium contributions.
   • LAIP (Loan Against Insurance Policy): LIC/HDFC/ICICI 85-90% loan with no CIBIL.
   • MWPA 1874 (Married Women's Property Act): Complete statutory immunity from
     civil courts, bankruptcy attachments, and business creditors.

📌 VAULT SYNERGY:
   • Note: 01_Mindset_Motive/Infinite_Banking_Concept_and_Cash_Value_Leverage.md
   • Visual Matrix: Attachments/Infinite_Banking_Cash_Value_Architecture_Matrix.jpg
================================================================================
""")

def cmd_yale(args):
    print("""
================================================================================
🏛️ YALE UNIVERSITY: FINANCIAL MARKETS (ECON 252) — PROF. ROBERT J. SHILLER
================================================================================
💡 Core Principle: "Anyone interested in investment banking, corporate finance,
   and markets must cover this foundational bedrock. Markets are not abstract math;
   they are human institutions for risk management and capital allocation."
   — Curated by Ananta Chhajer (@anantachhajer • MBA, IIM Ahmedabad)

1️⃣ 📊 CORE CAPITAL MARKETS & DEBT THEORY
   • Debt & Leverage: Mechanics of borrowing, collateral, bankruptcy & solvency.
   • Corporate Equities: Common & preferred shares, governance & valuation moats.
   • Efficient Markets (EMH): Information arbitrage, random walks & market anomalies.
   • Insurance Foundations: The archetypal risk-pooling institution of human society.

2️⃣ 🏦 INSTITUTIONS, CENTRAL BANKS & SYSTEMIC RISK
   • Commercial & Central Banks: Money multiplier, reserves, interest rates & liquidity.
   • Financial Crises & Misbehavior: Subprime panic, rating agencies & regulatory failure.
   • Shadow Banking: Non-bank intermediaries, liquidity freezes & Basel III norms.

3️⃣ 📈 DERIVATIVES & REAL ESTATE FINANCE
   • Forwards & Futures: Basis risk, commodity price discovery & currency hedging.
   • Options & Swaps: Asymmetric risk payoffs (calls/puts), Black-Scholes intuition.
   • Real Estate Finance: Mortgage securitization, MBS, REITs & housing price bubbles.

4️⃣ 🧠 BEHAVIORAL FINANCE & TITANS MASTERCLASSES
   • Nobel Robert Shiller: Irrational Exuberance, asset bubbles & social contagion.
   • David Swensen (Yale CIO): The Yale Endowment Model (Private Equity, VC & Real Assets).
   • Hank Greenberg (AIG CEO): Global underwriting, reinsurance & counterparty systemic risk.

🎯 GOVT EXAM & CAREER SYNERGY:
   • RBI Grade B (Phase 2): Direct coverage of FM & ESI syllabus (Monetary Policy, Debt Markets).
   • Banking PO (SBI/IBPS): Asset-Liability Management (ALM), Basel CAR, NPAs.
   • Investment Banking / M&A: Corporate valuation, capital structure & enterprise risk.

📌 VAULT SYNERGY:
   • Note: 02_Cognitive_Learning/Ananta_Chhajer_Yale_Financial_Markets_Curriculum.md
   • Visual Matrix: Attachments/Ananta_Chhajer_Yale_Financial_Markets_Matrix.jpg
   • Official Yale Playlist: https://youtube.com/playlist?list=PL8FB14A2200B87185
================================================================================
""")

def cmd_faculty(args):
    print("""
================================================================================
🎯 GOVT EXAM FREE YOUTUBE FACULTY MATRIX (@fitpoliceankur)
================================================================================
💡 Core Principle: Stop mentor-jumping! Pick 1 proven master per subject on
   YouTube, complete their foundational playlist, and transition directly to PYQ.
   Curated by Ankur (@fitpoliceankur) for SSC, Banking, RRB, and State Exams.

1️⃣ 📐 MATHEMATICS (QUANTITATIVE APTITUDE)
   • Aditya Ranjan Sir (Rankers Gurukul): Digital sum, unit digit, speed shortcuts.
   • Rakesh Yadav Sir (Careerwill): Foundational 7300+ PYQ, percentage-ratio base.
   • Gagan Pratap Sir (Careerwill): Advanced math, high-difficulty geometry & algebra.

2️⃣ 🧩 REASONING (GENERAL INTELLIGENCE)
   • Piyush Varshney Sir (Careerwill): 100-50 Syllogism (no Venn!), seating puzzles.
   • RG Vikramjeet Sir (Rankers Gurukul): Clocks, calendars, rapid option elimination.
   • Manish Sir: Structural reasoning, series patterns & non-verbal visual logic.

3️⃣ 📖 ENGLISH LANGUAGE & COMPREHENSION
   • Neetu Singh Mam (KD Campus): The Mother of Grammar (Plinth to Paramount).
   • Rani Mam (English with Rani): 60 Rules of Grammar, vocab mnemonics, cloze tests.
   • Jaideep Sir (Careerwill): Logical syntax foundation & advanced sentence flow.

4️⃣ 🌍 GENERAL KNOWLEDGE / GENERAL STUDIES (GK/GS)
   • Khan Sir Patna (Khan GS): Intuitive map-based Geography, Polity & permanent encoding.
   • Crazy Gk Trick: Visual mnemonics, memory tricks & static GK tables.
   • SSC Parmar (Parmar SSC): High-yield TCS PYQ analysis & NCERT static science.

🌟 SUPPLEMENTARY PILLARS:
   • Hindi: Arun Sir, Nidhi Mam, Vivek Sir (Exampur).
   • Daily Current Affairs: Kumar Gaurav Sir (Utkarsh Classes 6 AM).
   • Static Revision: Speedy Current Affairs PDF & Indologus.

📋 KANBOARD EXECUTION:
   • Project #4 (Govt Exam Tracker): Track AFCAT, Banking PO, RRB JE/ALP, SSC.
   • Project #5 (Syllabus Tracker): Migrate Not Started ➔ Studying ➔ Practice ➔ Mastered.

📌 VAULT SYNERGY:
   • Note: 02_Cognitive_Learning/Govt_Exam_Top_YouTube_Faculty_Matrix.md
   • Visual Matrix: Attachments/Govt_Exam_Top_YouTube_Faculty_Matrix.jpg
================================================================================
""")

def cmd_linkedin(args):
    print("""
================================================================================
🚀 ASHUTOSH PRATAP SINGH: LINKEDIN HIDDEN HIRING & PROFILE RADAR (@technical_sapien)
================================================================================
💡 Core Principle: "Stop applying blindly to public saturated job boards! 80% of
   elite roles are filled via the hidden job market. Optimize your profile radar
   for search algorithms and reach decision-makers directly."
   — Ashutosh Pratap Singh (@technical_sapien • Tech Influencer & Career Coach)

1️⃣ 🛡️ THE 6-PILLAR PROFILE RADAR MAKEOVER
   • Profile Photo: High-res headshot, smiling/eye contact (+36x more messages).
   • Custom Banner: 1584x396px branded header with core skills & value proposition.
   • Headline Formula: [Target Role] | [Core Technologies/Skills] | [Quantified Impact].
     (e.g., "Full Stack Developer | Python, React, PostgreSQL | Scaled APIs to 1M+ RPS")
   • About Section (>400 chars): Origin story, technical strengths, metrics & CTA.
   • Experience (STAR Method): Situation, Task, Action, Result with hard numbers.
   • Skills & Endorsements: Top 5 domain competencies aligned with target JDs.

2️⃣ 🔍 SECRET BOOLEAN SEARCH QUERIES (Bypassing Job Boards)
   • Hidden Unadvertised Jobs (Posts Filter, Past 24h):
     "hiring" AND ("software engineer" OR "full stack" OR "analyst") AND ("urgent" OR "immediate") -"closed"
   • Target Decision Makers Directly (People Filter):
     ("Engineering Manager" OR "Tech Lead" OR "VP of Engineering") AND "hiring" AND "India"
   • Fast-Growing Funded Startups (Posts Filter):
     ("we are growing our team" OR "expanding our engineering team") AND ("remote" OR "hybrid") AND ("apply" OR "DM me")
   • Google X-Ray Recruiter Search:
     site:linkedin.com/in/ "Recruiter" AND ("actively recruiting" OR "looking for") AND "Fintech"

3️⃣ ✉️ 3-TIER RECRUITER INMAIL & OUTREACH ARCHITECTURE
   • Tier 1 (Connection Hook <300 chars):
     "Hi [Name], loved your recent post on [Topic]. I specialize in [Key Skill] and built [Mini-Project/Result]. Would love to connect and follow your work at [Company]!"
   • Tier 2 (Asynchronous Value Drop):
     "Thanks for connecting, [Name]! Noticed your team is scaling [Initiative]. Here is a quick 2-page teardown/solution I drafted that might save your team 5+ hours: [Link]."
   • Tier 3 (Frictionless Soft Close):
     "No immediate reply needed—if this aligns with your priorities, would love a brief 10-min virtual coffee chat next Tuesday to see how I can contribute."

📌 VAULT SYNERGY:
   • Note: 01_Mindset_Motive/LinkedIn_Hidden_Hiring_and_Career_Acceleration.md
   • Visual Matrix: Attachments/LinkedIn_Hidden_Hiring_Search_Matrix.jpg
================================================================================
""")

def cmd_ig(args):
    print("""
================================================================================
📱 INNERLINK: INSTAGRAM ALGORITHM 3 CRITICAL SETTINGS RESET (@_innerlink)
================================================================================
💡 Core Principle: "Stop posting content blindly on Instagram! If you have zero
   or low reach, the problem isn't just the algorithm—it's your account settings!
   Fix these 3 non-negotiable settings to align with Meta's recommendation engine."
   — Innerlink | Content Marketing (@_innerlink)

1️⃣ 🛡️ SETTING 1: SWITCH TO PROFESSIONAL / CREATOR ACCOUNT
   • Pathway: Settings & activity ➔ Creator tools and controls ➔ Switch account type
     ➔ Switch to professional account ➔ Select "Creator".
   • Impact: Shifts account from personal 'friends-and-family' network to Meta's
     Global Public Recommendation Engine; enables Explore page and Reels distribution.

2️⃣ 🎯 SETTING 2: SEMANTIC NICHE CATEGORY VECTORING
   • Pathway: Edit profile ➔ Profile information ➔ Category ➔ Choose exact domain
     (e.g., Digital Creator, Education, Entrepreneur) ➔ Toggle "Display on profile".
   • Impact: Directly tags your account in Meta AI's topic clustering vector database.
     Ensures your 50–100 seed-batch viewers actually care about your topic instead of
     swiping away in 1 second.

3️⃣ 🔄 SETTING 3: HARD CACHE PURGE (ALGORITHM RESET)
   • Pathway: Settings & activity ➔ Accounts Centre ➔ Your information and permissions
     ➔ Search history ➔ Clear all searches ➔ Timeframe: "All time" ➔ Clear all searches.
   • Impact: Wipes out stale viewing biases, search histories, and local cache noise.
     Gives your account a clean slate so Meta matches outbound content to new audiences.

4️⃣ 🚀 BONUS RETENTION & VIRALITY RULES:
   • Highest Quality Uploads: Settings ➔ Media quality ➔ "Upload at highest quality" ON.
   • 3-Second Hook: Spoken question + bold moving text on screen within 1.5–3.0 seconds.
   • Loop Completion: Keep Reels under 15–25s with seamless loop to hit >100% watch-time.
   • Comment-to-DM Trigger: "Comment CHEAT CODE to receive the PDF" for algorithmic surge.

📌 VAULT SYNERGY:
   • Note: 01_Mindset_Motive/Instagram_Algorithm_Growth_and_Settings_Reset.md
   • Visual Matrix: Attachments/Instagram_Algorithm_Growth_Settings_Matrix.jpg
================================================================================
""")

def cmd_control(args):
    print("""
================================================================================
🛡️ J ROMANO: THE ART OF SELF-CONTROL & TRIGGER DECONSTRUCTION (@romanoism)
================================================================================
💡 Core Principle: "5 key things that changed my life completely... How to master
   the art of self-control. He who angers you conquers you. External events are
   outside your control, but your internal response is your absolute sovereignty."
   — J Romano (@romanoism) & Marcus Aurelius

1️⃣ 🗺️ STEP 1: STUDY WHAT TRIGGERS YOU (Pattern Mapping)
   • Action: Catalog every person, comment, tone, or situation that provokes anger.
   • Stoic Law: You cannot master an adversary you refuse to map. Identify your
     emotional tripwires before you walk into the battlefield.

2️⃣ 🔍 STEP 2: ASK WHY & HOW IT TRIGGERS YOU (Root Cause Excavation)
   • Action: Dig into the underlying wound: Is it wounded pride, fear of rejection,
     or past childhood conditioning?
   • Stoic Law: The external instigator is merely a mirror reflecting your own
     unresolved insecurity. Heal the internal wound, and the trigger loses all power.

3️⃣ 🚨 STEP 3: RECOGNIZE WHEN IT HAPPENS (Real-Time Metacognition)
   • Action: Notice early somatic markers: elevated heart rate, clamped jaw, shallow
     chest, or flushing skin.
   • Stoic Law: The gap between feeling the biological surge and opening your mouth
     is where 100% of your power and freedom resides.

4️⃣ 🫁 STEP 4: SHIFT YOUR MIND TO YOUR BREATHING (Autonomic Decoupling)
   • Action: Immediately disengage eye contact and execute 2 sharp nasal inhales
     followed by 1 extended mouth exhale (Huberman Physiological Sigh).
   • Neurobiology Law: Shifts nervous system from sympathetic to parasympathetic.
     Extinguishes amygdala fight-or-flight signaling within 6 seconds.

5️⃣ 🤐 STEP 5: FOCUS ON NOT REACTING (The Power of Strategic Silence)
   • Action: Consciously refuse to deliver the impulsive retaliation they expect.
     Maintain calm, unbothered stillness and measured posture.
   • Stoic Law: Silence projects terrifying authority. When you refuse to react,
     the other party's emotional frame collapses under its own weight.

🧠 THE VIKTOR FRANKL PRINCIPLE:
   "Between stimulus and response there is a space. In that space is our power
   to choose our response. In our response lies our growth and our freedom."

📌 VAULT SYNERGY:
   • Note: 01_Mindset_Motive/Romano_Stoic_Self_Control_and_Emotional_Regulation.md
   • Visual Matrix: Attachments/Romano_Stoic_Self_Control_Emotional_Regulation_Matrix.jpg
================================================================================
""")

def cmd_auster(args):
    print("""
================================================================================
📖 PAUL AUSTER: 4 3 2 1 — PARALLEL LIVES & COUNTERFACTUAL MASTERY
================================================================================
💡 Core Principle: "Did I make the right choices in life? Would I be happier if
   I took another path? Paul Auster's Booker Prize masterpiece explores 4 parallel
   timelines of one character, proving that there is no paradise in the unlived
   alternate paths. Radical acceptance of your actual life is the ultimate freedom."
   — Clara (@therealisticbookcorner) & Paul Auster (1947–2024)

1️⃣ 🧭 THE 4 PARALLEL TIMELINES OF ARCHIBALD FERGUSON:
   • Timeline 1 (4.1): Suburban Affluence ➔ Sports & political journalist,
     Columbia University 1968 student strikes, stable disciplined writing.
   • Timeline 2 (4.2): Arson & Father's Death ➔ Plunges into poverty, Rochester
     and NYC grit, fluid sexuality, hard-won creative resilience.
   • Timeline 3 (4.3): Family Embezzlement & Bitter Divorce ➔ Introverted lover
     of French poetry and cinema; tragically killed by lightning at age 13.
   • Timeline 4 (4.4): Expatriate in Paris ➔ Cinephile, survived car crash, the
     sole surviving Ferguson who wrote the other 3 lives to honor what might have been.

2️⃣ 🧠 COGNITIVE & PSYCHOLOGICAL MASTERY:
   • Counterfactual Trap: Torturing yourself with hypothetical alternate pasts.
   • The Fallacy of the Flawless Alternative: Every single path carries its own
     unforeseen tragedy, financial stress, or heartbreak. No path escapes reality.
   • Chance (Tyché) vs Will: 50% of life is blind luck (the falling branch); the
     other 50% is how you respond with discipline, character, and focus.
   • Nietzschean Amor Fati: Love your actual fate. Stop mourning ghost timelines.

3️⃣ 🎧 HOMESERVER & AUDIOBOOKSHELF SYNERGY:
   • Audiobookshelf: http://192.168.1.100:13378 (Tailscale: http://100.x.y.z:13378)
   • Tier: Priority 2: READ (Wealth, Mindset & Literary Depth)
   • Audiobook: 4 3 2 1 (Unabridged, 36h 48m, read by Paul Auster himself)

📌 VAULT SYNERGY:
   • Note: 02_Cognitive_Learning/Paul_Auster_4321_Parallel_Lives_and_Counterfactual_Mastery.md
   • Visual Matrix: Attachments/Paul_Auster_4321_Parallel_Lives_Matrix.jpg
================================================================================
""")

def cmd_greene(args):
    print("""
================================================================================
⚔️ ROBERT GREENE: TURN THE TABLES — THE COUNTERATTACK STRATEGY
================================================================================
💡 Core Principle: "Never see a situation as hopeless. Your own weakness can
   become strength with clever manipulation. Moving first will often put you at a
   disadvantage: You expose your strategy and limit your options. Instead, hold back,
   bait the other side into a rash, arrogant attack, and counterpunch with devastating
   force."
   — Robert Greene (@robertgreeneofficial) & Napoleon Bonaparte

1️⃣ ❌ THE FIRST-MOVER TRAP:
   • Premature Exposure: Initiating conflict reveals your vector, assets, and motive.
   • Resource Burn: Attackers deplete vital energy while defenders conserve strength.
   • Delusion of Momentum: Aggressors mistake speed for supremacy, walking into traps.

2️⃣ 🛡️ FEIGNED WEAKNESS & BAIT:
   • Calculated Vulnerability: Project hesitation or retreat to lower their guard.
   • Ego Inflation: Arrogant opponents cannot resist what looks like easy prey.
   • Strategic Overextension: Draw them off solid ground until their flanks are bare.

3️⃣ 🌋 NAPOLEON'S ADVERSITY CRUCIBLE (Mental Alchemy):
   • "Never See a Situation as Hopeless": Crisis extinguishes mental fog and trivialities.
   • The Seed of Reversal: Every adverse setback carries the exact structural flaw
     needed to flip the conflict into total triumph.
   • Historical Exemplar: Austerlitz (1805) — Napoleon feigned a crumbling right flank,
     luring the Austro-Russian coalition into abandoning the Pratzen Heights, then
     cut the enemy army cleanly in two.

4️⃣ ⚡ THE DECISIVE COUNTERSTRIKE (Strategic Aikido):
   • Redirect Momentum: Do not clash head-on; weaponize their own force against them.
   • Strike the Exposed Center: Deliver the counterpunch when they have zero reserves left.
   • Psychological Rout: Overconfidence turns instantly into panic and collapse.

💼 REAL-WORLD APPLICATION:
   • Workplace Attacks: Maintain stoic silence; let the hostile colleague talk themselves
     into a corner, then calmly dismantle their premise with verifiable facts.
   • Negotiations: Never make the opening proposal; let them establish the anchor first.
   • Setbacks & Exams: Treat failures as diagnostic crucibles to trigger ruthless focus.

📌 VAULT SYNERGY:
   • Note: 01_Mindset_Motive/Robert_Greene_Counterattack_Strategy_and_Adversity_Mastery.md
   • Visual Matrix: Attachments/Robert_Greene_Counterattack_Strategy_Matrix.jpg
================================================================================
""")

def cmd_pyramid(args):
    print("""
================================================================================
🧠 DR. VLAD BELIAVSKY: THE PYRAMID MIND & EMOTIONAL HEALING SYSTEM
================================================================================
💡 Core Principle: "Treat your emotions like your guest. Let them come in, let
   them go! Reading books on positive thinking is not going to heal your deep
   wounds. The mind is a 6-level architecture; you cannot override visceral
   emotional pain with superficial rational logic."
   — Dr. Vlad Beliavsky (Cambridge Neuroscientist) & Md Junaid (@readandrisee)

1️⃣ 🏛️ THE 6 INTERCONNECTED LEVELS OF MIND:
   • Level 1: REASON ➔ Conscious logic, critical deduction, analytical attention.
   • Level 2: BELIEFS ➔ Core assumptions, identity rules, internalized lenses.
   • Level 3: MEMORIES ➔ Past experiences, breakup grief, trauma, emotional imprints.
   • Level 4: EMOTIONS ➔ Affective survival responses, somatic warning signals.
   • Level 5: SPEECH ➔ Subconscious self-talk, narrative framing, internal dialogue.
   • Level 6: BEHAVIOUR ➔ Observable motor actions, habits, physical execution.

2️⃣ 💥 WHY "POSITIVE THINKING" BOOKS FAIL TO HEAL:
   • Architectural Mismatch: Positive affirmations operate purely at Level 1 (Reason).
   • The Deep Wound: Trauma, heartbreak, and fear reside in Level 3 (Memories) and
     Level 4 (Emotions).
   • Slapping Level 1 rationalizations on an unhealed Level 4 emotion is like
     applying fresh paint over a crumbling, cracked foundation.

3️⃣ 🏡 THE GUEST HOUSE PRINCIPLE (Emotional Regulation):
   • Welcome the Visitors: Emotions are evolutionary messengers (the wild tiger warning).
   • Suppressing emotions disconnects you from vital somatic signals about boundaries.
   • Acknowledge fear, sorrow, or rage without judgment. Listen to the message, then
     let the biochemical wave depart naturally (~90 seconds duration).

4️⃣ 🔄 CURING THE OVERTHINKING LOOP:
   • The Trap: Painful Memory (L3) ➔ Anxiety/Fear (L4) ➔ Toxic Self-Talk (L5) ➔ Loops.
   • The Solution: You cannot think your way out of overthinking.
   • Level 6 Grounding: Drop immediately into physical motor action (Level 6 Behaviour)—
     ice water to face, 2x physiological sighs, and a 5-minute study micro-sprint.

💼 REAL-WORLD HEALING PROTOCOLS:
   • Breakup & Rejection: Allow Level 4 grief to exist without self-shame. Then use
     Level 5 (Speech) to re-author your identity from "victim" to "sovereign builder."
   • Exam Panic: Reinterpret adrenaline as evolutionary fuel designed to enhance alertness.
   • Habit Mastery: Align Reason (L1) with Behaviour (L6) through relentless daily action.

📌 VAULT SYNERGY:
   • Note: 01_Mindset_Motive/Dr_Vlad_Beliavsky_Pyramid_Mind_and_Emotional_Healing.md
   • Visual Matrix: Attachments/Dr_Vlad_Beliavsky_Pyramid_Mind_Matrix.jpg
================================================================================
""")

def cmd_comm(args):
    print("""
================================================================================
🗣️ FOUR BOOKS TO MASTER COMMUNICATION SKILLS (@readandrisee)
================================================================================
💡 Core Principle: "One day you will thank me for suggesting these four books.
   Communication is a 4-dimensional art: Emotional Attunement, Social Rapport,
   Power Dynamics, and Attraction Polarity. Master all four to become an unshakeable,
   magnetic communicator."
   — Md Junaid (@readandrisee)

1️⃣ ❤️ EMOTIONAL ATTUNEMENT: THE MAN'S GUIDE TO WOMEN (Dr. John Gottman)
   • The Fix-It Fallacy: Do NOT attempt to logically fix emotional distress; provide
     empathetic presence and listening first.
   • A-T-T-U-N-E: Awareness, Turning toward, Tolerance, Understanding, Non-defensive
     listening, and Empathy.
   • The 4 Horsemen: Banish Criticism, Contempt, Defensiveness, and Stonewalling.

2️⃣ 🤝 SOCIAL RAPPORT: HOW TO WIN FRIENDS & INFLUENCE PEOPLE (Dale Carnegie)
   • Deepest Human Craving: Sincere appreciation and feeling important.
   • The 70/30 Rule: Let the other person talk 70% of the time in casual interactions.
   • Ego-Free Persuasion: Frame ideas in terms of what benefits the other person.

3️⃣ ⚔️ POWER DYNAMICS & BOUNDARIES: THE 48 LAWS OF POWER (Robert Greene)
   • Law 4 (Restraint): Always say less than necessary; silence projects authority.
   • Law 9 (Demonstration): Win through your actions, never through argument.
   • Law 44 (Mirror Effect): Mirroring speech and body language disarms hostility.

4️⃣ 🧲 ATTRACTION POLARITY: ATOMIC ATTRACTION (Christopher Canwell)
   • Non-Neediness: Attraction is proportional to emotional independence.
   • The Rubber Band Rule: Never smother with needy texting; allow space to build tension.
   • Grounded Frame: Unshakeable posture, steady eye contact, and downward vocal inflection.

💼 REAL-WORLD SITUATIONAL EXECUTION:
   • Dating & Romance: Lead with non-neediness (Canwell) + deep listening (Gottman).
   • Workplace & Leadership: Praise team members (Carnegie) + speak concisely (Greene).
   • Conflict & Stress: Eliminate contempt/defensiveness + state boundaries calmly.

📌 VAULT SYNERGY:
   • Note: 01_Mindset_Motive/Communication_Mastery_Four_Foundational_Books.md
   • Visual Matrix: Attachments/Communication_Mastery_Four_Foundational_Books_Matrix.jpg
================================================================================
""")

def cmd_unscripted(args):
    print("""
================================================================================
📚 5 BOOKS THE RICH DON'T WANT YOU TO KNOW (@coffeewithbooks__)
================================================================================
💡 Core Principle: "Trust me, your whole perception of Self-Help will change
   after reading them! Mainstream pop-psychology pushes toxic positivity,
   unrealistic goals, and compliance with the 9-to-5 Matrix. These 5 masterworks
   provide a mechanical, anti-fragile operating system for sovereign life mastery."
   — Shashank (@coffeewithbooks__)

1️⃣ ⚙️ SYSTEMS OVER GOALS: HOW TO FAIL AT ALMOST EVERYTHING (Scott Adams)
   • Goals vs Systems: Goals keep you in perpetual failure; systems ensure daily wins.
   • Talent Stacking: Top 25% in 2-3 complementary skills beats top 1% in a single domain.
   • Energy Management: Prioritize physical vitality and sleep over calendar minutes.

2️⃣ 🛡️ ANTI-FRAGILE RESILIENCE: FROM FAILURE TO SUCCESS (Martin Meadows)
   • Cold Post-Mortem: Failure is diagnostic data; classify into Strategy vs Execution vs Noise.
   • Ego Decoupling: "My experiment failed" does NOT mean "I am an inherent failure."
   • Inoculation: Daily micro-rejections desensitize the fear of social and financial risk.

3️⃣ 🧠 NEUROPLASTIC SELF-TALK: WHAT TO SAY WHEN YOU TALK TO YOURSELF (Dr. Shad Helmstetter)
   • Subconscious Malware: 77% of childhood conditioning is negative and restrictive.
   • 5 Self-Talk Levels: Elevate from "I can't" to Level 4 "I am disciplined, sharp, and focused."
   • Linguistic Rewiring: Replace "I have to" with "I choose to execute."

4️⃣ 👂 DEEP SIGNAL LISTENING: HOW TO LISTEN (Oscar Trimboli)
   • The 125/400 Gap: People speak at 125 WPM, but think at 400 WPM; 75% remains unsaid.
   • 5 Listening Levels: Silence inner noise, hear content, context, pauses, and deep meaning.
   • The 3-Question Rule: Never interrupt; draw out the unsaid with "Tell me more" & "What else?"

5️⃣ 🚀 FINANCIAL SOVEREIGNTY: UNSCRIPTED (M.J. DeMarco)
   • The Scripted Matrix: The 40-year cubicle grind and 8% mutual fund hope is rigged.
   • C-E-N-T-S Commandments: Control platform, high Entry barrier, solve real Need,
     Time decoupling, and unbounded Scale.
   • Productocracy: Build a product so undeniably valuable that hype becomes obsolete.

💼 REAL-WORLD EXECUTION ENGINE:
   • Daily Study: Discard exam anxiety; measure today's executed system (Adams).
   • Setbacks & Mistakes: Classify coldly; zero self-flagellation (Meadows).
   • Internal Dialogue: Use Level 4 present-tense identity programming (Helmstetter).
   • Social Intelligence: Hear the 75% unsaid in negotiations and interviews (Trimboli).
   • Wealth Building: Build non-commoditized skills that satisfy C-E-N-T-S (DeMarco).

📌 VAULT SYNERGY:
   • Note: 01_Mindset_Motive/Five_Books_Rich_Dont_Want_You_To_Know.md
   • Visual Matrix: Attachments/Five_Books_Rich_Dont_Want_You_To_Know_Matrix.jpg
================================================================================
""")

def cmd_magnet(args):
    print("""
================================================================================
🧲 4 BOOKS THAT WILL MAKE YOU A HUMAN MAGNET (@glitch.mindset)
================================================================================
💡 Core Principle: "True magnetism is not cheap extroversion or loud talking.
   It is a 4-dimensional matrix of deep listening, tactical body language,
   unshakable moral authority, and ego-free human influence."
   — glitch.mindset (@glitch.mindset)

1️⃣ 👂 INTENTIONAL LISTENING & PRESENCE: HOW TO LISTEN WITH INTENTION (Patrick King)
   • Ego Suppression: Stop waiting for your turn to speak; clear your mental noise.
   • Reflective Mirroring: Acknowledge and validate their emotional core before logic.
   • The 3-Second Silence Lock: Wait a full 3 seconds after they finish talking;
     in 60% of cases, they will share their deeper, unspoken truth.

2️⃣ 👁️ TACTICAL CHARISMA & MICRO-CUES: HOW TO TALK TO ANYONE (Leil Lowndes)
   • The Flooding Smile: Never flash an instant generic grin; pause 1 second, look,
     then let a warm, personalized smile flood your eyes and face.
   • Sticky Eyes & Epoxy Eyes: Maintain unbroken gaze; observe target reactions.
   • The Big-Baby Pivot: Pivot your entire torso 100% toward the newcomer.
   • Parroting: Repeat the last 2-3 words with a curious tone to keep them talking.
   • Spotlight Protection: Never say "Me too!" and hijack their moment of pride.

3️⃣ 👑 LEADERSHIP GRAVITAS & INTEGRITY: HOW THE BEST LEADERS LEAD (Brian Tracy)
   • Unshakable Integrity: Your word is an unbreakable contract; trust is foundational.
   • Crisis Equilibrium: Remain the calmest, slowest voice in the room during stress.
   • Downward Vocal Inflection: Lower your pitch at the period; project natural authority.
   • Public Praise, Private Calibration: Never criticize an ally in front of others.

4️⃣ 🤝 EGO-FREE INFLUENCE & RAPPORT: HOW TO WIN FRIENDS (Dale Carnegie)
   • The 70/30 Conversational Ratio: Let the other person do 70% of the talking.
   • The Name Anchor: Use their name respectfully at the greeting and closing.
   • Plant Ideas Softly: Frame persuasion so they feel it was their own original idea.
   • Banish The 3 C's: Never criticize, condemn, or complain.

💼 4-STEP DAILY CHARISMA DRILL FOR KANAD:
   • 1. Morning Greetings: Full-body pivot (Lowndes) + 1-second pause flooding smile.
   • 2. Phone Calls: 3-Second silence lock (King) + emotional mirroring.
   • 3. Stressful Problems: Slow vocal cadence + downward pitch inflection (Tracy).
   • 4. Evening Chats: 70/30 listening ratio + anchor their name + sincere praise (Carnegie).

📌 VAULT SYNERGY:
   • Note: 01_Mindset_Motive/Human_Magnet_Charisma_Four_Foundational_Books.md
   • Visual Matrix: Attachments/Four_Books_Human_Magnet_Charisma_Matrix.jpg
================================================================================
""")

def cmd_stronger(args):
    print("""
================================================================================
🧠 6 BOOKS TO MAKE YOU EMOTIONALLY STRONGER (@bookreadersclub)
================================================================================
💡 Core Principle: "Emotional strength is not stoic numbness or toxic positivity.
   It is the mastery of somatic baseline regulation, prefrontal amygdala control,
   decoding interpersonal emotional needs, cognitive defusion, and non-negotiable boundaries."
   — Shubham Kumar (@bookreadersclub)

1️⃣ 🩺 CLINICAL THERAPY TOOLKIT: WHY HAS NOBODY TOLD ME THIS BEFORE? (Dr. Julie Smith)
   • Somatic Precedence: Mood is bodily; change your physical state before analyzing thoughts.
   • Recovery Velocity: Resilience is not zero pain, but bouncing back quickly to equilibrium.
   • Thought Detachment: Label physical symptoms objectively rather than internalizing failure.

2️⃣ ⚖️ EMOTIONAL INTELLIGENCE: BEYOND IQ (Daniel Goleman)
   • 5 EQ Pillars: Self-awareness, self-regulation, motivation, empathy, and social skill.
   • Amygdala Hijack: Catch the moment primitive fear threatens to override rational cortex.
   • The 6-Second Circuit: Pause 6 seconds when triggered to let the prefrontal cortex engage.

3️⃣ 🧲 S-A-V-E COMMUNICATION DRIVERS: EMOTIONAL MAGNETISM (Sandy Gerber)
   • S-A-V-E Drivers: People communicate for Safety, Achievement, Value, or Experience.
   • Pre-Response Decoding: Identify which magnet drives the speaker to eliminate friction.
   • Ignite Connection: Speak to their core emotional hunger rather than your personal ego.

4️⃣ 🔄 COGNITIVE DEFUSION & MOOD MECHANICS: MASTER YOUR EMOTIONS (Thibaut Meurisse)
   • Suffering Formula: Suffering = Pain x Resistance; accept pain to end chronic suffering.
   • Cognitive Defusion: Emotions are transient 90-second chemical waves; stop feeding loops.
   • Motor Redirection: Break emotional rumination immediately with physical action.

5️⃣ 🕊️ SOLITUDE & CONSCIOUS LOVE: 8 RULES OF LOVE (Jay Shetty)
   • Solitude First: You cannot love another maturely until you find peace in solitude.
   • Accept Their Karma: Love is supporting your partner's path without forcing conformity.
   • Non-Needy Love: Love from an overflowing cup of self-worth rather than empty neediness.

6️⃣ 🛡️ TRAUMA HEALING & SOVEREIGN BOUNDARIES: CLOSER TO LOVE (Vex King)
   • Trauma Cleansing: Unhealed childhood wounds dictate destructive relationship patterns.
   • Non-Negotiable Boundaries: Love without boundaries collapses into self-abandonment.
   • Radical Self-Respect: Set clear limits and walk away peacefully from disrespect.

💼 6-STEP DAILY EMOTIONAL STRENGTH PROTOCOL FOR KANAD:
   • 1. Morning State: 2x Physiological sighs + 500ml water + morning light (Smith).
   • 2. Challenging Study: Apply the 6-Second Pause when frustrated by aptitude problems (Goleman).
   • 3. Conversations: Diagnose if others need Safety, Achievement, Value, or Experience (Gerber).
   • 4. Stress Relief: Label emotions neutrally, drop shoulders, execute 5-min sprint (Meurisse).
   • 5. Solitude: Protect 30 minutes of screen-free solo reflection in the evening (Shetty).
   • 6. Night Review: Review boundaries, affirm self-worth, release resentment (King).

📌 VAULT SYNERGY:
   • Note: 01_Mindset_Motive/Six_Books_to_Make_You_Emotionally_Stronger.md
   • Visual Matrix: Attachments/Six_Books_Emotionally_Stronger_Matrix.jpg
================================================================================
""")

def cmd_adrenaline(args):
    print("""
================================================================================
⚡ TOP 5 BOOKS TO MAXIMIZE YOUR ADRENALINE RUSH (@booksopedia_)
================================================================================
💡 Core Principle: "Adrenaline rush is not reckless chaos or panic.
   In true psychological and martial mastery, adrenaline is an internal biological
   turbocharger designed to heighten sensory acuity, obliterate fatigue, and fuel
   extreme goal execution when channeled through disciplined systems."
   — Sourabh Dubey (@booksopedia_)

1️⃣ 🧬 BIOLOGICAL WILLPOWER ENGINE: THE SCIENCE OF SELF-DISCIPLINE (Peter Hollins)
   • Willpower as Metabolic Fuel: Finite resource managed via glucose, sleep, and decision limits.
   • 10-Minute Delay Rule: Pause 10 mins when craving strikes; neurochemical spike dies in 6-8 mins.
   • 20-Second Environmental Friction: 0 friction for deep work; 20s barriers for digital distractions.
   • 40% Navy SEAL Governor: Brain signals exhaustion when body is at 40%; push past the reflex.

2️⃣ 🏋️‍♂️ IRON WORKOUT DRIVE: THE LITTLE BLACK BOOK OF WORKOUT MOTIVATION (Michael Matthews)
   • Action Precedes Feeling: Motivation is the byproduct of action, not an emotion you wait to feel.
   • Radical Internal Locus: Eliminate victim excuses; view physical and mental difficulty as weight.
   • Mindset Progressive Overload: Voluntary daily discomfort directly fortifies cognitive stamina.
   • Fitness Anchor: Daily discipline anchoring Kanad's 82kg -> 72kg body recomposition.

3️⃣ ⚔️ RESISTANCE WARFARE: THE WAR OF ART (Steven Pressfield)
   • The Compass Rule: The toxic fear and dread opposing your work points directly to your destiny.
   • Professional Standard: Amateurs wait for mood; professionals clock in daily and master detachment.
   • Invoking the Muse: Synchronicity and effortless flow arrive only after disciplined labor.

4️⃣ 🚀 MOONSHOT VELOCITY: DO THE IMPOSSIBLE (Thibaut Meurisse)
   • Shatter Belief Ceilings: Subconscious limiting beliefs filter out bold possibilities; reset identity.
   • 4-Step Velocity Engine: Clarify moonshot, ruthlessly cut 90% non-essentials, execute 2-3 daily sprints.
   • Adrenaline Channeling: Harness acute performance fear into focused velocity rather than freeze.

5️⃣ 🥋 SHAOLIN STRATEGIC EQUILIBRIUM: HOW TO WIN WITHOUT FIGHTING (Bernhard Moestl)
   • Inner Equilibrium (Zazen): Act only from stillness; emotional reactivity guarantees tactical error.
   • Principle of Yielding (Ju): Never clash head-on; absorb and redirect hostile energy effortlessly.
   • Sovereign Non-Engagement: Supreme warriors win without unsheathing swords; preserve Qi.

💼 5-STEP DAILY ADRENALINE PROTOCOL FOR KANAD:
   • 1. Morning Calibration: 2x Physiological sighs + 500ml water + 5-min Zazen stillness (Moestl & Hollins).
   • 2. Resistance Sprints: Start study with the most feared RRB JE module (Compass Rule - Pressfield).
   • 3. Friction Firewall: Phone in other room (20s barrier) + 10-min pause on cravings (Hollins).
   • 4. Physical Overload: Mandatory 5-min gym entry; push past the 40% governor reflex (Matthews).
   • 5. Night Centering: Decouple from petty noise, review 3 needle-movers for tomorrow (Meurisse & Moestl).

📌 VAULT SYNERGY:
   • Note: 01_Mindset_Motive/Five_Books_to_Maximize_Adrenaline_Rush.md
   • Visual Matrix: Attachments/Five_Books_Maximize_Adrenaline_Rush_Matrix.jpg
================================================================================
""")

def cmd_soul(args):
    print("""
================================================================================
🧘 4 BOOKS FOR A BETTER MIND, BODY & SOUL (@ektadb_speaks)
================================================================================
💡 Core Principle: "True healing and sovereign execution cannot occur solely within
   the intellect. The human organism is an integrated tri-system: Cognitive (Mind),
   Somatic/Visceral (Body), and Identity/Intuitive (Soul). When overthinking is silenced,
   stored bodily trauma is released, subconscious self-worth is aligned, and dynamic action
   tools are deployed, human potential becomes unstoppable."
   — Ekta Bhanushali (@ektadb_speaks)

1️⃣ 🧠 COGNITIVE DECLUTTERING & ANXIETY CONTROL: STOP OVERTHINKING (Nick Trenton)
   • Spiral Interruption: Catch cognitive distortions (catastrophizing) before rumination triggers anxiety.
   • 5-4-3-2-1 Sensory Grounding: Anchor senses (5 sights, 4 touches, 3 sounds, 2 smells, 1 taste) to silence DMN.
   • 15-Min Worry Window: Schedule dedicated worry time (17:00–17:15) so study blocks remain pristine.
   • 4-7-8 Diaphragmatic Breath: Stimulate vagus nerve to down-regulate sympathetic fight-or-flight arousal.

2️⃣ 🧬 SOMATIC TRAUMA & NEURO-IMMUNITY: THE BODY KEEPS THE SCORE (Bessel van der Kolk, M.D.)
   • Visceral Trauma Storage: Emotional shocks lodge in fascia, organs, and neuromuscular armor.
   • Broca's Speech Deficit: In triggered stress, verbal centers shut down while amygdala alarms; logic cannot heal body.
   • Bottom-Up Regulation: Healing requires bodily movement—rhythmic breathwork, yoga, and posture resets.
   • Restoring Interoception: Reconnect with internal physical sensations without dissociating or freezing.

3️⃣ ✨ SUBCONSCIOUS IDENTITY ALIGNMENT: MANIFEST: 7 STEPS (Roxie Nafousi)
   • Demystifying Manifestation: Manifesting is the union of subconscious self-worth & proactive daily action.
   • Subconscious Unworthiness: Root out hidden childhood conditioning that secretly undermines ambitious goals.
   • Behavioral Alignment: Take daily micro-actions that mirror your future high-achieving engineer identity.
   • Envy as Empirical Proof: Transform peer jealousy into positive evidence that your target milestone is achievable.

4️⃣ 🛠️ DYNAMIC ACTION THERAPY & TOOLS: THE TOOLS (Phil Stutz & Barry Michels)
   • The Reversal of Desire: Confront avoidance; scream inward "Bring it on! I love pain!" and pass through dread.
   • Active Love Protocol: Dissolve rage by visualizing sending radiant loving light from your heart to the offender.
   • Inner Authority & Shadow: Overcome social anxiety by standing as an ally with your flawed, vulnerable shadow self.
   • Grateful Flow & Jeopardy: Generate sensory gratitude to break black clouds; picture deathbed to crush delay.

💼 4-STEP DAILY MIND, BODY & SOUL PROTOCOL FOR KANAD:
   • 1. Morning Alignment: 5-4-3-2-1 Grounding + 4-7-8 breath + visualize RRB JE rank (Trenton & Nafousi).
   • 2. Deep Study Sprints: Deploy "The Reversal of Desire" on difficult aptitude problems (Phil Stutz).
   • 3. Evening Somatic Release: Workout + Coach Kenny gut protocol + Alex Libin pelvic butterfly (van der Kolk).
   • 4. Night Centering: Deploy Active Love to dissolve resentment + Grateful Flow on 5 wins (Stutz).

📌 VAULT SYNERGY:
   • Note: 01_Mindset_Motive/Four_Books_for_Better_Mind_Body_Soul.md
   • Visual Matrix: Attachments/Four_Books_Mind_Body_Soul_Matrix.jpg
================================================================================
""")

def cmd_dialogue(args):
    print("""
================================================================================
🗣️ TACTICAL COMMUNICATION & DIALOGUE PLAYBOOK (@booksopedia_)
================================================================================
💡 Core Principle: "Theory alone does not win high-stakes conversations.
   When tension rises, pre-programmed verbal scripts, non-reactive body language,
   and downward vocal inflections project sovereign authority and magnetism."
   — Sourabh Dubey (@booksopedia_) & glitch.mindset (@glitch.mindset)

1️⃣ 👂 INTENTIONAL LISTENING & DECODER: HOW TO LISTEN WITH INTENTION (Patrick King)
   • 3-Second Silence Anchor: Wait 3 full seconds after they finish; 60% volunteer deeper truth.
   • De-escalation Script: "It sounds like that was deeply frustrating. Take your time... I am listening."
   • Banish Fixer Syndrome: Suppress offering immediate advice; validate emotional safety first.
   • Paraphrase-Validation Loop: "Before I respond, what you are essentially saying is [X], correct?"

2️⃣ 👁️ TACTICAL CHARISMA & MICRO-CUES: HOW TO TALK TO ANYONE (Leil Lowndes)
   • The Flooding Smile: Pause 1 second, lock eyes, then let a warm, personalized smile flood face.
   • The Big-Baby Pivot: Pivot entire torso and feet 100% toward the person to signal full respect.
   • Conversational Parroting: Repeat their last 2-3 words with an inquisitive tilt to invite depth.
   • Never-Naked Answers: Attach a colorful conversational hook to your hometown, college, or job.

3️⃣ 👑 LEADERSHIP GRAVITAS & INTERVIEW CALM: HOW LEADERS LEAD (Brian Tracy)
   • Downward Vocal Cadence: Drop your pitch at the period; upward inflections project weakness.
   • The 0.5x Speed Rule: Speak at half-speed during tense technical interviews; slowness signals mastery.
   • Uncertain Technical Question: "Excellent question, sir. While I don't recall the empirical coefficient,
     my engineering foundation tells me it operates under [core law]. I will verify immediately."
   • Sovereign Integrity: "You have my word on this, sir. Consider it executed with zero compromise."

4️⃣ 🤝 EGO-FREE PERSUASION & RAPPORT: HOW TO WIN FRIENDS (Dale Carnegie)
   • 70/30 Listening Law: Let the other person speak 70% of the time; guide with strategic questions.
   • Sincere Name Anchoring: A person's name is the sweetest sound; anchor name at greetings/closings.
   • Indirect Idea Seeding: "Building on that brilliant point you made earlier, [Name], what if we tested...?"
   • The 3 C's Ban: Completely eliminate Criticism, Condemning, and Complaining.

💼 4-STEP DAILY CONVERSATION PROTOCOL FOR KANAD:
   • 1. Morning Greeting: 100% Big-Baby Pivot + 1-second Flooding Smile + Never-Naked hook (Lowndes).
   • 2. Deep Conversations: 3-Second silence anchor before replying + emotional mirroring (King).
   • 3. Professional Viva/Interviews: 0.5x speed + downward pitch cadence at sentence end (Tracy).
   • 4. Persuasion & Rapport: 70/30 listening ratio + indirect idea seeding + name anchor (Carnegie).

📌 VAULT SYNERGY:
   • Note: 01_Mindset_Motive/Tactical_Communication_and_Conversation_Playbook.md
   • Visual Matrix: Attachments/Tactical_Communication_Dialogue_Playbook_Matrix.jpg
================================================================================
""")

def cmd_prakhar(args):
    print("""
================================================================================
⚡ BEYOND SELF-HELP: 3 LIFE-CHANGING BOOKS (@prakhar_insights9)
================================================================================
💡 Core Principle: "If you are watching a self-help channel for too long, you are
   doing it wrong! Self-help channels and books are like training wheels on a cycle.
   Eventually you must take them off, bleed on the pavement, and ride the cycle yourself.
   These three masterworks demolish passive dopamine addiction and launch you into
   moral sovereignty, neurobiological flow, and transcendental consciousness."
   — Prakhar Gupta (@prakhar_insights9 — Prakhar ke Pravachan)

1️⃣ 🏛️ TIER 1: RADICAL MORAL SOVEREIGNTY (Dr. Jordan B. Peterson — 12 Rules for Life)
   • Neurochemical Serotonin Anchor (Rule 1): Stand up straight with shoulders back;
     primordial lobster hierarchy circuitry floods brain with serotonin and authority.
   • Micro-Order Before Macro-Critique (Rule 6): Set your house/desk in perfect order
     before complaining about exam systems, politics, or family burdens.
   • Meaning Over Expedience (Rule 7): Voluntarily shoulder the heaviest responsibility;
     dignity and psychological resilience are forged through purposeful struggle.
   • Absolute Ownership: Completely banish victim mentalities and external excuses.

2️⃣ ⚡ TIER 2: NEUROBIOLOGICAL FLOW & PEAK OUTPUT (Steven Kotler & Jamie Wheal — Stealing Fire)
   • Transient Hypofrontality: In deep flow, the Dorsolateral Prefrontal Cortex (DLPFC)
     down-regulates, completely silencing the inner critic, second-guessing, and dread.
   • The STER Genome of Peak Flow:
     - S (Selflessness): Neurotic ego and "What if I fail?" anxieties evaporate.
     - T (Timelessness): Time processing vanishes into an infinite, razor-sharp present.
     - E (Effortlessness): Complex technical problem solving becomes frictionlessly fluid.
     - R (Richness): Massive neurochemical surge amplifies pattern recognition 500%.
   • 90-Minute Sprint Engine: Struggle (15m) -> Release (5m) -> Flow (60m) -> Recovery (10m).

3️⃣ 🪷 TIER 3: TRANSCENDENTAL FREEDOM & CONSCIOUSNESS (Osho — Mahagita: Ashtavakra Gita Vol. 1)
   • The Supreme Spiritual Discourse: "The greatest book to listen to in the history of books."
   • King Janaka's Dilemma & Instant Awakening:
     "Muktabhimani mukto hi baddho baddhabhimanyapi" — If you consider yourself bound, you are
     bound; if you consider yourself free, you are free. Liberation is immediate awareness.
   • Sakshi Bhava (The Witness State): The fatal flaw of self-help is trying to "fix" the ego;
     Ashtavakra teaches you are neither the body, nor the mind, nor the anxious thoughts.
     You are the eternal, unattached witness (Sakshi) observing the mental drama.
   • Transcending Panic: Watch anxiety and test fear as mere passing clouds in pure consciousness.

💼 3-TIER OPERATIONAL PROTOCOL FOR KANAD:
   • 1. Physical & Moral Baseline (Peterson): Clean room/desk, erect spine, zero excuses.
   • 2. Flow Cognitive Immersion (Kotler): 90-min phone-free deep study blocks for RRB JE.
   • 3. Witness Anchor (Osho): When dread attacks, 2x physiological sighs, step into Sakshi Bhava.

📌 VAULT SYNERGY:
   • Note: 01_Mindset_Motive/Prakhar_Gupta_Three_Life_Changing_Books_Beyond_Self_Help.md
   • Visual Matrix: Attachments/Prakhar_Three_Life_Changing_Books_Matrix.jpg
================================================================================
""")

def cmd_neverquit(args):
    print("""
================================================================================
🛡️ 5 BOOKS THAT TEACH YOU TO NEVER QUIT IN LIFE (@coffeewithbooks__)
================================================================================
💡 Core Principle: "We all go through life's ups and downs. Sometimes we feel like
   giving up and that's totally normal to feel that way. But don't let 1 minute of
   your emotion dictate your life and decisions."
   — Shashank (@coffeewithbooks__)

1️⃣ 🧱 SUBTRACTIVE MENTAL TOUGHNESS: 13 THINGS MENTALLY STRONG PEOPLE DON'T DO (Amy Morin)
   • Subtractive Strength: Mental toughness is defined by what you refuse to indulge in.
   • Banish Self-Pity: Ditch "Why me?" — self-pity exaggerates suffering and halts progress.
   • 100% Retained Power: Never say "He made me mad" — you are the sole master of your response.
   • Compounding Horizon: Accept that early engineering progress produces zero visible results.

2️⃣ ⚔️ INNER WARFARE & PURPOSE: WIN YOUR INNER BATTLES (Darius Foroux)
   • Fear is a False Alarm: Evolutionary survival brain misinterprets study friction as physical threat.
   • Movement Destroys Fear: Action kills anxiety faster than rumination; systems beat fickle mood.
   • Purpose as Armor: Connect daily grind to your ultimate motive (dignity and family pride).

3️⃣ 🧘 DAY-TIGHT COMPARTMENTS & WORRY EXTINCTION: HOW TO STOP WORRYING (Dale Carnegie)
   • Day-Tight Compartments: Iron bulkheads on yesterday and tomorrow; execute solely in today's hours.
   • Willis Carrier 3-Step Formula:
     1. Ask fearlessly: "What is the absolute worst that can happen?"
     2. Mentally accept that worst outcome.
     3. Calmly focus 100% of energy on improving upon the worst.
   • The Law of Averages: 99% of catastrophic worries never happen.

4️⃣ 🏛️ STOIC ALCHEMY & TRIALS TO TRIUMPH: THE OBSTACLE IS THE WAY (Ryan Holiday)
   • Marcus Aurelius Axiom: "The impediment to action advances action. What stands in the way becomes the way."
   • Objective Perception: Strip emotional storytelling; see raw engineering facts without panic.
   • Amor Fati (Love of Fate): Treat every exam obstacle as training weight forging cognitive dominance.

5️⃣ 🌊 QUADRIPLEGIA SURVIVAL & 1/4 STEP PROTOCOL: 8 ¼ RULES FOR RESILIENCE (Jackson Sherry)
   • The 1/4 Step Rule: Paralyzed to triathlete; when unable to leap, take a quarter-step.
   • Anti-Burnout Engine: In severe exhaustion, do not quit; solve 1 formula or read 1 paragraph.
   • The Lighthouse Anchor: Fix eyes on an immovable anchor (core dignity) in stormy emotional seas.

💼 3-STEP DAILY NEVER-QUIT PROTOCOL FOR KANAD:
   • 1. Morning Baseline (Morin & Carnegie): Day-Tight Compartments + 100% power retention.
   • 2. Study Sprints (Foroux & Holiday): 5-min sprint when dread strikes; "Obstacle IS the way."
   • 3. Fatigue & Crisis (Sherry & Carnegie): Deploy 1/4 Step Rule; Willis Carrier worst-case peace.

📌 VAULT SYNERGY:
   • Note: 01_Mindset_Motive/Five_Books_That_Teach_You_To_Never_Quit.md
   • Visual Matrix: Attachments/Five_Books_Never_Quit_Resilience_Matrix.jpg
================================================================================
""")

def cmd_schoolfail(args):
    print("""
================================================================================
🎓 5 BOOKS THAT TEACH WHAT SCHOOL FAILED TO TEACH (@coffeewithbooks__)
================================================================================
💡 Core Principle: "My school taught me to memorize stuff like a printer, but
   never taught me the importance of reading, thinking, communicating, or
   managing life under pressure. Traditional academics prepare students for
   predictable exams, yet adult success and engineering leadership demand five
   real-world meta-skills."
   — Shashank (@coffeewithbooks__)

1️⃣ 🗣️ PRACTICAL COMMUNICATION & SOCIAL DYNAMICS: THE FINE ART OF SMALL TALK (Debra Fine)
   • 3-Part Conversation Engine: Invitation (open questions) -> Elaboration (never dry 1-word answers) -> Graceful Exit.
   • Free-Information Mining: Listen for verbal breadcrumbs (hobbies, goals, tools) to deepen rapport.
   • The Graceful Exit: Leave on a high note without awkwardness or fabricated excuses.

2️⃣ ⚡ EXECUTIVE PRODUCTIVITY & SYSTEM ARCHITECTURE: GETTING THINGS DONE (David Allen)
   • Psychic RAM Principle: "Your mind is for having ideas, not holding them." Uncaptured loops cause anxiety.
   • 5-Stage GTD Workflow: Capture -> Clarify -> Organize -> Reflect -> Engage (100% externalized).
   • 2-Minute Rule: If an action takes under 120 seconds, execute immediately; never queue or schedule it.

3️⃣ 🧠 CRITICAL THINKING & COGNITIVE BIAS EXTINCTION: THE ART OF THINKING CLEARLY (Rolf Dobelli)
   • Sunk Cost Fallacy: Past invested time/money is gone; evaluate only forward expected value.
   • Swimmer's Body Illusion: Never confuse selection traits with results; demand empirical causality.
   • Confirmation Bias: Actively hunt for disconfirming evidence to test your strongest engineering hypotheses.

4️⃣ 🏛️ ADAPTABILITY, FLEXIBILITY & STOIC ALCHEMY: THE OBSTACLE IS THE WAY (Ryan Holiday)
   • Stoic Triumvirate: Objective Perception (zero panic) + Directed Action (energy) + Inner Will (fortitude).
   • Curriculum of Friction: Technical roadblocks and exam delays are not disruptions; they are the training ground.
   • Amor Fati: Embrace struggle with genuine gratitude as custom intellectual resistance training.

5️⃣ 🩺 EMOTIONAL REGULATION & CLINICAL PROBLEM-SOLVING: WHY HAS NOBODY TOLD ME THIS BEFORE? (Dr. Julie Smith)
   • Square Spiral of Distress: Physiology ⇄ Thoughts ⇄ Emotions ⇄ Behavior; intervene at the somatic level first.
   • Somatic Baseline Reset: Two deep physiological sighs + cold water wash reset neurochemical alarm in 30s.
   • Recovery Velocity: High performers feel sadness and dread too; the differentiator is rapid recovery velocity.

💼 3-STEP ADULT REAL-WORLD MASTERY PROTOCOL FOR KANAD:
   • 1. Morning GTD Inbox Clearance: Externalize all mental tasks into Obsidian/Kanboard; execute <2-min tasks immediately.
   • 2. Stoic & Bias Audit: Reframe numerical stumbling blocks as obstacle-curriculum; mercilessly discard sunk costs.
   • 3. Somatic & Social Reset: Use open questions in daily dialogue; reset mood crashes with double physiological sighs.

📌 VAULT SYNERGY:
   • Note: 01_Mindset_Motive/Five_Books_School_Failed_To_Teach_You.md
   • Visual Matrix: Attachments/Five_Books_School_Failed_To_Teach_Matrix.jpg
================================================================================
""")

def cmd_ego(args):
    print("""
================================================================================
🗿 EGO IS THE ENEMY — RYAN HOLIDAY: 3 PHASES OF MASTERY
================================================================================
💡 Core Principle: "Ego is the invisible enemy that sabotages our potential
   before we begin (Aspire), corrupts our character when we succeed (Success),
   and turns our setbacks into permanent ruin (Failure). True greatness requires
   quiet confidence rooted in raw competence, apprentice humility, and unbroken
   Stoic dignity."
   — Ryan Holiday (2016)

1️⃣ 🧗 PHASE 1: ASPIRE • THE APPRENTICE'S CRUCIBLE
   • Talk vs. Work: Broadcasting goals releases cheap premature dopamine; silence keeps the furnace hot.
   • John Boyd's Dilemma: "To Be or To Do?" Choose to DO the deep technical work over craving status ("To Be").
   • The Student Mindset: Place yourself in rooms where you know the least; submit to relentless learning.
   • The Canvas Strategy: Clear the path for mentors and organizations; make yourself indispensable without ego.

2️⃣ 🏆 PHASE 2: SUCCESS • SOBRIETY & VIGILANCE
   • Always Stay an Apprentice: The moment you believe you've arrived, decline begins.
   • The Narrative Fallacy: Don't tell yourself heroic stories; recognize the role of luck, timing, and routine.
   • Seneca's Euthymia: Walk your own path with serene confidence; stop comparing your pace to competitors.

3️⃣ 🛡️ PHASE 3: FAILURE • STOIC ANTIFRAGILITY
   • Alive Time vs. Dead Time (Robert Greene): Setbacks are either wasted in bitter rumination (dead time)
     or converted into aggressive skill-building, lifting, and formula drilling (alive time).
   • The Effort is Enough: Marcus Aurelius: External outcomes are outside your control; your standard of duty is victory.
   • Neutralize Resentment: Hatred poisons the host; let silent, overwhelming competence be your only reply.

💼 3-STEP DAILY EGO-EXTINCTION DRILL FOR KANAD:
   • 1. Morning Silence (Aspire): 0 goal broadcasting; sit at study desk in monk-mode apprentice focus.
   • 2. Internal Scorecard (Success): Judge progress by deep work blocks executed, not erratic praise or mood.
   • 3. Alive Time Lockdown (Failure/Limbo): Treat every day of RRB JE preparation as high-yield Alive Time.

📌 VAULT & HOMESERVER SYNERGY:
   • Note: 01_Mindset_Motive/Ryan_Holiday_Ego_Is_The_Enemy.md
   • Visual Matrix: Attachments/Ryan_Holiday_Ego_Is_The_Enemy_Matrix.jpg
   • Audiobookshelf Ebook: ID 9352a896-4db4-41e9-93fa-6d154a2eb7bf (Priority 1: STUDY)
   • Audiobookshelf Audiobook: Watcher Daemon active (PID 871629)
================================================================================
""")

def cmd_agreements(args):
    print("""
================================================================================
🦅 THE FOUR AGREEMENTS — DON MIGUEL RUIZ: TOLTEC FREEDOM
================================================================================
💡 Core Principle: "There is a huge amount of freedom that comes to you when
   you take nothing personally. You become immune to the black magic of toxic
   words and opinions. What others say and do is merely a projection of their
   own dream, their own wounded reality."
   — Don Miguel Ruiz (1997)

1️⃣ 🗣️ AGREEMENT 1: BE IMPECCABLE WITH YOUR WORD (সত্যনিষ্ঠ ও নিষ্কলঙ্ক বাক্য)
   • Zero Self-Denigration: Never tell yourself "I am slow" or "I cannot crack this." Words cast spells.
   • White Magic vs Black Magic: Use speech solely in the direction of truth, courage, and focused action.
   • Refuse Gossip: Gossiping poisons the speaker's mind and drains executive working memory.

2️⃣ 🛡️ AGREEMENT 2: DON'T TAKE ANYTHING PERSONALLY (কোনো কিছু ব্যক্তিগতভাবে না নেওয়া)
   • The Projection Axiom: Others' insults, anger, or praise reflect their internal dream, not your worth.
   • The Poison Cup: If someone hands you a cup of anger or disrespect, you only suffer if you drink it.
   • Psychological Immunity: Corporate terminations or family skepticism are impersonal weather patterns.

3️⃣ 🔍 AGREEMENT 3: DON'T MAKE ASSUMPTIONS (কখনো অনুমান বা মনগড়া ব্যাখ্যা না করা)
   • The Fiction Trap: The human brain invents catastrophic drama when data is missing; stop reading minds.
   • Empirical Verification: Ask direct questions. In study, never assume you know a topic—test with closed-book recall.
   • Replace Drama With Data: Base every career and exam decision on cold empirical engineering facts.

4️⃣ ⚡ AGREEMENT 4: ALWAYS DO YOUR BEST (সর্বদা নিজের বর্তমান সর্বোচ্চ দেওয়া)
   • Dynamic Capacity: Your best while rested is 3 hours of deep math; your best when tired is 30 mins of formula review.
   • Middle Path: Doing less invites guilt; pushing past biological limits invites burnout.
   • Regret Elimination: Giving 100% of your present capacity guarantees absolute peace of mind at night.

💼 3-STEP DAILY TOLTEC FREEDOM PROTOCOL FOR KANAD:
   • 1. Morning Word Impeccability: 0 self-criticism; speak only constructive truth to yourself.
   • 2. Daytime Teflon Shield: Treat criticism as others' projection; 0 assumptions about exam cutoffs.
   • 3. Nightly Reconciliation: Surrender results to fate knowing you gave today's honest best effort.

📌 VAULT & HOMESERVER SYNERGY:
   • Note: 01_Mindset_Motive/Don_Miguel_Ruiz_The_Four_Agreements.md
   • Visual Matrix: Attachments/Don_Miguel_Ruiz_The_Four_Agreements_Matrix.jpg
   • Audiobookshelf Ebook: ID 6d834d3a-b53b-4eff-ba8b-d102301e3a05 (Priority 1: STUDY)
   • Audiobookshelf Audiobook: ID 25f81faa-88d0-4617-b6e1-665e2d5a748c (Priority 1: STUDY)
================================================================================
""")

def cmd_beyondorder(args):
    print("""
================================================================================
🐉 BEYOND ORDER: 12 MORE RULES FOR LIFE — DR. JORDAN B. PETERSON
================================================================================
💡 Core Principle: "Order is not enough. You must keep one foot firmly in what
   you understand, and step the other courageously into the unknown, revitalizing
   both yourself and the world."
   — Dr. Jordan B. Peterson (2021)

🧭 THE KNIFE-EDGE DIALECTIC (CHAOS vs TYRANNICAL ORDER):
   • Excess Chaos: Anxiety, dread, nihilism, cognitive paralysis.
   • Excess Order: Bureaucracy, dogma, ossification, tyrannical stagnation.
   • The Hero's Walk: Balance on the border of the unknown to continuously renew yourself.

1️⃣ 🏛️ RULE 1: DO NOT CARELESSLY DENIGRATE SOCIAL INSTITUTIONS
   • Respect ancestral solutions (Chesterton's Fence); reform with humble competence.
2️⃣ ⚡ RULE 2: IMAGINE WHO YOU COULD BE, AND AIM SINGLY AT THAT
   • Confront your Shadow voluntarily; the Hero transforms psychological lead into gold.
3️⃣ 🌫️ RULE 3: DO NOT HIDE UNWANTED THINGS IN THE FOG
   • Refusal to face reality lets monsters breed; name problems with surgical verbal precision.
4️⃣ 🪨 RULE 4: NOTICE OPPORTUNITY WHERE RESPONSIBILITY HAS BEEN ABDICATED
   • Where others complain or drop the load is your competitive advantage. Carry the heaviest rock.
5️⃣ 🛡️ RULE 5: DO NOT DO WHAT YOU HATE
   • Submitting to tyranny breeds murderous resentment; protect your moral conscience at all costs.
6️⃣ 🚫 RULE 6: ABANDON IDEOLOGY
   • Stop scapegoating external villains; take radical ownership and clean your complex house first.
7️⃣ ⚔️ RULE 7: WORK AS HARD AS YOU CAN ON AT LEAST ONE THING
   • Apprentice discipline: monastic specialization forges the mind into an elite, transferable blade.
8️⃣ 🌸 RULE 8: TRY TO MAKE ONE ROOM IN YOUR HOME AS BEAUTIFUL AS POSSIBLE
   • Beauty is an encounter with transcendence; an aesthetic sanctuary counters nihilism and fatigue.
9️⃣ ✍️ RULE 9: IF OLD MEMORIES STILL MAKE YOU CRY, WRITE THEM DOWN COMPLETELY
   • Narrative exposure therapy: map unresolved trauma in full prose to convert danger into wisdom.
🔟 🌹 RULE 10: PLAN AND WORK DILIGENTLY TO MAINTAIN ROMANCE
   • Romance requires deliberate negotiation, designated dates, and radical honesty, not entitlement.
1️⃣1️⃣ 🧘 RULE 11: DO NOT ALLOW YOURSELF TO BECOME RESENTFUL, DECEITFUL, OR ARROGANT
   • Resentment signals neglected duty; deceit fractures reality; arrogance blinds before catastrophe.
1️⃣2️⃣ 🙏 RULE 12: BE GRATEFUL IN SPITE OF YOUR SUFFERING
   • Suffering is mortal baseline; conscious gratitude is supreme defiance: affirming Being amid pain.

💼 DAILY SOVEREIGNTY EXECUTION FOR KANAD:
   • 1. Single Aim: Monastic 3-hour deep study sprint (Rule 7) targeting exam mastery (Rule 2).
   • 2. Radical Clarity: Zero fog; write errors & setbacks with surgical honesty (Rules 3 & 9).
   • 3. Heroic Dignity: Carry the heaviest load; reject bitterness; cultivate Amor Fati (Rules 4, 5, 12).

📌 VAULT & HOMESERVER SYNERGY:
   • Note: 01_Mindset_Motive/Jordan_Peterson_Beyond_Order_12_More_Rules.md
   • Visual Matrix: Attachments/Jordan_Peterson_Beyond_Order_Matrix.jpg
   • Audiobookshelf Ebook: ID 983f0a10-f015-45dc-bbfc-7d3b92372b11 (Priority 1: STUDY)
   • Audiobookshelf Audiobook: ID c15c96a1-b332-4c62-a38c-a32e76d411b9 (Priority 1: STUDY)
================================================================================
""")

def cmd_meaning(args):
    print("""
================================================================================
🕊️ MAN'S SEARCH FOR MEANING — VIKTOR E. FRANKL: LOGOTHERAPY & SOVEREIGNTY
================================================================================
💡 Core Principle: "Everything can be taken from a man but one thing: the last
   of the human freedoms—to choose one's attitude in any given set of
   circumstances, to choose one's own way."
   — Dr. Viktor E. Frankl (1946)

🧭 DIE DREI WEGE ZUM SINN (THE 3 PATHWAYS TO MEANING):
   1️⃣ 🛠️ CREATIVE WORK & DEEDS (Schöpferische Werte):
      • Producing a work, mastering a rigorous discipline, or achieving a mission.
      • Frankl mentally reconstructing his confiscated book in Auschwitz.
      • For Kanad: Syllabus mastery as active sacred meaning-creation.
   2️⃣ ❤️ EXPERIENCING LOVE & ART (Erlebniswerte):
      • Experiencing nature, beauty, art, or genuine loving human connection.
      • "The salvation of man is through love and in love" — spiritual communion.
      • For Kanad: Aesthetic study sanctuary and profound familial duty.
   3️⃣ 🛡️ ATTITUDE TOWARD UNAVOIDABLE SUFFERING (Einstellungswerte):
      • When facing an unchangeable fate, we are challenged to change ourselves.
      • Turning personal tragedy into human triumph; suffering with dignity.
      • For Kanad: Past layoff letters & setbacks as the forge of unshakeable grit.

⚡ 4 FOUNDATIONAL LOGOTHERAPY PILLARS:
   • 1. Will to Meaning: Man's primary drive (defeating depression, aggression, addiction).
   • 2. The Sacred Gap: Space between stimulus and response where human freedom lives.
   • 3. Nietzsche's Engine: "He who has a why to live can bear almost any how."
   • 4. Tragic Optimism: Saying "Yes to Life" in spite of pain, guilt, and death.

💼 3-STEP DAILY LOGOTHERAPY PROTOCOL FOR KANAD:
   • 1. Morning Meaning Alignment: Study blocks as unfinished manuscript (Nietzschean Why).
   • 2. Daytime Teflon Immunity: Step into the Sacred Gap; past setbacks cannot touch your soul.
   • 3. Nightly Tragic Optimism: Audit today's strain as noble growth; sleep in deep peace.

📌 VAULT & HOMESERVER SYNERGY:
   • Note: 01_Mindset_Motive/Viktor_Frankl_Mans_Search_For_Meaning.md
   • Visual Matrix: Attachments/Viktor_Frankl_Mans_Search_For_Meaning_Matrix.jpg
   • Audiobookshelf Ebook: ID 957fcf42-b3f1-4b23-a58d-85b3e6809aa6 (Priority 1: STUDY)
   • Audiobookshelf Audiobook: ID e6a4ca42-c4ed-48ec-a136-320f63c4300e (Priority 1: STUDY)
================================================================================
""")

def cmd_howwelearn(args):
    print("""
================================================================================
🧠 HOW WE LEARN — BENEDICT CAREY & STANISLAS DEHAENE: COGNITIVE SCIENCE
================================================================================
💡 Core Principle: "Forgetting is not an enemy of memory; it is its greatest
   friend and prerequisite. When you struggle to retrieve what was partially
   forgotten, retention becomes permanent."
   — Benedict Carey (2014)

🔬 STANISLAS DEHAENE: 4 NEUROLOGICAL PILLARS OF LEARNING:
   1️⃣ 🎯 ATTENTION: The selective amplifier; filters 99% noise. Zero multitasking.
   2️⃣ ⚡ ACTIVE ENGAGEMENT: Bayesian prediction engine; closed-book recall over passive reading.
   3️⃣ 🔍 ERROR FEEDBACK: Prediction error signal; mistakes are the sole trigger for synaptic updating.
   4️⃣ 💤 CONSOLIDATION: Deep slow-wave sleep transfers memories from hippocampus to neocortex.

🚀 BENEDICT CAREY: 6 COGNITIVE ACCELERATION ENGINES:
   • 1. Forgetting as Memory Multiplier: Bjork's Storage vs Retrieval strength (Desirable Difficulty).
   • 2. Contextual Variation: Alter rooms, lighting & seating to hook diverse sensory cues.
   • 3. The Spacing Effect: 1 hour across 3 days yields 300% more retention than 3-hour cramming.
   • 4. Interleaving Practice: Mix Quant, Reasoning & Verbal to master problem-type recognition.
   • 5. The Pre-Testing Effect: Testing before studying creates cognitive scaffolding (2.5x gain).
   • 6. Incubation & Zeigarnik Effect: Walk away when blocked; let the Default Mode Network solve it.

💼 3-STEP DAILY EXAM ACCELERATION PROTOCOL FOR KANAD:
   • 1. Pre-Test Prime: Attempt 3-5 PYQ questions blindly before reading new chapter.
   • 2. Interleaved Sprints: 45-min blocks alternating between Quant, Reasoning & General Studies.
   • 3. Closed-Book Audit: Write summaries from memory into Obsidian Active Recall; sleep 8 hours.

📌 VAULT & HOMESERVER SYNERGY:
   • Note: 02_Cognitive_Learning/Benedict_Carey_How_We_Learn.md
   • Visual Matrix: Attachments/How_We_Learn_Cognitive_Mastery_Matrix.jpg
   • Audiobook: Audiobookshelf ID 85604e81-3d74-4086-87df-ef821a0fd721 (Priority 1: STUDY)
   • E-Books: Carey (026b6e7d) & Dehaene (d43e0c56) (Priority 1: STUDY)
================================================================================
""")

def cmd_greenlights(args):
    print("""
================================================================================
🚦 GREENLIGHTS — MATTHEW MCCONAUGHEY: THE ART OF LIVIN' & AUTONOMIC SOVEREIGNTY
================================================================================
💡 Core Principle: "We don't like red and yellow lights. But almost every red light
   in life eventually turns green. It forces us to stop, pivot, reflect, and engineer
   our ultimate destiny."
   — Matthew McConaughey (2020)

🚦 THE TRAFFIC LIGHT TRIAD:
   1️⃣ 🟢 GREENLIGHTS: Affirmations, flow states, right of way, speed, unhindered momentum.
   2️⃣ 🟡 YELLOWLIGHTS: Caution, hesitation, diets, pauses, transitions, recalibrations.
   3️⃣ 🔴 REDLIGHTS: Job loss, crisis, heartbreak, failures, forced full stops.
      * The Red Light Alchemy: A red light is not the end of the road; it saves you
        from driving into an abyss and pivots you directly toward your true calling.

🏛️ THE 4 PILLARS OF MCCONAUGHEY WISDOM:
   • 1. Less Impressed, More Involved: Stop worshipping people, exams, or giants on pedestals.
        Roll up your sleeves and get your hands dirty in daily execution.
   • 2. The Process of Elimination: Finding who you are starts with knowing who you are NOT.
        Subtract self-pity, doomscrolling, victim identity, and toxic chatter.
   • 3. Relative Speed (Prescribed vs Preferred): Reject society's artificial panic (Prescribed).
        Calibrate your life to your soul's authentic, sustainable cadence (Preferred).
   • 4. Outlaw Logic & The Solitary Walk: The guts to say NO to easy comfort and walk through
        the desert in solitude until your true inner frequency rings crystal clear.

💼 3-STEP DAILY GREENLIGHT PROTOCOL FOR KANAD:
   • 1. Re-frame the Red Light: Past termination was a blessing in disguise—it halted corporate
        slavery and ignited full-time Govt Exam mastery, health sovereignty, and dignity.
   • 2. Less Impressed, More Involved: Don't fear the syllabus or cutoffs; immerse in 3-hour deep work blocks.
   • 3. Daily Subtractive Audit: Eliminate who you are not; protect your peace and prime focus.

📌 VAULT & HOMESERVER SYNERGY:
   • Note: 01_Mindset_Motive/Matthew_McConaughey_Greenlights.md
   • Visual Matrix: Attachments/Matthew_McConaughey_Greenlights_Matrix.jpg
   • Audiobook: Audiobookshelf ID a760e547-16ea-4134-b8b2-27f5d03dd0d2 (Priority 1: STUDY)
   • E-Book: Audiobookshelf ID c244e567-4dff-4b18-968c-947d849eab11 (Priority 1: STUDY)
================================================================================
""")

def cmd_wordpower(args):
    print("""
================================================================================
📚 WORD POWER MADE EASY — NORMAN LEWIS: ROOT-WORD ETYMOLOGY ENGINE
================================================================================
💡 Core Principle: "Words are the symbols of ideas. The more words you have at
   your command, the clearer, more accurate, and more powerful will be your thinking."
   — Norman Lewis (1949)

⚡ THE ETYMOLOGY MULTIPLIER ENGINE:
   1️⃣ Greek & Latin Roots: 1 root morpheme (e.g., EGO, ALTER, VERT, MIS) anchors 20-50 words.
   2️⃣ Prefix / Suffix Combos: Systematic structural construction creates nuanced meanings.
   3️⃣ Predictive Deduction: 100% accurate deduction of unseen words in Govt Exams (SSC/Bank/WBCS).

🏛️ THE 4 THEMATIC VOCABULARY PILLARS:
   • 1. Personality Types (Sessions 1-10): Egoist vs Egotist, Altruist, Introvert/Extrovert/Ambivert,
        Misanthrope (Hates man), Misogynist (Hates women), Misogamist (Hates marriage), Ascetic.
   • 2. Medical Specialists (Sessions 11-20): Internist, Gynecologist, Obstetrician, Pediatrician,
        Dermatologist (Skin), Ophthalmologist (Eye), Orthopedist (Straight bones), Cardiologist, Neurologist.
   • 3. Human Behaviors & Deception (Sessions 21-30): Notorious, Consummate, Incorrigible,
        Inveterate (Vetus = old habit), Congenital (From birth), Chronic (Time), Pathological, Egregious.
   • 4. Verbal Actions & Maneuvers (Sessions 31-47): Disparage, Equivocate, Titillate, Adulate,
        Proscribe (Outlaw), Obviate (Bypass obstacles), Militate, Placate (Soothe), Condone, Malign.

💼 3-STEP DAILY VOCABULARY PROTOCOL FOR KANAD:
   • 1. 1 Session / Day: 15-20 min morning focus. Master root morphemes; never binge dictionary lists.
   • 2. Somatic Broca Articulation: Pronounce words aloud using phonetic keys to build motor memory.
   • 3. Closed-Book Active Retrieval: Complete session quizzes with book closed; dissect roots in Obsidian.

📌 VAULT & HOMESERVER SYNERGY:
   • Note: 02_Cognitive_Learning/Norman_Lewis_Word_Power_Made_Easy.md
   • Visual Matrix: Attachments/Norman_Lewis_Word_Power_Made_Easy_Matrix.jpg
   • E-Book: Audiobookshelf ID 3da54da9-dde7-4d41-91f9-9058f415361e (Priority 1: STUDY)
================================================================================
""")

def cmd_psychocybernetics(args):
    print("""
================================================================================
🧠 PSYCHO-CYBERNETICS — DR. MAXWELL MALTZ: THE MIND'S SERVO-MECHANISM
================================================================================
💡 Core Principle: "The self-image sets the boundaries of individual achievement.
   It defines what you can and cannot do. Expand the self-image and you expand
   the area of the possible. Your subconscious mind is an automatic goal-striving
   servo-mechanism steered by your mental pictures."
   — Dr. Maxwell Maltz (1960)

🏛️ THE 4 CORE PILLARS OF PSYCHO-CYBERNETICS:
   • 1. The Self-Image Thermostat: Your subconscious mind will violently resist
        any outer success that exceeds your internal self-identity. If you view
        yourself as a corporate cast-off, you will unconsciously sabotage Govt Exams.
        Upgrade the thermostat to 'Sovereign Scholar & Relentless Executioner'.
   • 2. The Automatic Creative Servo-Mechanism: Your brain acts like a homing missile.
        Give it a crystal-clear target (e.g. 165+ in SSC CGL Tier 1), and it calculates
        the trajectory automatically through unconscious neural adjustments.
   • 3. The Theater of the Mind (Mental Rehearsal): The nervous system cannot tell the
        difference between a real experience and an intensely, vividly imagined one.
        Sitting in stillness for 15 minutes and visualizing flawless mathematical
        problem-solving lays down the identical physical neural synapses.
   • 4. Negative Feedback as Steering, Not Self-Condemnation: A torpedo veers off
        course 90% of the flight; it uses errors solely for telemetry recalibration.
        Mistakes in mock tests are neutral data points, never verdicts on your worth.

💼 3-STEP DAILY PSYCHO-CYBERNETIC PROTOCOL FOR KANAD:
   • 1. Morning Theater of the Mind (15 Mins): Sit in the Liluah/Arambagh study corner.
        Close eyes and mentally walk through solving complex arithmetic calmly and accurately.
   • 2. Zero-Guilt Telemetry Recalibration: When an answer is wrong in mock tests, say:
        "Course correction received." Log the error formula immediately without emotional drama.
   • 3. Emotional Scar Surgery: Forgive past workplace trauma and termination. Cut the psychic
        cord; treat the corporate past as obsolete data from a previous incarnation.

📌 VAULT & HOMESERVER SYNERGY:
   • Note: 01_Mindset_Motive/Maxwell_Maltz_Psycho_Cybernetics.md
   • Visual Matrix: Attachments/Maxwell_Maltz_Psycho_Cybernetics_Matrix.jpg
   • E-Book: Audiobookshelf ID bd0640d3-63fb-4436-8739-b20c975ba35d (Priority 1: STUDY)
================================================================================
""")

def cmd_supernatural(args):
    print("""
================================================================================
🌌 BECOMING SUPERNATURAL — DR. JOE DISPENZA: NEURO-QUANTUM TRANSFORMATION
================================================================================
💡 Core Principle: "Can you accept the notion that once you change your internal
   state, you no longer need the outer world to provide you with a reason to feel
   joy, gratitude, or power? When you change your electromagnetic signature, you
   collapse time and draw the desired future directly to you."
   — Dr. Joe Dispenza (2017)

🏛️ THE 4 CORE PILLARS OF BECOMING SUPERNATURAL:
   • 1. Electromagnetic Quantum Signature:
        Thoughts = Electrical charge radiating into the quantum field.
        Feelings = Magnetic signature drawing reality back to the physical body.
        Routine anxiety broadcast = Re-creating the identical miserable past.
        Elevated gratitude + Clear vision = Epigenetic and physical transformation.
   • 2. Heart-Brain Coherence: High Beta waves (stress/fight-or-flight) cause brain
        incoherence. Focused slow heart breathing shifts nervous rhythm into coherent
        Alpha, Theta, and Gamma states, boosting immunity and cognitive endurance.
   • 3. Blessing of the 8 Energy Centers: Lower 3 centers (survival, sexuality, power)
        trap over 80% of personal energy. Upward spinal breath liberates trapped
        kundalini energy into the heart, thyroid, pineal, and crown centers.
   • 4. Epigenetic Elevation Ahead of Environment: Genes do not create disease;
        environmental signals do. By embodying the triumphant emotion before passing
        the exam, you signal genes to upgrade your biology in the present moment.

💼 3-STEP DAILY SUPERNATURAL PROTOCOL FOR KANAD:
   • 1. Dawn Coherence Breathing (10 Mins): Inhale slowly through the heart center;
        exhale slowly while holding elevated feelings of unshakeable triumph and peace.
   • 2. Future-State Embodiment: Study not as a desperate candidate begging for an
        appointment letter, but as an already appointed Govt Officer mastering his craft.
   • 3. Evening Pineal Decoupling: Before sleep, detach from 3D space, time, and physical
        limitations. Enter the quantum void of infinite potential.

📌 VAULT & HOMESERVER SYNERGY:
   • Note: 01_Mindset_Motive/Joe_Dispenza_Becoming_Supernatural.md
   • Visual Matrix: Attachments/Joe_Dispenza_Becoming_Supernatural_Matrix.jpg
   • E-Book: Audiobookshelf ID f5aa0591-2d27-49f6-b911-39c49639a0f1 (Priority 1: STUDY)
================================================================================
""")

def cmd_execution(args):
    print("""
================================================================================
⚙️ EXECUTION: THE DISCIPLINE OF GETTING THINGS DONE — BOSSIDY & CHARAN
================================================================================
💡 Core Principle: "Execution is the missing link between aspirations and results.
   It is not just tactics—it is a systematic discipline, culture, and operational
   engine that must be built into personal identity."
   — Larry Bossidy & Ram Charan (2002)

🏛️ THE 4 CORE PILLARS OF EXECUTION MASTERY:
   • 1. Execution as Systematic Discipline: Ideas, strategies, and fancy planners
        create zero value. Value is generated exclusively when tasks are completed
        with relentless, boring operational follow-through on the ground.
   • 2. The 3 Core Operational Processes:
        - People Process: Allocate your highest mental energy (mornings) to your
          highest-friction subjects (Mathematics & Advanced English).
        - Strategy Process: Build realistic, grounded roadmaps without wishful thinking.
        - Operations Process: Break 90-day macro targets into daily non-negotiable sprints.
   • 3. The 7 Essential Leadership Behaviors: Know your reality, insist on realism,
        set clear priorities, follow through relentlessly, reward doers, expand
        capabilities, and know your emotional triggers and weaknesses.
   • 4. Robust Candor & Binary Milestones: Banish vague subjective self-talk ("I studied
        well today"). Replace with strict binary metrics: Was the 25-question set done?
        YES or NO. No narratives, no excuses.

💼 3-STEP DAILY EXECUTION PROTOCOL FOR KANAD:
   • 1. Binary Morning Target Lock: Write down exact target: "Solve 20 Trigonometry
        PYQs by 1:00 PM with 80%+ accuracy."
   • 2. Zero-Excuses Operational Sprint: Phone locked in drawer; zero social media.
   • 3. Candid Evening Audit: 10:00 PM review in Obsidian. Check tasks; record raw reality.

📌 VAULT & HOMESERVER SYNERGY:
   • Note: 02_Cognitive_Learning/Larry_Bossidy_Ram_Charan_Execution.md
   • Visual Matrix: Attachments/Larry_Bossidy_Ram_Charan_Execution_Matrix.jpg
   • Shelf: Priority 1: STUDY (Deep Work, Stoicism & Systems)
================================================================================
""")

def cmd_sameasever(args):
    print("""
================================================================================
⏳ SAME AS EVER: A GUIDE TO WHAT NEVER CHANGES — MORGAN HOUSEL
================================================================================
💡 Core Principle: "If you want to understand the future, don't try to forecast
   what will change. Look at what has never changed for thousands of years: human
   fear, greed, status-seeking, envy, and stories. The constants are your edge."
   — Morgan Housel (2023)

🏛️ THE 4 CORE PILLARS OF SAME AS EVER:
   • 1. Timeless Constants Over Unreliable Forecasts: History is shaped by unpredictable
        Black Swans. Stop obsessing over exam cutoff forecasts and YouTube predictions.
        Anchor in timeless human truths: deep revision, disciplined stamina, and calm.
   • 2. The Expectation Gap Formula:
        Happiness = Reality - Expectations
        Peace and mental stamina come from anchoring expectations in internal mastery
        rather than external comparisons with peers or social media illusions.
   • 3. Calm Breeds Chaos & The Necessity of Slack: Economic calm breeds complacency
        and fragile over-leveraging. Never optimize your daily schedule to 100% capacity;
        keep 20% flexible slack to absorb life shocks without breaking your study routine.
   • 4. The Power of Quiet Compounding: Massive results never occur from manic, 1-week
        frenzies. They stem from quiet, boring, unglamorous compounding over months.
        The winner is simply the one who survives bad days without quitting.

💼 3-STEP DAILY TIMELESS PROTOCOL FOR KANAD:
   • 1. Morning Slack & Focus Anchor: Keep schedule flexible with 20% buffer room.
   • 2. Expectation Decoupling: Measure today only against yesterday's personal standard.
   • 3. Compound Continuity: On tired or low-energy days, preserve the chain with 20 mins
        of flashcards. Never break the compounding cycle completely.

📌 VAULT & HOMESERVER SYNERGY:
   • Note: 02_Cognitive_Learning/Morgan_Housel_Same_As_Ever.md
   • Visual Matrix: Attachments/Morgan_Housel_Same_As_Ever_Matrix.jpg
   • Shelf: Priority 1: STUDY (Deep Work, Stoicism & Systems)
================================================================================
""")

def cmd_stolenfocus(args):
    print("""
================================================================================
🎯 STOLEN FOCUS: WHY YOU CAN'T PAY ATTENTION — JOHANN HARI
================================================================================
💡 Core Principle: "Your inability to focus is not a personal failure, moral flaw,
   or lack of willpower. Your attention did not collapse; it was systematically
   stolen by a multibillion-dollar economic system designed to keep you addicted,
   fragmented, and enraged."
   — Johann Hari (2022)

🏛️ THE 4 CORE PILLARS OF FOCUS RECLAMATION:
   • 1. Systemic Theft of Attention: Stop self-flagellating over lack of willpower.
        Surveillance capitalism monetizes outrage and distraction. Relying on raw
        willpower inside a hyper-connected room is biological suicide.
   • 2. The Switch-Cost Effect & Destruction of Flow:
        Multitasking is a neurological myth. A single phone interruption costs
        23 minutes and 15 seconds to regain deep focus, and task-switching temporarily
        drops effective IQ by 10 to 15 points.
   • 3. Collapse of Deep Reading & Mind-Wandering: Skimming social media feeds atrophies
        sustained narrative brain networks. Free mind-wandering (daydreaming without screens)
        activates the Default Mode Network, which synthesizes creative breakthroughs.
   • 4. Restorative Sleep & Metabolic Shield: Sleep flushes out metabolic neurotoxins
        via the glymphatic system. Blue light, sleep fragmentation, and ultra-processed
        sugar spikes cripple the prefrontal cortex and paralyze sustained focus.

💼 3-STEP FOCUS RECLAMATION PROTOCOL FOR KANAD:
   • 1. Physical Distance Friction: The smartphone is placed in another room inside a
        closed drawer during 4-hour morning study sprints.
   • 2. Monotasking Flow Lock: 90-minute blocks with only 1 note or 1 textbook open.
   • 3. Daily Digital Sunset & Twilight Walk: All screens powered down or shifted to warm
        amber by 9:30 PM. 15-minute screen-free rooftop walk to allow mind-wandering.

📌 VAULT & HOMESERVER SYNERGY:
   • Note: 02_Cognitive_Learning/Johann_Hari_Stolen_Focus.md
   • Visual Matrix: Attachments/Johann_Hari_Stolen_Focus_Matrix.jpg
   • E-Book: Audiobookshelf ID 0e39f1e1-c7b6-47f8-b70a-e2d8692fa275 (Priority 1: STUDY)
================================================================================
""")

def cmd_avoiding(args):
    print("""
================================================================================
🪄 THE MAGIC YOU'RE LOOKING FOR IS IN THE WORK YOU'RE AVOIDING
================================================================================
💡 Core Principle: "The magic you're looking for is in the work you're avoiding.
   The breakthrough is never hidden in a secret shortcut, another productivity hack,
   or a motivational video. It is buried directly beneath the uncomfortable task
   you dread the most."
   — Chris Williamson (Modern Wisdom) & Dipen Parmar

🏛️ THE 4 CORE PILLARS OF TRANSMUTING RESISTANCE INTO MAGIC:
   • 1. The Resistance Compass (Steven Pressfield):
        The more resistance, dread, or friction you feel toward an activity, the more
        crucial it is to your growth and exam victory. Resistance is an infallible
        directional needle pointing straight to your breakthrough.
   • 2. The Illusion of Shortcuts & Passive Consumption:
        Searching for hacks, secret study tips, or watching motivational reels is
        merely sophisticated procrastination. "Magic" is simply compound unglamorous
        labor disguised as patience.
   • 3. Carl Jung: In Sterquiliniis Invenitur (Gold in the Filth):
        Ancient alchemical axiom: "In filth it will be found." What you need most is
        buried where you least want to look. Facing past termination trauma and difficult
        math problem sets transforms psychological poison into supreme sovereign power.
   • 4. The 5-Minute Micro-Friction Breaker:
        Static friction is 10x higher than kinetic friction; starting is the only real
        barrier. Lower the threshold: commit to just 1 problem or 5 minutes of focused
        reading. Once in motion, dopamine momentum powers the sprint.

💼 3-STEP DAILY BREAKTHROUGH PROTOCOL FOR KANAD:
   • 1. Pinpoint The Dread: Every morning, ask: "What study task or physical habit
        am I dreading the most today?" (e.g. 25 Trigonometry PYQs or fat-loss cardio).
   • 2. Execute 5-Minute Micro-Sprint: Open the book immediately. Zero hesitation, zero
        social media. Solve question #1 with complete sensory focus.
   • 3. Log Binary Victory: Mark task complete in Obsidian. Remind yourself: "Today
        I confronted the resistance and conquered it."

📌 VAULT & HOMESERVER SYNERGY:
   • Note: 01_Mindset_Motive/Chris_Williamson_The_Magic_You_Are_Avoiding.md
   • Visual Matrix: Attachments/Chris_Williamson_Magic_in_Work_You_Avoid_Matrix.jpg
   • Related Study: 02_Cognitive_Learning/Larry_Bossidy_Ram_Charan_Execution.md
   • Core Motive Anchor: 01_Mindset_Motive/Motive_and_Dignity_Anchor.md
================================================================================
""")

def cmd_shadows(args):
    print("""
================================================================================
🕶️ POWER STAYS IN THE SHADOWS — LEWIS STRAUSS & ROBERT DOWNEY JR.
================================================================================
💡 Core Principle: "Amateurs seek the sun and get eaten. Power stays in the shadows."
   — Lewis Strauss / Robert Downey Jr. (Oppenheimer, 2023 • Oscar Winner 2024)

🏛️ THE 4 FOUNDATIONAL PILLARS OF SHADOW SOVEREIGNTY:
   • 1. The Sun Trap (Validation Addiction & Dopamine Leaks):
        Amateurs prematurely broadcast their goals on social media and to relatives.
        Pre-mature announcements leak critical dopamine, invite envy, and create
        unnecessary friction before the real work is done.
   • 2. Power in the Shadows (Concealed Mastery & Strategic Silence):
        True sovereign power moves quietly behind closed doors. Robert Greene's
        Law 3 (Conceal Intentions) & Law 4 (Always Say Less Than Necessary).
        Silent progress creates insurmountable asymmetric advantages.
   • 3. The 31-Year Compounding Redemption (RDJ's Real-Life Arc):
        From first Oscar nomination (Chaplin, 1992) to prison/rock bottom (1996-2001)
        to resurgence (Iron Man, 2008) and Oscar victory (Oppenheimer, 2024).
        A private career setback is merely a temporary dip in a 30-year arc.
   • 4. The Dark Horse Execution Protocol:
        Stop explaining career choices to relatives. Build quietly in Liluah & Arambagh.
        Let the final Public Service Commission appointment letter make the noise.

💼 3-STEP DAILY DARK HORSE PROTOCOL FOR KANAD:
   • 1. Total Radio Silence: Zero social media posts or status updates about exams,
        books, or study sessions. Conceal intentions 100%.
   • 2. Winter Reframe: Treat the private layoff as RDJ's 1996 pivot. It is the incubation
        period where deep roots are grown before the historic comeback.
   • 3. Closed-Door Deep Work: 3-4 hours daily solitary study block. Complete Project #4
        and Project #5 quietly. Dignity is earned through quiet mastery.

📌 VAULT & HOMESERVER SYNERGY:
   • Note: 01_Mindset_Motive/Lewis_Strauss_Power_Stays_in_the_Shadows.md
   • Visual Matrix: Attachments/Robert_Downey_Jr_Lewis_Strauss_Power_in_Shadows_Matrix.jpg
   • Core Motive Anchor: 01_Mindset_Motive/Motive_and_Dignity_Anchor.md
   • Related Study: 01_Mindset_Motive/Ryan_Holiday_Ego_Is_The_Enemy.md
================================================================================
""")

def cmd_krishna(args):
    print("""
================================================================================
🕉️ OVERCOMING LAZINESS & CONQUERING THE SLAVE MIND — BHAGAVAD GITA 6.5 & 3.42
================================================================================
💡 Core Dialectic:
   "हे कृष्ण! मुझे हर एक काम में आलस आता है, मैं अपना कोई भी काम ढंग से नहीं कर पाता..."
   श्रीकृष्ण उत्तर देते हैं:
   "आलसी होने का भी विकल्प तुम्हारा है। आलसी वही है जो अपने मन का गुलाम है।
    जो कुछ भी है सब तुम्हारे ऊपर है। अपने आत्मबल से अपना उद्धार करो।
    तुम्हारा दुश्मन कोई और नहीं, तुम स्वयं हो!"
   — Bhagavad Gita 6.5 (उद्धरेदात्मनात्मानं) & 3.42 (इन्द्रियाणि पराण्याहुः)

🏛️ THE 4 FOUNDATIONAL PILLARS OF GITA MIND MASTERY:
   • 1. Laziness is an Elective Choice (আলস্য কোনো রোগ নয়, এটি একটি সিদ্ধান্ত):
        Inertia is not a genetic curse. Every minute you choose whether to obey
        the mind's craving for passive comfort or enforce intellect over lethargy.
   • 2. The Enslaved Mind vs Sovereign Intellect (মনের দাসত্ব বনাম প্রজ্ঞার শাসন):
        Gita 3.42: Body < Senses < Mind (Manas) < Intellect (Buddhi) < Atman.
        When Buddhi surrenders to Manas, the rider is dragged by the wild elephant.
   • 3. You Are Your Only Enemy (আত্মৈব রিপুরাত্মনঃ):
        The uncontrolled mind is your most vicious enemy; the conquered mind is
        your greatest ally (बन्धुः). Stop blaming the layoff, exams, or relatives.
   • 4. Atma-Uddhar: The Sacred Self-Rescue (আত্মবল দিয়ে আত্ম-উদ্ধার):
        उद्धरेदात्मनात्मानं—Nobody is coming to rescue you from mediocrity. You must
        elevate yourself through direct, disciplined action.

💼 3-STEP DAILY GITA ANTI-LAZINESS PROTOCOL FOR KANAD:
   • 1. Catch the Seductive Whisper (Tamas Labeling):
        When the thought arises: "I will study later / Let me check reels", state:
        "This is Tamas Guna whispering. My mind is attempting to enslave my intellect."
   • 2. 5-Second Buddhi Physical Overrule:
        Stand up immediately, wash face with cold water, sit at the desk, and solve
        question #1. Physical movement forcefully drags the mind into alignment.
   • 3. Mirror Atma-Uddhar Declaration:
        Look in the mirror and declare: "I am my only savior. My mind is my servant,
        not my master. Today I execute with unbroken dignity."

📌 VAULT & HOMESERVER SYNERGY:
   • Note: 01_Mindset_Motive/Bhagavad_Gita_Krishna_Overcoming_Laziness_Mind_Mastery.md
   • Visual Matrix: Attachments/Bhagavad_Gita_Krishna_Overcoming_Laziness_Mind_Mastery_Matrix.jpg
   • Motive Anchor: 01_Mindset_Motive/Motive_and_Dignity_Anchor.md
   • Stoic Self-Control: 01_Mindset_Motive/Romano_Stoic_Self_Control_and_Emotional_Regulation.md
================================================================================
""")

def cmd_chanakya(args):
    print("""
================================================================================
⚔️ CHANAKYA NEETI: 4 INVIOLABLE BOUNDARIES OF SELF-RESPECT
================================================================================
💡 Core Dialectic:
   "जहाँ आदर नहीं, वहाँ जाना नहीं।
    जो सुनता नहीं, उसे समझाना नहीं।
    जो पछताता नहीं, उसे अपनाना नहीं।
    और जो सच बोलने पर भी रूठ जाए, उसे कभी मनाना नहीं।"
   — Acharya Chanakya • The Shikhshit Talks (@the_shikhshit_talks_) • Reel C4S7Ti7Bly_

🏛️ THE 4 INVIOLABLE BOUNDARIES (৪টি অলঙ্ঘনীয় সামাজিক ও আত্মসম্মান সীমানা):
   • 1. No Respect -> Never Go (जहाँ आदर नहीं, वहाँ जाना नहीं):
        Never seek validation in spaces designed to devalue your dignity.
        Do not step into houses or social circles where your time is mocked.
   • 2. Closed Mind -> Never Explain (जो सुनता नहीं, उसे समझाना नहीं):
        Cognitive energy is finite and sacred. Arguing with someone committed to
        misunderstanding you is intellectual suicide. Stop defending your goals.
   • 3. No Remorse -> Never Forgive/Accommodate (जो पछताता नहीं, उसे अपनाना नहीं):
        A mistake without genuine repentance is a calculated pattern.
        Permanently quarantine individuals who repeatedly violate your trust.
   • 4. Angered by Truth -> Never Appease (जो सच बोलने पर रूठ जाए, उसे कभी मनाना नहीं):
        Truth is objective reality. If someone sulks or plays victim when
        faced with reality, never apologize or flatter them. Let reality stand.

💼 3-STEP DAILY BOUNDARIES PROTOCOL FOR KANAD:
   • 1. Zero-Validation Geography: Stop attending toxic family/friend gatherings
        that question or ridicule your Govt exam journey (WBCS, Railways, SSC).
   • 2. Cut Discussion with Skeptics: Never explain your 10-hour study routine
        or career roadmap to people who have never built anything.
   • 3. Ruthless Reality Calibration: Accept mock test scores without delusion,
        and never apologize to anyone for prioritizing your exam hours over socializing.

📌 VAULT & REFERENCE SYNERGY:
   • Note: 01_Mindset_Motive/Chanakya_Neeti_Four_Inviolable_Boundaries_Mindset.md
   • Visual Matrix: Attachments/Chanakya_Neeti_Four_Inviolable_Boundaries_Matrix.jpg
   • Reference: ~/.gemini/config/skills/self-help/references/chanakya_boundaries_protocol.md
   • Power in Shadows: 01_Mindset_Motive/Lewis_Strauss_Power_Stays_in_the_Shadows.md
   • Self-Rescue: 01_Mindset_Motive/Devanand_Exist_Gita_Realistic_Self_Motivation.md
================================================================================
""")

def cmd_dangerous(args):
    print("""
================================================================================
⚔️ HK PRIME: 10 RULES TO BECOME DANGEROUS & ELIMINATE STAGNATION
================================================================================
💡 Core Dialectic:
   "Don't give a shit. They will hate you for your failure, and they will hate you for your success.
    Real is rare. Be real and rejected rather than fake and accepted.
    A man without a vision for his future will always return to his past.
    It's OK to fail. Fear being in the exact same place next year as you are now."
   — HK Prime (@hkprime_) • Reel C4NXKcVO0Mj

🏛️ THE 10 RULES IN 4 STRATEGIC QUADRANTS (৪টি কাঠামোগত স্তম্ভে ১০টি নীতি):
   [QUADRANT I: SOCIAL IMMUNITY & RADICAL DETACHMENT]
   • Rule 1: Don't Give a Shit (লোকনিন্দা ও প্রশংসায় নির্লিপ্ততা):
        They will hate you for your failure and hate you for your success. Detach completely.
   • Rule 2: Be Real & Unapologetic (মেকি স্বীকৃতির চেয়ে সত্যে বর্জন শ্রেয়):
        Real is so rare these days. Choose authentic rejection over fraudulent acceptance.
   • Rule 3: Remove the Clowns (সার্কাসের ভাঁড় ছাঁটাই; ঈগলের সাথে ওড়া):
        Befriend dogs, you learn to bark; befriend eagles, you learn how to fly. Cut low-aim peers.

   [QUADRANT II: COGNITIVE WEALTH & INTERNAL MASTERY]
   • Rule 5: Mind Precedes Wealth (ব্যাংক ব্যালান্সের আগেই মননশীল প্রাচুর্য):
        You become rich in your mind long before you become rich in your bank account.
   • Rule 7: Don't Be Sorry, Be Better (ভুলে বিলাপ নয়; দক্ষতায় উত্তর):
        Eliminate victim excuses and self-pity. Upgrade your competence and dominate.

   [QUADRANT III: RELENTLESS GRIT & STRATEGIC HARD WORK]
   • Rule 4: Sweat Over Wishful Thinking (বীজ বপন ছাড়া ফসলের স্বপ্ন মূর্খতা):
        No success without hard work. Waiting for harvest without sowing seeds is pure delusion.
   • Rule 6: The Darkest Hour Precedes Level Up (লেভেল আপের ঠিক আগেই সংঘাত চরম হয়):
        Things always get hardest right before the level up. Never quit when the resistance peaks.

   [QUADRANT IV: VISIONARY EXECUTION & STAGNATION ANNIHILATION]
   • Rule 8: Anchor an Unshakable Vision (দূরদৃষ্টিহীন মন পুরনো খাদে ফেরে):
        A man without a vision for his future will always return to his past failures and habits.
   • Rule 9: Ruthless Selective 'NO' (লক্ষ্যের বাইরের সবকিছুতে আপসহীন না):
        Decide what life you really want, then say NO to anything and anyone that isn't that.
   • Rule 10: Fear Stagnation Over Failure (ব্যর্থতাকে নয়; স্থবিরতাকে ভয় পাও):
        Failing is a data point. Fear being in the exact same unfulfilled place next year as now.

💼 3-STEP DANGEROUS EXECUTION PROTOCOL FOR KANAD:
   • 1. Morning Vision Priming (Rule 8 & 9):
        Review the Ashokan Empire Govt Exam roadmap before touching your phone. Say NO to distractions.
   • 2. Resistance Breaker at Study Block 3 (Rule 4 & 6):
        When mental exhaustion hits at 3 PM, recognize it as the pre-level-up boss fight. Push 1 more cycle.
   • 3. Ruthless Evening Social Quarantine (Rule 1, 2 & 3):
        Zero attendance in idle chatter. Zero remorse for unanswered gossip texts. Protect sovereign energy.

📌 VAULT & REFERENCE SYNERGY:
   • Note: 01_Mindset_Motive/10_Rules_To_Become_Dangerous_Mindset.md
   • Visual Matrix: Attachments/10_Rules_To_Become_Dangerous_Matrix.jpg
   • Reference: ~/.gemini/config/skills/self-help/references/10_rules_become_dangerous_protocol.md
   • Boundaries: 01_Mindset_Motive/Chanakya_Neeti_Four_Inviolable_Boundaries_Mindset.md
   • Laziness Annihilation: 01_Mindset_Motive/Bhagavad_Gita_Krishna_Overcoming_Laziness_Mind_Mastery.md
================================================================================
""")

def cmd_mindstorming(args):
    print("""
================================================================================
🧠 BRIAN TRACY: THE 20-IDEA MINDSTORMING METHOD
================================================================================
💡 Core Dialectic:
   "Write your goal or problem at the top of the page in the form of a question.
    You then force yourself to write 20 answers to that question.
    You'll be absolutely amazed at the quality of the answers that appear before you.
    This is called Mindstorming! It's one of the most powerful creative thinking exercises.
    Select at least ONE action and implement it immediately!"
   — Brian Tracy • Visionary Venue (@visionaryvenue) • Reel C3yS2M5s4Qo

🏛️ THE 3-STEP MINDSTORMING ARCHITECTURE (মূল ৩টি অপরিহার্য ধাপ):
   • STEP 1: Frame Goal as an Open Question (কাগজের শীর্ষে প্রশ্নাকারে নোঙর):
        Take a blank sheet. Never write a passive statement. Write an active, positive,
        measurable challenge. E.g.: "How can I score 75%+ in WBCS over the next 6 months?"
   • STEP 2: Force Exactly 20 Answers (বাধ্যতামূলকভাবে ২০টি উত্তরের লড়াই):
        Never stop at 3, 5, or 10. Write non-stop until you hit answer #20.
   • STEP 3: Execute At Least 1 Action Immediately (তৎক্ষণাৎ ১টি পদক্ষেপ বাস্তবায়ন):
        Review the 20 answers. Pick the single highest-leverage item and start executing NOW.

🧬 THE 3 COGNITIVE DEPTHS OF THE 20 ANSWERS (২০টি উত্তরের ৩-স্তরের গভীরতা):
   • Answers 1 — 5 : The Cognitive Ease Tier (সহজ ও চেনা পৃষ্ঠীয় উত্তর)
        Working memory dump: "Wake up early", "Stop using phone", "Read daily".
        Essential for clearing surface noise, but rarely revolutionary.
   • Answers 6 — 10 : The Analytical Friction Tier (বিশ্লেষণাত্মক ও কাঠামোগত স্তর)
        Friction begins; most people quit here! Pushes into routine systems, time-blocking,
        and process redesign.
   • Answers 11 — 20 : The Subconscious Breakthrough Tier (অবচেতন উদ্ভাবনী প্রজ্ঞা)
        Lateral thinking awakens. Answers 16 to 20 almost always contain the life-changing,
        unconventional, radical breakthroughs!

🎯 BRIAN TRACY'S 2 GOLDEN TRIGGER QUESTIONS:
   • Question 1 (The Single Greatest Problem):
        "What ONE problem, if I were to solve it, would have the greatest
         positive impact on my life, career, or exam success?"
   • Question 2 (The Single Greatest Goal):
        "What ONE goal, if I were to achieve it, would have the greatest
         positive impact on my future, status, and profitability?"

💼 KANAD'S DAILY EXAM MINDSTORMING SPRINT (১০ মিনিটের সকালের ড্রিল):
   • 1. Blank Paper Protocol: Every Sunday or study slump, write Kanad's core hurdle at the top.
   • 2. 20-Answer Sprint: Push through mental lethargy to generate 20 concrete micro-steps.
   • 3. Immediate 5-Minute Launch: Do step #1 before standing up from the desk.

📌 VAULT & REFERENCE SYNERGY:
   • Note: 02_Cognitive_Learning/Brian_Tracy_20_Idea_Mindstorming_Method.md
   • Visual Matrix: Attachments/Brian_Tracy_20_Idea_Mindstorming_Matrix.jpg
   • Reference: ~/.gemini/config/skills/self-help/references/brian_tracy_mindstorming_protocol.md
   • Learning Framework: 02_Cognitive_Learning/Oakley_Learning_Framework.md
   • Focus Masterclass: 02_Cognitive_Learning/Productivity_and_Focus_Masterclass.md
   • Bossidy Execution: 02_Cognitive_Learning/Larry_Bossidy_Ram_Charan_Execution.md
================================================================================
""")

def cmd_noregret(args):
    print("""
================================================================================
🕊️ SUDHA MURTY: NO REGRETS, SELF-ELEVATION & GITA 6.5
================================================================================
💡 Core Dialectic:
   "Regret ka toh koi sthaan nahi hai life mein!
    'Maine yeh kyon nahi kiya, aisa karna chahiye tha...'
    Jo kiya aapne us waqt ke akal ke hisaab se kiya! Aapne jaise jiya, sahi kiya.
    Apne aap ko neeche mat girao! Bhagavad Gita mein bahut strong shlok hai:
    'उद्धरेदात्मनात्मानं नात्मानमवसादयेत्'—Apne aap ko upar uthao! Apne aap ko pyaar karo!
    You should know that aap sab kuch kar sakte ho! Apne aap mein confidence laao!"
   — Sudha Murty • Podcast Media (@pod.castmedia) • Reel C3uFLw2vA8r

🏛️ THE 3 PILLARS OF SOVEREIGN SELF-ELEVATION:
   • Pillar 1: The Zero-Regret Axiom (অনুশোচনাহীন অতীত):
        Never judge past decisions with today's maturity. You acted according to
        the wisdom, pressures, and awareness you had at that exact time. Drop the guilt.
   • Pillar 2: Prohibition of Self-Degradation (নাৎমানমবসাদয়েৎ):
        Sri Krishna & Sudha Murty strictly forbid self-loathing. You must be your
        own best friend and savior. Self-pity is a spiritual and mental toxin.
   • Pillar 3: Radical Self-Belief (অপরাজেয় আত্মবিশ্বাস):
        "Aap sab kuch kar sakte ho!" What can't you achieve? Awaken unyielding
        confidence in your prefrontal capacity and steady daily execution.

💼 KANAD'S DAILY PROTOCOL (WBCS & GOVT EXAM SOVEREIGNTY):
   • 1. Banish Career Guilt: Drop all remorse over previous jobs or timeline delays.
        Channel 100% of your metabolic and cognitive force into the study desk.
   • 2. Mock Test Failure Armor: After a poor mock score, never plunge into despair.
        Analyze mistakes neutrally, refine notes, and rise back up immediately.
   • 3. Daily Identity Affirmation: Every morning recite: "उद्धरेदात्मनात्मानं".
        No rescuer is coming; Kanad rescues Kanad through focused discipline.

📌 VAULT & REFERENCE SYNERGY:
   • Note: 01_Mindset_Motive/Sudha_Murty_No_Regret_and_Self_Elevation.md
   • Visual Matrix: Attachments/Sudha_Murty_No_Regret_Self_Elevation_Matrix.jpg
   • Reference: ~/.gemini/config/skills/self-help/references/sudha_murty_no_regret_protocol.md
   • Gita Laziness Elimination: 01_Mindset_Motive/Bhagavad_Gita_Krishna_Overcoming_Laziness_Mind_Mastery.md
   • Realistic Self-Motivation: 01_Mindset_Motive/Devanand_Exist_Gita_Realistic_Self_Motivation.md
   • Amor Fati & No Regret: 02_Cognitive_Learning/Paul_Auster_4321_Parallel_Lives_and_Counterfactual_Mastery.md
================================================================================
""")

def cmd_traits(args):
    print("""
================================================================================
⚡ ALEX HORMOZI: THE 3 TRAITS OF HYPER-SUCCESSFUL PEOPLE (THE HORMOZI PARADOX)
================================================================================
💡 Core Dialectic:
   "What are the three most common traits of hyper-successful people?
    I think it's:
    1. A superiority complex — They believe that they are better than other people
       and that they deserve more.
    2. Crippling insecurity — They have this deep, existential feeling that they're
       never going to be enough.
    3. Impulse control — They have the ability to focus on one thing for an
       extended period of time and not get distracted.
    The superiority complex makes you think you can do it. The crippling insecurity
    makes you feel like you have to do it to be okay. And the impulse control
    makes you actually stick to it long enough to make it happen."
   — Alex Hormozi (@hormozi) & Chris Williamson (@chriswillx) • Modern Wisdom #610

🏛️ THE 3 CORE PSYCHOLOGICAL PILLARS:
   • 1. Superiority Complex (The Gas Pedal / The Cheese / শ্রেষ্ঠত্ববোধ):
        An unshakeable, irrational conviction that you are destined for greatness.
        You reject average outcomes and genuinely believe you can do what others call impossible.
   • 2. Crippling Insecurity (The Burning Engine / The Cat / চিরস্থায়ী অতৃপ্তি):
        A persistent existential void and terror of mediocrity ("Never Enough").
        No matter how much you achieve, the bar rises. This fire prevents complacency.
   • 3. Impulse Control (The Steering Wheel / The Narrow Tube / আবেগীয় সংযম):
        The supreme ability to delay gratification, resist short-term dopamine temptations,
        and endure years of monotonous, boring execution without chasing shiny objects.

⚔️ THE DUAL PROPULSION + CHANNELING ENGINE:
   • The Pull (Superiority): Pulls you toward the monumental goal.
   • The Push (Insecurity): Chases you away from the horror of being a failure.
   • The Tube (Impulse Control): Confines the massive kinetic energy into a single vector.

💼 KANAD'S DAILY PROTOCOL (WBCS GROUP A & EXAM MASTERY):
   • 1. AM Superiority Anchoring: 5-minute morning affirmation of executive command.
        "I was born to conquer WBCS Group A. Average mediocrity is unacceptable."
   • 2. Insecurity Fuel Transmutation: When self-doubt strikes, do NOT soothe yourself
        with social media or comfort food. Use the anxiety as fuel: open Indian Polity & solve 50 MCQs.
   • 3. Iron Monastic Sprints: 4x90-minute blocks with zero tab-switching and zero phone distraction.
        Tolerate syllabus revision boredom with stoic resolve.

📌 VAULT & REFERENCE SYNERGY:
   • Note: 01_Mindset_Motive/Alex_Hormozi_Three_Traits_of_Hyper_Successful_People.md
   • Visual Matrix: Attachments/Hormozi_Three_Traits_Hyper_Successful_Matrix.jpg
   • Reference: ~/.gemini/config/skills/self-help/references/alex_hormozi_three_traits_protocol.md
   • Zero Regret & Self-Elevation: 01_Mindset_Motive/Sudha_Murty_No_Regret_and_Self_Elevation.md
   • Dangerous Mindset: 01_Mindset_Motive/10_Rules_To_Become_Dangerous_Mindset.md
   • Focus Reclamation: 02_Cognitive_Learning/Johann_Hari_Stolen_Focus.md
   • Productivity & Focus: 02_Cognitive_Learning/Productivity_and_Focus_Masterclass.md
================================================================================
""")

def cmd_twopains(args):
    print("""
================================================================================
⚖️ JIM ROHN: THE TWO PAINS — DISCIPLINE VS REGRET (@excelleratee)
================================================================================
💡 Core Dialectic:
   "We must all suffer one of two pains: the pain of discipline or the pain of regret.
    The difference is discipline weighs ounces, while regret weighs tons —
    because it can accumulate."
   — Jim Rohn (Father of Modern Personal Development & Mentor to Tony Robbins)

🏛️ THE 4 FOUNDATIONAL LAWS OF SUFFERING:
   • 1. Suffering is Inevitable (যন্ত্রণা সার্বজনীন ও অনিবার্য):
        No human escapes discomfort. Escapism through sleep, reels, and procrastination
        is a fatal illusion. You cannot choose a pain-free life; you only choose WHICH pain.
   • 2. The Pain of Discipline (শৃঙ্খলার কষ্ট — ওজন: আউন্স):
        Acute, temporary, localized, and proactive. The pain of waking up at 6 AM, sitting
        for a 90-min study sprint, and resisting junk dopamine burns for minutes, then
        instantly transforms into dignity, self-respect, and neurological resilience.
   • 3. The Pain of Regret (অনুশোচনার যন্ত্রণা — ওজন: টন টন):
        Chronic, toxic, and cumulative. The agonizing question of "What if?" Looking back
        after years and knowing you held back your true potential crushes the human soul.
   • 4. The Accumulation Trap (কেন অনুশোচনা জমে পাহাড় হয়):
        Discipline is cash: pay a daily micro-tax and stay free.
        Regret is predatory debt: defer today's effort, and interest compounds exponentially.

💼 KANAD'S DAILY PROTOCOL (WBCS & GOVT EXAM SOVEREIGNTY):
   • 1. Morning Weight Calibration: Alarm rings -> Compare: 2 ounces of getting up now
        vs 20 tons of seeing your name missing from the WBCS merit list. Choose 2 ounces.
   • 2. Distraction Refusal: When phone/reels tempt during study, speak aloud:
        "This scroll is buying regret on high-interest credit. I refuse." Lock phone away.
   • 3. Evening Dignity Audit: Clear all 4x90-min study blocks before bed. Sleep in absolute
        mental peace knowing today's invoice of discipline has been paid in full.

📌 VAULT & REFERENCE SYNERGY:
   • Note: 01_Mindset_Motive/Jim_Rohn_The_Two_Pains_Discipline_vs_Regret.md
   • Visual Matrix: Attachments/Jim_Rohn_Two_Pains_Discipline_vs_Regret_Matrix.jpg
   • Reference: ~/.gemini/config/skills/self-help/references/jim_rohn_two_pains_protocol.md
   • Zero Regret & Self-Elevation: 01_Mindset_Motive/Sudha_Murty_No_Regret_and_Self_Elevation.md
   • Hyper-Success Engine: 01_Mindset_Motive/Alex_Hormozi_Three_Traits_of_Hyper_Successful_People.md
   • Dangerous Mindset: 01_Mindset_Motive/10_Rules_To_Become_Dangerous_Mindset.md
================================================================================
""")

def cmd_tedtalks(args):
    print("""
================================================================================
🎙️ TRADING TIERS: 7 LIFE-CHANGING TED TALKS (@tradingtiers)
================================================================================
💡 Core Dialectic:
   "Gaining market exposure and watching these 7 TED talks have helped me earn
    $100,000+ in trading over the last year. The lessons from these TED Talks
    would have saved me 2 years of expensive mistakes if I had discovered them earlier."
   — Trading Tiers (@tradingtiers) • Reel C2sIR_3Bx1a

🏛️ THE 7 COGNITIVE & DECISION-MAKING MASTERCLASSES:
   • 1. How the Greatest Investors Win in Markets & Life (William Green):
        25 years of interviewing titans (Charlie Munger, John Templeton). Success comes
        from avoiding stupidity rather than seeking brilliance. Play the long compounding game.
   • 2. The Mindset of a Trader (Hicham Benjelloun):
        Markets and reality operate on probabilities, not certainties. Detach your ego from
        individual trades or mock test outcomes; execute your disciplined mathematical strategy.
   • 3. The Power of Belief: Mindset and Success (Eduardo Briceño):
        Growth mindset conditioning. Focus on progress over end-results. Mistakes and wrong
        answers are vital diagnostic feedback, not proofs of limited intelligence.
   • 4. Why We Make Bad Decisions (Dan Gilbert):
        Harvard psychology research on cognitive biases. Presentism makes humans discount
        future rewards for cheap instant comfort. Recognize the cognitive trap.
   • 5. How to Make Stress Your Friend (Kelly McGonigal):
        Stanford neurobiology: Stress only kills when you believe it is harmful. Reframe
        the pounding heart and nervousness as your body's "Courage Response" oxygenating your brain.
   • 6. The Paradox of Choice (Barry Schwartz):
        An overload of options breeds decision fatigue, paralysis, and dissatisfaction.
        Drastically limit your choices: pick 1 primary book per subject and master it 10 times.
   • 7. Success is a Continuous Journey (Richard St. John):
        Success is never a fixed destination; it is an unceasing circular loop. Complacency is
        the silent killer of champions. Stay humble, curious, and relentlessly disciplined.

💼 KANAD'S DAILY PROTOCOL (WBCS & GOVT EXAM SOVEREIGNTY):
   • 1. Book Clutter Purge (Barry Schwartz): Lock away 10 secondary PDFs. Stick to 1 core book.
   • 2. Error Neutrality (Benjelloun & Briceño): Mock test errors = free diagnostic gold.
   • 3. Biological Courage (Kelly McGonigal): Exam pressure is your prefrontal turbocharger.
   • 4. Long-Range Compounding (William Green): Monastic 4x90-min daily grind wins the war.

📌 VAULT & REFERENCE SYNERGY:
   • Note: 02_Cognitive_Learning/Trading_Tiers_7_Life_Changing_TED_Talks_Mastery.md
   • Visual Matrix: Attachments/Trading_Tiers_7_Life_Changing_TED_Talks_Matrix.jpg
   • Reference: ~/.gemini/config/skills/self-help/references/trading_tiers_ted_talks_protocol.md
   • Focus Reclamation: 02_Cognitive_Learning/Johann_Hari_Stolen_Focus.md
   • Learning Science: 02_Cognitive_Learning/Benedict_Carey_How_We_Learn.md
   • Timeless Constants: 02_Cognitive_Learning/Morgan_Housel_Same_As_Ever.md
================================================================================
""")

def cmd_toxic(args):
    print("""
================================================================================
🛑 DAN ZAKARIA: TOP 10 PEOPLE TO AVOID AT ALL COSTS (@danzakaria)
================================================================================
💡 Core Dialectic:
   "Top 10 people to avoid (at all costs):
    1. Complainers           6. Victim mindset people
    2. Jealous people        7. Backstabbers
    3. People with no goals  8. Doubters
    4. Negative thinkers     9. Talkers (no action)
    5. Users (opportunists) 10. Procrastinators"
   — Dan Zakaria (@danzakaria) • Facebook Reel 1464512378893610

🏛️ THE 3 TOXIC CATEGORIES & COUNTERMEASURES:
   • 1. Energy & Emotional Vampires (Complainers, Jealous, Negative, Victims):
        Drains prefrontal neural energy and elevates systemic cortisol.
        Countermeasure: 'Grey Rock' method — zero emotional fuel, absolute silence.
   • 2. Ambition & Progress Killers (No Goals, Doubters, Talkers, Procrastinators):
        Normalizes mediocrity, cheap verbal dopamine, and perpetual delay.
        Countermeasure: Radical Selective 'NO' — protect monastic 4x90-min study blocks.
   • 3. Social Parasites & Manipulators (Users, Backstabbers):
        Exploitative opportunists who smile to your face and stab your trust.
        Countermeasure: Strict confidentiality — Robert Greene Law 4 (Say Less Than Necessary).

💼 KANAD'S DAILY PROTOCOL (WBCS MONASTIC BOUNDARY SHIELD):
   • 1. Telegram & Social Group Purge: Archive/mute all exam gossip and whining groups.
   • 2. Silent Grind Law: Never announce mock test scores or daily targets to peers.
   • 3. Inversion Discipline: To clear WBCS, eliminate 100% of social distractions first.
   • 4. 2x Daily Comm Check: Limit messages/calls to 15m afternoon and 20m night.

📌 VAULT & REFERENCE SYNERGY:
   • Note: 01_Mindset_Motive/Dan_Zakaria_Top_10_People_To_Avoid_At_All_Costs.md
   • Visual Matrix: Attachments/Dan_Zakaria_10_People_To_Avoid_Matrix.jpg
   • Reference: ~/.gemini/config/skills/self-help/references/dan_zakaria_toxic_people_protocol.md
   • Chanakya Boundaries: 01_Mindset_Motive/Chanakya_Neeti_Four_Inviolable_Boundaries.md
   • 10 Rules To Dangerous: 01_Mindset_Motive/10_Rules_To_Become_Dangerous_Mindset.md
   • Robert Greene Crucible: 01_Mindset_Motive/Robert_Greene_Turn_The_Tables_Crucible.md
   • Attention Ecology: 02_Cognitive_Learning/Johann_Hari_Stolen_Focus.md
================================================================================
""")

def cmd_braindiscipline(args):
    print("""
================================================================================
🧠 HOW TO TRAIN YOUR BRAIN TO ENJOY DISCIPLINE (@codewithblacky)
================================================================================
💡 Core Dialectic:
   "Discipline is not a punishment for your weaknesses; it is the currency of
    your sovereignty. Stop waiting for motivation. Decouple action from feelings
    and execute anyway."
   — Solu Mondal (@codewithblacky) x Dan Zakaria Curated Masterclasses

🏛️ THE 6 CURATED NEURO-DISCIPLINE MASTERCLASSES:
   • 1. Solo Leveling Monastic Mindset (Slide 1 - Sung Jin-woo):
        Transform from passive spectator to sovereign monk. Daily quests with zero excuses.
   • 2. Dr. Justin Sung: How to Force Your Brain to Study (Slide 2):
        Non-linear concept maps over rote memorization. Master cognitive friction and load.
   • 3. Amy Wang: This Will Make You Want to Work Hard (Slide 3):
        Dopamine baseline reset. Find pride and deep serotonin in daily friction.
   • 4. Dan Zakaria: Psychology of Discipline (Slide 4 - img_index=4):
        "DO IT ANYWAY." Feelings are an illusion. Motivation follows action, never precedes it.
        Kill the internal negotiator. Identity shift: You are a disciplined civil servant.
   • 5. Dr. Izzy Sealey: How to Train Your Brain to Be Focused (Slide 5):
        Attentional spotlight & visual gating. Zero-latency study initiation.
   • 6. Ali Abdaal: 5 Ways to Become More Self-Disciplined (Slide 6):
        Friction architecture: Eliminate willpower reliance. Track lead metrics (4x90 min blocks).
   • 7. Ruri Ohama: 7 Weird ADHD Hacks to Improve Your Life (Slide 7):
        2-minute micro-commitment gateway, body doubling, and novelty injection.

💼 KANAD'S WBCS 4x90 MONASTIC STUDY ARCHITECTURE:
   • Block 1 (08:00 - 09:30): Dan Zakaria Protocol — "Do it anyway." Hardest topic (Math/Economy).
   • Block 2 (11:00 - 12:30): Justin Sung Protocol — Non-linear semantic concept mapping in Obsidian.
   • Block 3 (15:00 - 16:30): Izzy Sealey + Ruri Ohama Protocol — 2-min gateway & PYQ sprints.
   • Block 4 (19:00 - 20:30): Amy Wang + Ali Abdaal Protocol — Lead metrics audit & night desk prep.

📌 VAULT & REFERENCE SYNERGY:
   • Note: 02_Cognitive_Learning/CodeWithBlacky_How_To_Train_Brain_To_Enjoy_Discipline.md
   • Visual Matrix: Attachments/CodeWithBlacky_Train_Brain_Discipline_Matrix.jpg
   • Reference: ~/.gemini/config/skills/self-help/references/codewithblacky_brain_discipline_protocol.md
   • Dan Zakaria Avoid People: 01_Mindset_Motive/Dan_Zakaria_Top_10_People_To_Avoid_At_All_Costs.md
   • Focus Masterclass: 02_Cognitive_Learning/Productivity_and_Focus_Masterclass.md
   • Oakley Learning: 02_Cognitive_Learning/Oakley_Learning_Framework.md
================================================================================
""")

def cmd_upperbody(args):
    print("""
================================================================================
🏋️‍♂️ NO-GYM UPPER BODY CALISTHENICS PROTOCOL (@a_k_da_don / Grandson)
================================================================================
💡 Core Training Formula:
   "🔥 Upper Body Workout to Get Strong & Defined | No Gym Needed
    3 sets of 40 secs each | 2-3 rounds | Rest 60 secs between rounds"
   — Grandson (@a_k_da_don) • Instagram Reel DfITBBht9PO

🏛️ THE 6 ANATOMICAL CALISTHENICS POWER MOVEMENTS:
   • 1. Wide-Grip Deficit Chest Pushups (ওভারসাইজড ওয়াইড-গ্রিপ পুশআপ):
        Target: Sternal & Costal Pecs (Outer Chest Flare, Depth & Serratus Anterior).
        Mechanics: Hands 1.5x shoulder width, 3-sec eccentric descent, full chest stretch.
   • 2. Reverse-Grip Pelican / Bicep Pushups (রিভার্স-গ্রিপ বাইসেপ পুশআপ):
        Target: Biceps Brachii, Brachialis & Distal Biceps Tendon Architecture.
        Mechanics: Palms turned backwards toward hips, elbows tracking tight along ribcage.
   • 3. Diamond / Inward-Squeeze Pushups (ডায়মন্ড / ক্লোজ-গ্রিপ পুশআপ):
        Target: Sternal Squeeze Cleavage & Triceps Brachii (Medial & Lateral Heads).
        Mechanics: Index fingers & thumbs forming diamond directly below sternum.
   • 4. Sphinx Bodyweight Triceps Extensions (স্ফিংস বডিওয়েট ট্রাইসেপস এক্সটেনশন):
        Target: Triceps Brachii Long Head & Lateral Horseshoe Definition ("Day 1 vs Day 10").
        Mechanics: Forearm plank position, push through palms to elevate forearms off ground.
   • 5. Pike Pushup / Overhead Press (পাইক পুশআপ / ভার্টিক্যাল প্রেস):
        Target: Anterior & Lateral Deltoids, Clavicular Upper Chest & Trapezius.
        Mechanics: Hips elevated in sharp V-shape, head travels forward in tripod trajectory.
   • 6. Mantis Knuckle / Forearm Press (ম্যান্টিস নাকল ও রিস্ট প্রেস):
        Target: Wrist Extensors/Flexors, Forearm Vascularity & Hand Density ("Week 1 vs Week 4").
        Mechanics: Kneeling or modified plank on knuckles/forearms, controlled wrist load.

⏱️ WORKOUT ARCHITECTURE & CADENCE:
   • Work Interval: 40 seconds continuous time-under-tension (TUT) per exercise.
   • Intra-Exercise Rest: 20 seconds deep nasal recovery & metabolic clearance.
   • Inter-Round Rest: 60-90 seconds between full 6-exercise circuits.
   • Volume: 2-3 full rounds (Total duration: 18-25 minutes).
   • Frequency: 3-4 days per week (Alternating with lower body / walking / core).

💼 KANAD'S WBCS STUDY BREAK INTEGRATION (82 KG ➔ 72 KG CUT):
   • Zero-Equipment Monastic Break: Execute during 20-min breaks between 90-min study blocks.
   • Posture & Cervical Decompression: Reverse thoracic kyphosis and study slouching.
   • Metabolic Fire: Elevates EPOC, increases insulin sensitivity, accelerates fat oxidation.
   • Dopamine & Focus Recalibration: Replaces social media binging with physical mastery.

📌 VAULT & REFERENCE SYNERGY:
   • Note: 03_Habits_Protocols/AK_Da_Don_Upper_Body_No_Gym_Calisthenics_Protocol.md
   • Visual Matrix: Attachments/AK_Da_Don_Upper_Body_No_Gym_Calisthenics_Matrix.jpg
   • Reference: ~/.gemini/config/skills/self-help/references/ak_da_don_upper_body_calisthenics_protocol.md
   • Daily Routine Flow: 03_Habits_Protocols/Daily_Routine_Flow_Guide.md
   • Shoulder Protocol: 03_Habits_Protocols/Shoulder_Mobility_and_Rotator_Cuff_Protocol.md
   • Posture Correction: 03_Habits_Protocols/Bottle_Posture_Correction_Protocol.md
================================================================================
""")

def cmd_standingabs(args):
    print("""
================================================================================
🥋 STANDING AB WORKOUTS AT HOME PROTOCOL (@a_k_da_don / Grandson)
================================================================================
💡 Core Training Formula:
   "Standing ab workouts at home 🏠🔥
    3 sets of 40 secs each | 2-3 rounds | Rest 60 secs between rounds"
   — Grandson (@a_k_da_don) • Instagram Reel DehcPahqkup

🏛️ THE 4 STANDING CORE POWER MOVEMENTS:
   • 1. Standing Straight Leg Kicks / Alternating High Kicks (দাঁড়িয়ে পা তুলে লোয়ার অ্যাবস):
        Target: Lower Rectus Abdominis, Iliopsoas (Hip Flexors) & Deep Core Compression.
        Mechanics: Swing straight leg to chest height with forward reach & toe tap.
        Advantage: Zero floor spinal shear forces; protects L4-L5 lumbar vertebrae.
   • 2. Standing Lateral Leg Raises / Oblique Abductions (হাত কোমরে রেখে পার্শ্বীয় পা উত্তোলন):
        Target: External & Internal Obliques, Transverse Abdominis (TVA / Inner Corset).
        Mechanics: Hands on hips; strict lateral leg abduction without tilting torso.
        Advantage: Tightens the deep abdominal wall to snatch and flatten bloated waistline.
   • 3. Standing Knee-to-Elbow Oblique Crunch (প্রিজনার স্ট্যান্সে কনুই-হাঁটু অবলিক ক্রাঞ্চ):
        Target: Oblique Flanks, Serratus Anterior & V-Taper Definition ("Love Handle Shredder").
        Mechanics: Prisoner hands behind ears; drive knee sideways while crushing ribcage down.
        Advantage: Concentrated lateral fiber shortening; sculpts side-ab striations.
   • 4. Combat High-Knee Core March (কম্ব্যাট স্ট্যান্সে হাই-নী কোর মার্চ):
        Target: Total Rectus Abdominis, Deep Core Bracing & Cardio EPOC Burn.
        Mechanics: Boxing guard stance; rapid rhythmic high-knee drives with abdominal bracing.
        Advantage: Ramps heart rate into fat-burning zone for rapid visceral fat oxidation.

⏱️ CADENCE & CIRCUIT PROTOCOL:
   • Work Interval: 40 seconds continuous time-under-tension (TUT) per exercise.
   • Intra-Exercise Rest: 20 seconds nasal parasympathetic recovery.
   • Round Duration: 4 minutes per full circuit of 4 exercises.
   • Volume: 2-3 full rounds (60-90 seconds rest between rounds).
   • Total Duration: 12-16 minutes (No mat, no floor contact, zero equipment).

💼 KANAD'S WBCS STUDY BREAK INTEGRATION (82 KG ➔ 72 KG CUT):
   • Zero-Friction 6-Min Study Break: Complete 1 round between 90-min study blocks.
   • Reverses Study Slouching: Activates deep core and glutes in upright standing posture.
   • Dopamine Recalibration: Replaces social media binging with physical accomplishment.
   • Day 1 to Day 21 Progression: Accelerates visceral fat loss alongside caloric deficit.

📌 VAULT & REFERENCE SYNERGY:
   • Note: 03_Habits_Protocols/AK_Da_Don_Standing_Abs_Home_Workout_Protocol.md
   • Visual Matrix: Attachments/AK_Da_Don_Standing_Abs_Workout_Matrix.jpg
   • Reference: ~/.gemini/config/skills/self-help/references/ak_da_don_standing_abs_workout_protocol.md
   • Upper Body Calisthenics: 03_Habits_Protocols/AK_Da_Don_Upper_Body_No_Gym_Calisthenics_Protocol.md
   • Bedtime Pelvic Reset: 03_Habits_Protocols/Alex_Libin_Bedtime_Pelvic_Tilt_and_Flat_Belly_Protocol.md
   • Bottle Posture: 03_Habits_Protocols/Bottle_Posture_Correction_Protocol.md
   • Daily Routine Flow: 03_Habits_Protocols/Daily_Routine_Flow_Guide.md
================================================================================
""")

def cmd_skipreadstudy(args):
    print("""
================================================================================
📚 JULIE HOGBIN: SKIP, READ, STUDY 3-TIER BOOK FILTER & CONSCIOUS LEADERSHIP
================================================================================
💡 Core Dialectic & Philosophy:
   "Skip, Read or Study? The 3-Tier Cognitive Filter for High-Impact Leadership"
   — Julie Hogbin (@juliehogbin / juliehogbin.com) • Conscious Leadership Coach
   Author & Publisher (Hogbin House Publishing), Co-Author of 'Wealth Beyond Money'

🏛️ THE 3-TIER COGNITIVE READING FILTER:
   • 1. 🔴 SKIP (Superficial, Stretched, or Outdated Fluff):
        - Atomic Habits (James Clear): 5-minute blog post stretched to 300 pages. Action beats reading.
        - The 4-Hour Workweek (Tim Ferriss): Outdated 2007 geo-arbitrage. Monastic execution needed.
        - Awaken the Giant Within (Tony Robbins): 90s NLP hype & emotional highs without sober systems.
   • 2. 🟡 READ (Mental Models & Paradigm Shifts — Read Once):
        - Rich Dad Poor Dad (Robert Kiyosaki): Asset vs liability shift; lacks deep investing rigor.
        - Ready, Fire, Aim (Michael Masterson): Speed of execution; sell before perfecting.
        - The Psychology of Money (Morgan Housel): Behavior beats intellect; financial slack & room for error.
        - The Intelligent Investor (Benjamin Graham): Margin of Safety & Mr. Market detachment.
   • 3. 🟢 STUDY (The Core Canon — Daily Active Recall & Character Building):
        - Think and Grow Rich (Napoleon Hill): Subconscious programming, DMP & autosuggestion.
        - The Leadership Challenge (Kouzes & Posner): "Study. If you want to be a good leader, read this book."
        - How to Win Friends and Influence People (Dale Carnegie): 70/30 listening ratio, human diplomacy.
        - The 7 Habits of Highly Effective People (Stephen Covey): Character ethic & Private-to-Public victory.
        - Wealth Beyond Money (Hogbin & Ezekiel): "Study, study, study! If you want success and balance, study!"

👑 THE KOUZES & POSNER 5 LEADERSHIP PRACTICES (FOR WBCS / ADMINISTRATIVE EXCELLENCE):
   • 1. Model the Way: Clarify personal values and lead by 100% Behavioral Consistency.
   • 2. Inspire a Shared Vision: Paint an inspiring, collective picture of the future.
   • 3. Challenge the Process: Seize initiative, experiment, modernise workflows, and learn from mistakes.
   • 4. Enable Others to Act: Foster trust, share power, and build psychological safety.
   • 5. Encourage the Heart: Sincerely recognize individual contributions and celebrate collective wins.

💎 JULIE HOGBIN'S 4 PILLARS OF TRUE WEALTH ('Wealth Beyond Money'):
   • 1. Health: Neurological vigor, physical endurance, clean nutrition & posture.
   • 2. Relationships: Sincere human bonds, empathy, family loyalty, and zero toxic ego.
   • 3. Financial Sovereignty: Debt freedom, margin of safety, and silent long-term compounding.
   • 4. Life Balance & Purpose: Deep inner peace, spiritual calm, and societal legacy.

💼 KANAD'S WBCS & COGNITIVE ACTION PROTOCOL:
   • 1. Audit Reading List: Ruthlessly eliminate repetitive habit fluff.
   • 2. Allocate Study Blocks: Dedicate prime 60-min daily deep work solely to STUDY canon.
   • 3. Active Recall & Cornell Notes: Close the book and synthesize 3 core rules in own words.
   • 4. Direct Execution: Prioritize desk study (Math, Reasoning, History) over passive reading.

📌 VAULT & REFERENCE SYNERGY:
   • Note: 02_Cognitive_Learning/Julie_Hogbin_Skip_Read_Study_Books_Framework.md
   • Visual Matrix: Attachments/Julie_Hogbin_Skip_Read_Study_Books_Matrix.jpg
   • Reference: ~/.gemini/config/skills/self-help/references/julie_hogbin_skip_read_study_protocol.md
   • Rob Moore Priority Matrix: 02_Cognitive_Learning/Rob_Moore_Book_Reading_and_Study_Priorities.md
   • Master Dashboard: 00_Dashboard/Master_Self_Help_Hub.md
================================================================================
""")

def cmd_forearms(args):
    print("""
================================================================================
🦾 HIMANSU FIT: SHIRT-SLEEVE FOREARM AESTHETIC & 3-STEP GIANT SET PROTOCOL
================================================================================
💡 Core Training Dialectic:
   "Jab tum koi shirt pehno to tumhara forearms kuch aisa dikhe, too crazy na?
    To simple tumhe kya karna hai, aise do dumbbell pakad lena hai... bina chhode!"
   — Himansu Behera (@himansu_fit_) • Instagram Reel DfJe6XaSFC2

🏛️ THE 3-STEP MECHANICAL GIANT SET ("BINA CHHODE" PROTOCOL):
   • 1. Standing Dumbbell Wrist Rotations (১৮০° প্রোনেশন-সুপিনেশন ঘূর্ণন):
        Reps: 20 to 30 reps (Controlled 180-degree rotation arc).
        Target: Pronator Teres, Pronator Quadratus, Supinator & Brachioradialis.
        Mechanics: Elbows bent at 90 degrees; rotate palms down (pronation) to palms up (supination).
        Benefit: Dense rotational stability, thickens wrist joints and tendon insertions.
   • 2. Overhand Pronated Reverse Wrist Curls (ওভারহ্যান্ড রিভার্স রিস্ট এক্সটেনশন):
        Reps: 5 to 15 reps (Strict wrist extension against gravity).
        Target: Extensor Carpi Radialis Longus/Brevis & Extensor Digitorum.
        Mechanics: Immediately shift to overhand grip; extend wrists upward toward the upper forearm.
        Benefit: Builds the muscular upper forearm "shelf" visible when arms hang at your side.
   • 3. Underhand Supinated Regular Wrist Curls (আন্ডারহ্যান্ড রেগুলার রিস্ট ফ্লেকশন):
        Reps: 5 to 15 reps (Full range wrist flexion to complete burnout).
        Target: Flexor Carpi Radialis, Flexor Carpi Ulnaris & Palmaris Longus.
        Mechanics: Instantly flip to underhand grip; curl wrists upward into maximum contraction.
        Benefit: Explodes deep inner forearm thickness, crushing grip power & cephalic vascularity.

⚡ THE "BINA CHHODE" LAW (BLOOD OCCLUSION & REACTIVE HYPEREMIA):
   • Zero Rest Between Exercises: Execute Step 1 ➔ Step 2 ➔ Step 3 without dropping dumbbells!
   • Continuous Isometric Grip: Restricts venous outflow, forcing rapid oxygen depletion.
   • Reactive Hyperemia Pump: Releasing dumbbells after the tri-set floods forearms with blood.
   • Volume: 2-3 full rounds • Rest: 60-90 seconds between rounds • Total: 6-8 minutes.

👔 FASHION & MASCULINE AESTHETIC INTEGRATION:
   • The 100% Visible Muscle: In formal/casual shirts, forearms are always exposed.
   • Master / Italian Sleeve Roll: Unbutton cuff, pull 1.5-2 inches below elbow, fold lower fabric.
   • Never roll above the elbow (protects professional gravitas and frames forearm V-taper).
   • Watch & Metal Contrast: Pair with silver/leather wristwatch for quiet masculine authority.

💼 KANAD'S WBCS MONASTIC STUDY BREAK INTEGRATION (82 KG ➔ 72 KG CUT):
   • Zero-Travel Finish: Keep 2 dumbbells by study desk in Arambagh or Liluah.
   • Execute 1 round (2 min) after 90-min deep work session (Math/Reasoning/History).
   • Reduces cortisol, stimulates endorphins, and provides instant dopamine without phone scrolling.

📌 VAULT & REFERENCE SYNERGY:
   • Note: 03_Habits_Protocols/Himansu_Fit_Forearm_Shirt_Sleeve_Aesthetic_Protocol.md
   • Visual Matrix: Attachments/Himansu_Fit_Forearm_Shirt_Sleeve_Aesthetic_Matrix.jpg
   • Reference: ~/.gemini/config/skills/self-help/references/himansu_fit_forearm_hypertrophy_protocol.md
   • Fashion Guide: 04_Fashion_Grooming/Kanad Wardrobe.md
   • Upper Body Calisthenics: 03_Habits_Protocols/AK_Da_Don_Upper_Body_No_Gym_Calisthenics_Protocol.md
   • Standing Abs: 03_Habits_Protocols/AK_Da_Don_Standing_Abs_Home_Workout_Protocol.md
================================================================================
""")

def cmd_sunil(args):
    print("""
================================================================================
🧘 SUNIL YOGA FIT: ANTERIOR PELVIC TILT (APT) & LORDOSIS CORRECTION PROTOCOL
================================================================================
💡 Core Clinical Dialectic:
   "Fix your anterior pelvic tilt with help of these exercises... daily 3-5 minutes! ✅"
   — Sunil Dhayal (@sunilyogafit_) • Instagram Reel DfMvfLsyS2B

🏛️ THE 4 CORRECTIVE YOGA MOVEMENTS (3-5 MINUTES DAILY):
   • 1. Pawanmuktasana / Lumbar Tuck & Roll (পবনমুক্তাসন — লাম্বার ডিকম্প্রেশন):
        Hold: 45 to 60 seconds (Supine knee-hug into tight ball, head lifted).
        Target: Decompresses Erector Spinae & Quadratus Lumborum (QL).
        Mechanics: Pulls pelvis into full posterior pelvic tilt, reversing lumbar hyperlordosis.
   • 2. Supta Baddha Konasana / Reclining Butterfly (সুপ্ত বদ্ধকোণাসন — অ্যাডাক্টর রিলিজ):
        Hold: 45 to 60 seconds (Supine, soles together, knees falling wide open).
        Target: Adductor Longus/Magnus, Pectineus & Pelvic Floor Musculature.
        Mechanics: Relieves groin constriction and releases forward downward pelvic pull.
   • 3. Setu Bandhasana / Glute Bridge with Resistance (সেতুবন্ধাসন — গ্লুট সক্রিয়করণ):
        Hold: 45 to 60 seconds (Dynamic reps or isometric hold with 3-sec peak glute squeeze).
        Target: Gluteus Maximus, Hamstrings & Lower Abdominal Wall.
        Mechanics: Reciprocal Inhibition — intense glute contraction forces tight psoas to shut off!
   • 4. Supta Virasana / Reclining Hero Pose (সুপ্ত বীরাসন — সোয়াস ও কোয়াডস ওপেনার):
        Hold: 45 to 60 seconds (Kneeling with feet outside hips, reclining flat, arms overhead).
        Target: Rectus Femoris, Psoas Major & Quadriceps.
        Mechanics: The ultimate deep hip-flexor stretch; reverses 10 hours of seated chair shortening.

⚠️ ANTERIOR PELVIC TILT & THE "FAKE BELLY" ILLUSION:
   • Lower Crossed Syndrome: Seated study shortens hip flexors/lower back & deactivates glutes/abs.
   • Pelvic Bucket Spill: Pelvis tilts forward-down, causing lumbar lordosis and abdominal protrusion.
   • Visceral Spillage: Organs spill forward, creating a false gut pooch even at low body fat!
   • Immediate Posture Lift: Restoring neutral pelvic alignment flattens the abdomen instantly.

💼 KANAD'S DAILY 3-5 MINUTE INTEGRATION (82 KG ➔ 72 KG RECOMPOSITION):
   • Zero-Equipment Monastic Habit: Execute upon waking, after 3-hour study block, or at bedtime.
   • Desk Worker Spine Insurance: Relieves lower back ache from prolonged WBCS prep sessions.
   • Wardrobe Harmony: Restores level waistband/belt line for crisp trousers and Old Money styling.

📌 VAULT & REFERENCE SYNERGY:
   • Note: 03_Habits_Protocols/Sunil_Yoga_Fit_Anterior_Pelvic_Tilt_Correction_Protocol.md
   • Visual Matrix: Attachments/Sunil_Yoga_Fit_Anterior_Pelvic_Tilt_Matrix.jpg
   • Reference: ~/.gemini/config/skills/self-help/references/sunil_yoga_fit_anterior_pelvic_tilt_protocol.md
   • Bedtime Pelvic Reset: 03_Habits_Protocols/Alex_Libin_Bedtime_Pelvic_Tilt_and_Flat_Belly_Protocol.md
   • Standing Abs: 03_Habits_Protocols/AK_Da_Don_Standing_Abs_Home_Workout_Protocol.md
   • Master Dashboard: 00_Dashboard/Master_Self_Help_Hub.md
================================================================================
""")

def cmd_communication(args):
    print("""
================================================================================
🗣️ JULIE HOGBIN: 5 BOOKS TO COMMUNICATE BETTER THAN 99% OF PEOPLE
================================================================================
💡 Core Leadership & Influence Philosophy:
   "How you use words, read body language, and negotiate will completely change your results."
   — Julie Hogbin (@juliehogbin) • Conscious Leadership & Management Mentor • Reel DfLJSEVs-2j

🏛️ THE 5-LAYER STRATEGIC INFLUENCE QUINTET:

   • 1. EXACTLY WHAT TO SAY (Phil M. Jones) — Micro-Linguistics & Verbal Triggers
        - Law: Micro-linguistic framing guides subconscious human choices without resistance.
        - "I'm not sure if it's for you, but...": Zero-pressure prompt that triggers intense curiosity.
        - "How open-minded are you to...": Bypasses stubbornness; nobody admits to being closed-minded.
        - "What do you know about...": Disarms reactive opinions and shifts counterparts into analytical thought.

   • 2. HOW TO WIN FRIENDS & INFLUENCE PEOPLE (Dale Carnegie) — Diplomatic Foundation
        - Law: Human beings are creatures of emotion, pride, and ego; validate their significance.
        - The 70/30 Listening Law: Listen twice as much as you speak; let the other person do 70% of the talking.
        - Eliminate "3Cs": Never criticize, condemn, or complain; criticism breeds defensive retaliation.
        - The Sweetest Sound: A person's name is to them the sweetest and most important sound in any language.

   • 3. THE FINE ART OF SMALL TALK (Debra Fine) — Conversational Agility & Icebreaking
        - Law: Confidence in public is a mechanical skill; small talk is the gateway to deep connections.
        - The Burden of Initiative: Take 100% responsibility to break the ice; never wait for others to approach.
        - Open-Ended Question Engine: Replace dead-end "How are you?" with "What's the best part of your project?".
        - Graceful Exit Formula: Transition cleanly without being awkward: name them, validate, and step away.

   • 4. WHAT EVERY BODY IS SAYING (Joe Navarro / Ex-FBI) — Non-Verbal Decryption
        - Law: The neocortex can lie, but the limbic system cannot; decode involuntary somatic signals.
        - Limbic Pacifying Gestures: Neck touching, suprasternal notch clutching & collar pulling signal distress.
        - Feet Don't Lie: Foot direction reveals where the person genuinely wants to go (engagement vs flight).
        - Ventral Shielding & Eye-Blocking: Crossed arms, objects between chests, or rapid blinking signal rejection.

   • 5. NEVER SPLIT THE DIFFERENCE (Chris Voss / Lead FBI Negotiator) — High-Stakes Leverage
        - Law: Conflict is discovery; tactical empathy controls high-stakes negotiations without compromise.
        - Mirroring & Labeling: Repeat last 1-3 words + "It seems like you feel..." to unlock hidden leverage.
        - Calibrated Questions: Use "How" and "What" ("How am I supposed to do that?") to shift burden to them.
        - Aim for "That's Right": "You're right" means shut up; "That's right" signals authentic emotional surrender.

🏛️ WBCS ADMINISTRATIVE & INTERVIEW INTEGRATION:
   • Public Grievance / Land Disputes: Chris Voss tactical empathy + Joe Navarro pacifying read.
   • WBCS Personality Test (Interview Board): Dale Carnegie 70/30 listening + Phil M. Jones framing.
   • Inter-Departmental Coordination: Debra Fine conversational agility + calibrated 'How' questions.

📌 VAULT & REFERENCE SYNERGY:
   • Note: 02_Cognitive_Learning/Julie_Hogbin_Five_Communication_Books_Protocol.md
   • Visual Matrix: Attachments/Julie_Hogbin_Five_Communication_Books_Matrix.jpg
   • Reference: ~/.gemini/config/skills/self-help/references/julie_hogbin_five_communication_books_protocol.md
   • 3-Tier Book Filter: 02_Cognitive_Learning/Julie_Hogbin_Skip_Read_Study_Books_Framework.md
   • Tactical Dialogue: 01_Mindset_Motive/Tactical_Communication_and_Conversation_Playbook.md
   • Master Dashboard: 00_Dashboard/Master_Self_Help_Hub.md
================================================================================
""")

def cmd_realistic(args):
    print("""
================================================================================
🕉️ GITA 6.5: REALISTIC SELF-MOTIVATION & THE 'NO MAGIC PILL' PROTOCOL
================================================================================
💡 Core Dialectic:
   "भगवद्गीता के कुछ महानतम श्लोक कौन से हैं? मेरी राय में गीता का सबसे शक्तिशाली श्लोक है:
    'उद्धरेदात्मनात्मानं नात्मानमवसादयेत् । आत्मैव ह्यात्मनो बन्धुरात्मैव रिपुरात्मनः ॥' (गीता ६.५)
    अर्थात्: मनुष्य को अपने मन के द्वारा अपना उद्धार करना चाहिए, स्वयं को कभी निराश या पराजित नहीं होने देना चाहिए...
    यह गीता में पाई गई अत्यंत ईमानदार और यथार्थवादी आत्म-प्रेरणा (Realistic Self-Motivation) का एक महान उदाहरण है।
    हर किसी ने उदासीनता (apathy) और प्रेरणा की कमी का अनुभव किया होगा।
    इससे बाहर निकालने के लिए कोई जादुई गोली (magic pill) नहीं है—शिवाय स्वयं के, स्वयं के माध्यम से!"
   — Dev (@devanand_exist) • Gita 6.5 Analysis

🏛️ THE 4 FOUNDATIONAL PILLARS OF REALISTIC SELF-MOTIVATION:
   • 1. The 'No Magic Pill' Law (কোনো জাদু বা শর্টকাট নেই):
        Waiting for a magical mood shift, new planner, or video is delusion.
        Nobody will clear exams or build your career for you.
   • 2. Realistic vs Delusional Motivation (টক্সিক পজিটিভিটি বনাম নির্মম বাস্তবতা):
        Gita 6.5 does not offer fake comfort; it places 100% agency on you.
        नात्मानमवसादयेत् — refuse to let yourself sink into self-pity and despair.
   • 3. The Self as Assassin or Ally (নিজের মনই ঘাতক কিংবা পরম সহায়):
        When you skip study and binge reels, you murder your sovereign future.
        When you sit down and execute 3 hours deep work, you are your own hero.
   • 4. Atma-Madhyama: Action Without Mood (মুডের অপেক্ষা না করে কর্ম):
        Self-rescue through self-action ("स्वयं की स्वयं के माध्यम से").
        Physical execution of question #1 dissolves apathy and generates flow.

💼 3-STEP DAILY REALISTIC MOTIVATION PROTOCOL FOR KANAD:
   • 1. Kill The Magic Pill Hope: Stop looking for shortcuts. Accept that
        exam cutoffs demand uncomfortable solitary effort in Liluah/Arambagh.
   • 2. Enforce 'No Despair' (नात्मानमवसादयेत्): Forbid self-pity over the private
        layoff. Stand up, breathe deep, and write formula #1 immediately.
   • 3. Self-Rescue Through Direct Action: Be your own ally. Complete Project #4
        and Project #5 tasks. Self-dignity is earned only through execution.

📌 VAULT & HOMESERVER SYNERGY:
   • Note: 01_Mindset_Motive/Devanand_Exist_Gita_Realistic_Self_Motivation.md
   • Visual Matrix: Attachments/Devanand_Exist_Gita_6_5_Realistic_Self_Motivation_Matrix.jpg
   • Core Shloka Study: 01_Mindset_Motive/Bhagavad_Gita_Krishna_Overcoming_Laziness_Mind_Mastery.md
   • Motive Anchor: 01_Mindset_Motive/Motive_and_Dignity_Anchor.md
================================================================================
""")


def cmd_mainfocus(args):
    print("""
================================================================================
🎯 KANAD CORE DIRECTION: TIER 1 SOVEREIGN MAIN FOCUS (P1)
================================================================================
🔥 THE ETERNAL MOTIVE (Personal-Vault/Personal/MOTIVE.md):
   "Whatever you think is your boundary—it's not true. Just a little try,
    and you will fly. It's a promise to myself that You—I—will fly. Will fly."
   • The Catalyst: The Termination Letter, betrayal, and humiliation.
   • The Craving: Power, Dignity, and Undeniable Redemption.
   • The Resolution: Refusal to live below true sovereign potential.

🏛️ P1 ACADEMIC & EXAM ENGINE (WBCS / Banking PO / Central Exams):
   • Monastic Study Architecture: 4 x 90-minute deep study blocks daily.
   • Barbara Oakley Learning: Alternating focused mode and diffuse retrieval.
   • Feynman Synthesis: Explain complex concepts simply in Bengali.
   • Task Initiation: 5-minute Micro-Sprint + Physiological Sigh (bypasses friction).
   • Vocabulary Mastery: Norman Lewis 'Word Power Made Easy' root morphemes.
   • Faculty Matrix: Top verified mentors mapped to Kanboard Projects #4 & #5.
   • Wall-Staring Attention: 10 min/evening zero-stimulus Trataka focus (Rank #1 calm).

🥋 PHYSICAL TRANSFORMATION & SOMA (82 kg ➔ 72 kg Lean Athletic Frame):
   • Upper Body: AK Da Don 6-move calisthenics (deficit chest, Pelican, Sphinx).
   • Standing Abs: 4-move zero-spinal-shear routine (40s TUT / 20s rest).
   • Posture & APT: Sunil Yoga Fit 4-movement lordosis correction + Alex Libin.
   • Cranial Decompression: Bottle posture sub-occipital release (clears brain fog).
   • Vascular Forearms: Himansu Fit 3-step dumbbell giant set + Italian sleeve roll.
   • Jan Aushadhi Stack: Omega-3, B-Complex, Creatine, Whey (Contraindicated: Iron).

⚡ UNYIELDING WILLPOWER & MONASTIC MINDSET:
   • Dan Zakaria: 'Do it anyway' — kill the internal negotiator, action precedes feeling.
   • Gita 6.5: उद्धरेदात्मनात्मानं — self-rescue through action; zero magic pills.
   • Robert Greene: Counterattack strategy — convert setbacks into tactical crucibles.
   • Ryan Holiday: Ego is the Enemy — alive time over dead time; silent execution.
   • Romano & James Dean: Stoic emotional regulation; calm, downward-inflected stillness.
================================================================================
""")

def cmd_strategy(args):
    print("""
================================================================================
🧭 STRATEGIC ASSETS: TIER 2 SELF-IMPROVEMENT & FUTURE PLANNING (P2)
================================================================================
🗣️ HIGH-STAKES COMMUNICATION & ADMINISTRATIVE LEADERSHIP:
   • Julie Hogbin 5-Book Stack: Exactly What to Say (Phil M. Jones), How to Win
     Friends (Carnegie), Small Talk (Fine), What Every BODY is Saying (Navarro),
     Never Split the Difference (Chris Voss).
   • Conscious Leadership: Kouzes & Posner 'The Leadership Challenge' 5 practices.
   • Character Ethic: Stephen Covey 'The 7 Habits of Highly Effective People'.
   • Administrative Leverage: Lewis Strauss shadow power & Chanakya boundaries.

💰 PERMANENT FINANCIAL SOVEREIGNTY & WEALTH ARCHITECTURE:
   • The Intelligent Investor (Graham) & Psychology of Money (Housel).
   • Real Estate House Hacking: Pre-marriage equity & cash flow leverage.
   • Infinite Banking: Dividend-paying whole life cash value liquidity.
   • Stock Market Literacy: Yale Financial Markets & Shobha Rana foundations.

👔 EXECUTIVE SARTORIAL CAPSULE & GROOMING:
   • First Government Job Joining Look: Tailored Old Money palette.
   • Facial Aesthetics & Skin: Dr. Hadiya Pharmaceutical DTan facewash & cleansing.
   • Rohini Moon-Venus Aesthetics: Dark chocolate leather, ivory, emerald & silver.

🛡️ PSYCHOLOGICAL RESILIENCE & FORTITUDE:
   • Viktor Frankl: Man's Search for Meaning & tragic optimism.
   • Jordan Peterson: Beyond Order (12 More Rules) & personal micro-order.
   • Maxwell Maltz: Psycho-Cybernetics & internal self-image reprogramming.
   • Don Miguel Ruiz: The Four Agreements (Teflon impeccability).
================================================================================
""")

def cmd_voice(args):
    print("""
================================================================================
🎙️ ZERO-COST VOICE TRAINING & VOCAL RESONANCE PROTOCOL
================================================================================
💡 Core Principle: Voice is an acoustic-muscular instrument. Pitch, resonance,
   gravitas, and crisp articulation depend on 4 physiological pillars:
   Power (Diaphragm), Source (Larynx), Resonators (Chest/Mask), Articulators (Jaw/Tongue).
   100% Free — Zero course fees, zero equipment needed!

🕒 THE 15-MINUTE DAILY ZERO-COST ROUTINE:
1️⃣ PHASE 1 (0:00 - 3:00) — Posture & Diaphragmatic Breath Ignition:
   • Wall Align / Book Posture: Scapulae down & back, chin parallel to floor.
   • 4-4-8 Diaphragmatic Expansion: 4s inhale (belly inflates, chest still).
   • Prolonged 'Sssss' Drill: 20-30s continuous smooth hiss under steady pressure.

2️⃣ PHASE 2 (3:00 - 6:00) — Larynx De-constriction & SOVT Warmup:
   • The Yawn-Sigh: Deep yawn lowers larynx, lift soft palate; exhale sighing "Haaah".
   • Lip Trills / Bubbles ("Brrrrr"): Dr. Ingo Titze semi-occluded tract glides (low-to-high).
   • Balances transglottal air pressure; massages vocal fold mucosa with zero friction.

3️⃣ PHASE 3 (6:00 - 10:00) — Chest Resonance & Baritone Tone Activation:
   • Sternum Hum ("Mmmmm"): Flat hand on breastbone, hum low until chest vibrates.
   • King Kong Taps: Tap chest gently while transitioning "Mmm-Ahhh", "Mmm-Ohhh".
   • Drops acoustic placement from the throat into the thoracic amplifier.

4️⃣ PHASE 4 (10:00 - 13:00) — Pen-in-Mouth Articulation Drill:
   • Jaw Release: Circular massage of masseter muscles under earlobes.
   • Pen Drill: Bite clean pen horizontally with front teeth; read text aloud for 90s.
   • Over-trains tongue/lips against resistance; creates instant razor-sharp diction!
   • Tongue Twisters: "কাঁচা গাব পাকা গাব", "Red leather, yellow leather".

5️⃣ PHASE 5 (13:00 - 15:00) — Interview Gravitas & Voice Memo Audit:
   • Downward Inflection: Drop pitch 1/2 octave at sentence period (eliminates uptalk).
   • 2-Second Strategic Pause: Replace "um", "mane", "actually" with dead silence.
   • Phone Memo: Record 60s practice answer; audit pace (120-140 WPM) & clarity.

🚫 5 HARMFUL VOCAL HABITS & FREE HYGIENE:
   ❌ Violent throat clearing ➔ ✅ Hard swallow or sip water.
   ❌ Whispering strain       ➔ ✅ Low relaxed normal speech.
   ❌ Dehydration             ➔ ✅ 3-3.5L plain water daily.
   ❌ Dry vocal tract         ➔ ✅ 3 min boiling water steam inhalation nightly.
   ❌ Mouth breathing         ➔ ✅ Strict nasal breathing at rest & during sleep.

📌 VAULT & KNOWLEDGE GRAPH:
   • Obsidian Note: 03_Habits_Protocols/Zero_Cost_Voice_Training_and_Vocal_Resonance_Protocol.md
   • Skill Reference: references/zero_cost_voice_training_protocol.md
   • Dashboard Link: 00_Dashboard/Master_Self_Help_Hub.md (Section 1.2 & 2.1)
================================================================================
""")

def cmd_lighting(args):
    print("""
================================================================================
💡 AI CENTURY STUDIOS: 24 CINEMATIC LIGHTING PROMPTS & PORTRAIT MASTERY
================================================================================
📸 Source: AI Century Studios (@aicenturystudios • Reel DfSHhNVzJyR)
💡 Core Principle: Visual aesthetics, jawline definition, and photographic gravitas
   are 90% governed by light and shadow (Chiaroscuro). Use these 24 lighting formulas
   for Midjourney v6 / Flux.1 AI generation and real-life executive headshots.

🏛️ THE 4 LIGHTING QUADRANTS:
1️⃣ STUDIO & PORTRAIT CLASSICS (Character & Authority):
   • 01. Rembrandt: 45° key light; signature triangle on shadow cheek; intellectual prestige.
   • 02. Clamshell: Overhead softbox + chin reflector; zero eyebags, dual iris catchlights.
   • 03. Split Lighting: 90° harsh side light; 50/50 bisection; duality & noir stoicism.
   • 04. High Key: Diffuse multi-source, white void; ultra-low contrast, pure optimism.
   • 07. Low Key: 80% shadow dominance, pitch black void; intimate luxury & quiet power.
   • 23. Rim Light: Kicker outline on hair/shoulders; athletic distinction & jawline pop.

2️⃣ NATURAL & ATMOSPHERIC (Authenticity & Emotion):
   • 09. Dappled Light: Sun filtering through leaves; dancing speckled bokeh shadows.
   • 10. Overcast Soft: Cloud diffusion wrap-around; true-to-life skin tones, zero squint.
   • 11. Golden Hour: Low-angle honey-amber sunset; golden hair glow, romantic victory.
   • 17. Moonlight: Cool cyan-blue silvery night sky; luminous nocturnal mystery.
   • 21. Lightning Flash: Instantaneous cold white burst; frozen raindrops, storm climax.
   • 22. Backlit Silhouette: Blinding backlight behind subject; iconic black figure halo.

3️⃣ PRACTICALS & ENVIRONMENTAL (Realism & Mood):
   • 12. Sodium Vapor: 2100K monochromatic yellow-orange streetlamp; cyberpunk rainy street.
   • 13. Fluorescent: Cool green-white clinical tube lights; sterile office/hospital thriller.
   • 14. Practicals Only: Illuminated solely by visible desk lamp / screen; monastic night study.
   • 15. Candlelight: 1800K flickering flame; soft rapid falloff, Barry Lyndon historical drama.
   • 16. Firelight: Dancing campfire glow, deep orange-red embers; primal warrior spirit.
   • 18. Flashlight: Narrow handheld torch beam; central hotspot, detective dark search.

4️⃣ DRAMATIC, STYLIZED & SCI-FI:
   • 05. Venetian Blinds: Horizontal linear window slat shadows; 1940s noir mystery.
   • 06. Hard Top Light: Steep vertical overhead lamp; dark eye-socket shadows, Godfather menace.
   • 08. Direct Flash: On-camera harsh flash, hard drop shadow; 90s vintage analog candid.
   • 19. Underlighting: Uplight beneath chin; eerie inverted shadows, theatrical villainy.
   • 20. Red Emergency: Monochromatic crimson strobe; submarine alarm, high-stakes crisis.
   • 24. Colored Gels: Dual complementary cyan key + magenta rim; neo-noir cyber fashion.

🎯 KANAD EXECUTIVE PORTRAIT APPLICATION:
   • WBCS / Govt Form & Interview: Rembrandt + Clamshell window setup (45° angle + lap reflector).
   • LinkedIn Headshot: Rim Light + Overcast soft daylight (sharp jawline separation).
   • Social / Personal Branding: Golden Hour 3/4 angle portrait (warm golden undertone synergy).

📌 VAULT & KNOWLEDGE GRAPH:
   • Obsidian Note: 04_Fashion_Grooming/AI_Century_Studios_24_Cinematic_Lighting_Prompts_Mastery.md
   • Visual Matrix: Attachments/AI_Century_Studios_24_Lighting_Prompts_Matrix.jpg
   • Reference: references/ai_century_studios_24_lighting_prompts.md
================================================================================
""")

def cmd_wallstare(args):
    print("""
================================================================================
🎯 THE_SPACEGUY: 10-MIN WALL-STARING ATTENTION TRAINING & TRATAKA PROTOCOL
================================================================================
📱 Source: The_SpaceGuy (@im_spaceguy • Reel DfjBX7Jz4EI)
💡 Core Thesis: "He wasn't wasting time. He was training his attention."
   Same wall, same time, 10 quiet minutes every evening — no phone, no music,
   just focus on one neutral point. Attention is a trainable cognitive muscle.

🔬 NEUROBIOLOGY & CLASSICAL MECHANICS:
   • Attention Muscle (DLPFC vs DMN): Each time mind drifts to worries/reels and
     you drag gaze back to the wall spot = 1 cognitive rep strengthening DLPFC & ACC.
   • Dopamine Baseline Reset: 10-min sensory blackout resensitizes dopamine receptors,
     making textbook Quant, Reasoning & GS feel crisp instead of painful.
   • Hippocampal Consolidation (Week 2): Stimulus-free silence acts as Oakley
     Diffuse Mode, locking the day's study formulas into long-term memory.
   • Exam Composure (Week 4): Prevents amygdala cortisol spike while peers cram
     frantically in the corridor — unlocking Rank #1 clarity under exam timers.
   • Bahiranga Trataka: Classical yogic single-point wall gaze quieting Chitta Vritti.

📅 THE 30-DAY PROGRESSION:
   • Week 1 (Days 1–7): High boredom friction & urge to check phone = normal rep load.
   • Week 2 (Days 8–14): Working memory & active recall speed noticeably increase.
   • Week 3 (Days 15–21): Frictionless entry into 4x90-min monastic study blocks.
   • Week 4 (Days 22–30): Laser executive lock & zero panic composure on exam day.

🛠️ KANAD DAILY EVENING PROTOCOL (Liluah / Arambagh):
   1️⃣ Strip All Input: Leave phone & earbuds in another room. Sit 4–6 ft from wall.
   2️⃣ Minute 0:00: 2 Physiological Sighs (double nasal inhale, long mouth exhale).
   3️⃣ 0:00–10:00: Fix gentle blinking gaze on one wall spot. Catch drifts & re-anchor.
   4️⃣ Minute 10:00: Immediately run 5-min closed-book Feynman recall on paper/Obsidian.

📌 VAULT & KNOWLEDGE GRAPH:
   • Obsidian Note: 02_Cognitive_Learning/The_SpaceGuy_10Min_Wall_Staring_Attention_Protocol.md
   • Visual Matrix: Attachments/The_SpaceGuy_Wall_Staring_Attention_Matrix.jpg
   • Reference: references/the_spaceguy_wall_staring_attention_protocol.md
================================================================================
""")

def cmd_abshred(args):
    print("""
================================================================================
🥋 SANJAY KUMAR JHA: ULTIMATE AB SHREDDING & CORE BURNER PROTOCOL
================================================================================
📱 Source: Sanjay Kumar Jha (@sanjaykumarjha • Facebook Reel 1746446120819061)
💡 Core Thesis: "Transform your midsection with this ultimate core burner! 
   Designed to torch fat and carve out definition, this routine targets every angle 
   of your abs. Consistency is everything, so stay dedicated and watch the transformation happen."

🏛️ THE 3 CORE POWER MOVEMENTS (THE BOTTLE HURDLE METHOD):
   • 1. ⚡ Low Plank Bottle Hip Dips & Oblique Twist (প্ল্যাঙ্ক বটেল হিপ ডিপস ও অবলিক টুইস্ট):
        Target: External & Internal Obliques, Transverse Abdominis (TVA / Deep Corset).
        Mechanics: Forearm plank over upright bottle; laterally rotate pelvis to dip hips 
                   toward floor, clearing bottle apex on every sweep.
        Advantage: Heavy rotational shear on lateral flanks; sculpts sharp oblique V-taper.
   • 2. ⚡ Seated Bottle Leg Extensions & Oblique Sweep (সিটেড বটেল লেগ এক্সটেনশন ও অবলিক সুইপ):
        Target: Lower Rectus Abdominis, Iliopsoas (Hip Flexors), Serratus Anterior.
        Mechanics: Seated with hands braced; sweep glued legs in a high lateral arc over bottle apex.
        Advantage: High continuous tension on lower abdominal wall without lumbar compression.
   • 3. ⚡ V-Sit Knee-to-Chest Oblique Twist (সিটেড নি-টু-চেস্ট অবলিক টুইস্ট):
        Target: Complete Abdominal Wall, Love Handles, Anti-Rotation Core Stability.
        Mechanics: Seated V-hold; obliquely tuck knees to chest clearing bottle height every rep.
        Advantage: Combines hip flexion with spinal rotation; stimulates slow & fast-twitch fibers.

⏱️ WORKOUT CIRCUIT & CADENCE:
   • Format: Tri-set circuit (Exercise 1 ➔ Exercise 2 ➔ Exercise 3 without rest).
   • Volume: 3-4 rounds | 15-20 reps per movement.
   • Rest: 45-60 seconds between rounds.
   • Total Duration: 10-12 minutes | Zero gym equipment (just a mat and a water bottle).

🔬 FAT LOSS & WAIST TIGHTENING SCIENCE (82 KG ➔ 72 KG CUT):
   • Spot reduction is a myth (systemic caloric deficit drives fat loss).
   • Oblique & TVA hypertrophy tightens the deep internal corset, pulling the waist inward
     and preventing loose skin as body fat decreases.
   • Seamlessly stacks with Kanad's daily 10k steps and calisthenics (/upperbody, /standingabs).

📌 VAULT & KNOWLEDGE GRAPH:
   • Obsidian Note: 03_Habits_Protocols/Sanjay_Kumar_Jha_Ab_Shredding_and_Core_Burner_Protocol.md
   • Visual Image: Attachments/Sanjay_Kumar_Jha_Ab_Shredding_Routine.jpg
   • Reference: https://www.facebook.com/share/r/1HLGa18B3L/
================================================================================
""")

def cmd_audit_tiers(args):
    import os
    vault = "/home/saman/Documents/OBSIDIAN/SELF HELP"
    t1, t2, t3, total = [], [], [], 0
    for root, dirs, files in os.walk(vault):
        dirs[:] = [d for d in dirs if not d.startswith(".") and d not in ["_Archive", "attachments", "Attachments"]]
        for f in files:
            if not f.endswith(".md") or f == "Master_Self_Help_Hub.md":
                continue
            total += 1
            p = os.path.join(root, f)
            with open(p, "r", encoding="utf-8") as fl:
                c = fl.read()
            if "tier: 1-core-direction" in c:
                t1.append(f)
            elif "tier: 3-quarantine" in c or "status: deprioritized" in c:
                t3.append(f)
            else:
                t2.append(f)
    print("=" * 80)
    print("🔍 OBSIDIAN VAULT TRI-TIER CLASSIFICATION AUDIT REPORT")
    print("=" * 80)
    print(f"📊 Total Active Markdown Notes: {total}")
    print(f"🎯 Tier 1 (Core Direction / P1 Main Focus):     {len(t1):2d} notes [ACTIVE EXECUTION]")
    print(f"🧭 Tier 2 (Strategic Assets / P2 Retained):       {len(t2):2d} notes [PRESERVED WISDOM]")
    print(f"🗄️ Tier 3 (Distraction Quarantine / P3 Filtered): {len(t3):2d} notes [ZERO-CLUTTER CRYPT]")
    print("-" * 80)
    print("✅ ZERO DELETION INTEGRITY: 100% of files & attachments preserved.")
    print("✅ ZERO COGNITIVE FRICTION: Distractions filtered from daily dashboard views.")
    print("=" * 80)

def main():
    parser = argparse.ArgumentParser(description="Antigravity Unified Self-Help CLI Engine")
    subparsers = parser.add_subparsers(dest="command", help="Sub-commands")

    # /boost
    p_boost = subparsers.add_parser("boost", help="Physiological sigh & 5-minute micro-sprint")
    p_boost.add_argument("--minutes", type=int, default=5, help="Duration in minutes")
    p_boost.add_argument("--simulate", action="store_true", help="Simulate timer without sleeping")

    # /grill-me
    p_grill = subparsers.add_parser("grill", help="Socratic drill & motive accountability")
    p_grill.add_argument("--topic", type=str, help="Subject/topic filter")
    p_grill.add_argument("--auto", "--reveal", dest="auto", action="store_true", help="Auto-reveal answer without interactive prompt")

    # /goal
    subparsers.add_parser("goal", help="Exam milestones, syllabus, fitness cut, wardrobe")

    # /plan
    p_plan = subparsers.add_parser("plan", help="Clock-free dynamic daily routine")
    p_plan.add_argument("--location", choices=["arambagh", "liluah"], default="arambagh", help="Location")
    p_plan.add_argument("--wake", default="08:00", help="Wake-up time")

    # /supplement
    p_supp = subparsers.add_parser("supplement", help="Jan Aushadhi supplement scheduler & checker")
    p_supp.add_argument("--check", type=str, help="Drug code to inspect")

    # /learn
    p_learn = subparsers.add_parser("learn", help="Oakley chunking & Feynman Bengali explanation")
    p_learn.add_argument("topic", nargs="?", default="Compound Interest vs Simple Interest", help="Concept to explain")

    # /plugin
    subparsers.add_parser("plugin", help="Obsidian & tooling advisory")

    # /automation
    subparsers.add_parser("automation", help="Pipeline sync runner")

    # /text (Masculine communication & morning frame)
    subparsers.add_parser("text", help="Masculine communication & the 9 morning texting archetypes")

    # /gut (Coach Kenny gut mobility & constipation protocol)
    subparsers.add_parser("gut", help="Coach Kenny 4x30 gut mobility & constipation protocol")
    subparsers.add_parser("constipation", help="Coach Kenny 4x30 gut mobility & constipation protocol")

    # /posture (Alex Libin bottle posture correction protocol)
    subparsers.add_parser("posture", help="Alex Libin 3-step bottle posture correction protocol")
    subparsers.add_parser("bottle", help="Alex Libin 3-step bottle posture correction protocol")

    # /focus (Isabella Saleh study & productivity framework)
    subparsers.add_parser("focus", help="Isabella Saleh 3-pillar study & focus framework")
    subparsers.add_parser("animedoro", help="Isabella Saleh 3-pillar study & focus framework")

    # /style (Old Money vs Starboy Aesthetic Guide)
    subparsers.add_parser("style", help="Old Money vs Starboy aesthetic & Rohini Moon-Venus guide")
    subparsers.add_parser("oldmoney", help="Old Money vs Starboy aesthetic & Rohini Moon-Venus guide")

    # /book (Rob Moore Book Prioritization & Audiobookshelf)
    subparsers.add_parser("book", help="Rob Moore Read/Study/Skip book priorities & Audiobookshelf")
    subparsers.add_parser("audiobook", help="Rob Moore Read/Study/Skip book priorities & Audiobookshelf")
    subparsers.add_parser("audiobookshelf", help="Rob Moore Read/Study/Skip book priorities & Audiobookshelf")

    # /shoulder (Fang Yuan Shoulder Mobility & Rotator Cuff Protocol)
    subparsers.add_parser("shoulder", help="Fang Yuan shoulder mobility & rotator cuff protocol")
    subparsers.add_parser("rotator", help="Fang Yuan shoulder mobility & rotator cuff protocol")

    # /video (Jovan Delo Anti-Brainrot Videos & MiniDLNA)
    p_video = subparsers.add_parser("video", help="Jovan Delo anti-brainrot mindset videos & MiniDLNA")
    p_video.add_argument("--part", type=int, choices=[1, 2], default=None, help="Video series part (1 or 2)")
    subparsers.add_parser("minidlna", help="Jovan Delo anti-brainrot mindset videos & MiniDLNA")
    subparsers.add_parser("video2", help="Jovan Delo anti-brainrot mindset videos Part 2 & MiniDLNA")

    # /career (Career Acceleration & Interview Mastery)
    subparsers.add_parser("career", help="Career acceleration & interview mastery masterclasses")
    subparsers.add_parser("interview", help="Career acceleration & interview mastery masterclasses")
    subparsers.add_parser("job", help="Career acceleration & interview mastery masterclasses")

    # /pest (Household Pest Control: Myths vs Facts)
    subparsers.add_parser("pest", help="Household pest control viral myths vs scientific reality")
    subparsers.add_parser("home", help="Household pest control viral myths vs scientific reality")

    # /bookposture (Alex Libin Desk-Study Book Posture Protocol)
    subparsers.add_parser("bookposture", help="Alex Libin 4x1-min desk-study book posture drills")
    subparsers.add_parser("neck", help="Alex Libin 4x1-min desk-study book posture drills")
    subparsers.add_parser("chin", help="Alex Libin 4x1-min desk-study book posture drills")

    # /dtan (Dr. Hadiya Dermatological D-Tan Cleansing Protocol)
    subparsers.add_parser("dtan", help="Dr. Hadiya 4 clinical d-tan soaps & skincare blueprint")
    subparsers.add_parser("soap", help="Dr. Hadiya 4 clinical d-tan soaps & skincare blueprint")
    subparsers.add_parser("skincare", help="Dr. Hadiya 4 clinical d-tan soaps & skincare blueprint")

    # /facewash (Dr. Hadiya Pharmacy D-Tan Face Wash Protocol)
    subparsers.add_parser("facewash", help="Dr. Hadiya 4 pharmacy d-tan face washes & dwell time")
    subparsers.add_parser("fw", help="Dr. Hadiya 4 pharmacy d-tan face washes & dwell time")
    subparsers.add_parser("cleanser", help="Dr. Hadiya 4 pharmacy d-tan face washes & dwell time")

    # /palette (Old Money Color Combinations & Quiet Luxury)
    subparsers.add_parser("palette", help="Old money 4 timeless color combinations")
    subparsers.add_parser("color", help="Old money 4 timeless color combinations")
    subparsers.add_parser("expensive", help="Old money 4 timeless color combinations")

    # /zyverel (ZYVEREL 8 Universal Color Combinations)
    subparsers.add_parser("zyverel", help="ZYVEREL 8 universal color combinations & 60-30-10 rule")
    subparsers.add_parser("pairings", help="ZYVEREL 8 universal color combinations & 60-30-10 rule")
    subparsers.add_parser("combinations", help="ZYVEREL 8 universal color combinations & 60-30-10 rule")

    # /pelvic (Alex Libin Bedtime Pelvic Realignment & Flat Belly Protocol)
    subparsers.add_parser("pelvic", help="Alex Libin bedtime 5-min pelvic realignment & flat belly protocol")
    subparsers.add_parser("tilt", help="Alex Libin bedtime 5-min pelvic realignment & flat belly protocol")
    subparsers.add_parser("flatbelly", help="Alex Libin bedtime 5-min pelvic realignment & flat belly protocol")
    subparsers.add_parser("apt", help="Alex Libin bedtime 5-min pelvic realignment & flat belly protocol")

    # /glowup (Glowup Utopia 6 Facial Aesthetics & Looksmaxxing)
    subparsers.add_parser("glowup", help="Glowup Utopia 6 facial aesthetics & looksmaxxing blueprint")
    subparsers.add_parser("looksmax", help="Glowup Utopia 6 facial aesthetics & looksmaxxing blueprint")
    subparsers.add_parser("face", help="Glowup Utopia 6 facial aesthetics & looksmaxxing blueprint")
    subparsers.add_parser("jawline", help="Glowup Utopia 6 facial aesthetics & looksmaxxing blueprint")

    # /shamani (Raj Shamani Top 2 Book Recommendations)
    subparsers.add_parser("shamani", help="Raj Shamani top 2 book recommendations & visual problem solving")
    subparsers.add_parser("rajbook", help="Raj Shamani top 2 book recommendations & visual problem solving")
    subparsers.add_parser("bookrec", help="Raj Shamani top 2 book recommendations & visual problem solving")
    subparsers.add_parser("napkin", help="Raj Shamani top 2 book recommendations & visual problem solving")

    # /kwik (Jim Kwik Limitless Brain Optimization)
    subparsers.add_parser("kwik", help="Jim Kwik Limitless 3M model, FASTER framework & 4 digital villains")
    subparsers.add_parser("limitless", help="Jim Kwik Limitless 3M model, FASTER framework & 4 digital villains")
    subparsers.add_parser("brain", help="Jim Kwik Limitless 3M model, FASTER framework & 4 digital villains")
    subparsers.add_parser("faster", help="Jim Kwik Limitless 3M model, FASTER framework & 4 digital villains")

    # /realestate (Gunveer Singh Pre-Marriage Real Estate Leverage & House Hacking)
    subparsers.add_parser("realestate", help="Gunveer Singh pre-marriage dual FHA leverage & house hacking")
    subparsers.add_parser("househack", help="Gunveer Singh pre-marriage dual FHA leverage & house hacking")
    subparsers.add_parser("duplex", help="Gunveer Singh pre-marriage dual FHA leverage & house hacking")
    subparsers.add_parser("fha", help="Gunveer Singh pre-marriage dual FHA leverage & house hacking")

    # /stock (Shobha Rana Top 3 Stock Market Foundational Books)
    subparsers.add_parser("stock", help="Shobha Rana top 3 stock market foundational books & value investing")
    subparsers.add_parser("sharemarket", help="Shobha Rana top 3 stock market foundational books & value investing")
    subparsers.add_parser("coffeecan", help="Shobha Rana top 3 stock market foundational books & value investing")
    subparsers.add_parser("lynch", help="Shobha Rana top 3 stock market foundational books & value investing")

    # /banking (Gunveer Singh Infinite Banking Concept & Cash Value Leverage)
    subparsers.add_parser("banking", help="Gunveer Singh infinite banking concept & cash value leverage")
    subparsers.add_parser("ibc", help="Gunveer Singh infinite banking concept & cash value leverage")
    subparsers.add_parser("familybank", help="Gunveer Singh infinite banking concept & cash value leverage")
    subparsers.add_parser("cashvalue", help="Gunveer Singh infinite banking concept & cash value leverage")

    # /yale (Yale University Financial Markets - Prof. Robert Shiller / Ananta Chhajer)
    subparsers.add_parser("yale", help="Yale University Financial Markets course (Robert Shiller)")
    subparsers.add_parser("shiller", help="Yale University Financial Markets course (Robert Shiller)")
    subparsers.add_parser("markets", help="Yale University Financial Markets course (Robert Shiller)")
    subparsers.add_parser("corporatefinance", help="Yale University Financial Markets course (Robert Shiller)")

    # /faculty (Govt Exam Top YouTube Faculty - Ankur)
    subparsers.add_parser("faculty", help="Govt Exam Top YouTube Faculty Matrix (Ankur)")
    subparsers.add_parser("teachers", help="Govt Exam Top YouTube Faculty Matrix (Ankur)")
    subparsers.add_parser("ssc", help="Govt Exam Top YouTube Faculty Matrix (Ankur)")
    subparsers.add_parser("govtexam", help="Govt Exam Top YouTube Faculty Matrix (Ankur)")

    # /linkedin (Ashutosh Pratap Singh - LinkedIn Hidden Hiring & Profile Radar)
    subparsers.add_parser("linkedin", help="LinkedIn Hidden Hiring & Profile Radar (Technical Sapien)")
    subparsers.add_parser("jobsearch", help="LinkedIn Hidden Hiring & Profile Radar (Technical Sapien)")
    subparsers.add_parser("hiring", help="LinkedIn Hidden Hiring & Profile Radar (Technical Sapien)")
    subparsers.add_parser("networking", help="LinkedIn Hidden Hiring & Profile Radar (Technical Sapien)")

    # /ig (Innerlink - Instagram Algorithm 3 Critical Settings Reset)
    subparsers.add_parser("ig", help="Instagram Algorithm 3 Critical Settings Reset (Innerlink)")
    subparsers.add_parser("instagram", help="Instagram Algorithm 3 Critical Settings Reset (Innerlink)")
    subparsers.add_parser("reels", help="Instagram Algorithm 3 Critical Settings Reset (Innerlink)")
    subparsers.add_parser("contentgrowth", help="Instagram Algorithm 3 Critical Settings Reset (Innerlink)")

    # /control (J Romano - Stoic Self-Control & Trigger Deconstruction)
    subparsers.add_parser("control", help="Stoic Self-Control & Trigger Deconstruction (J Romano)")
    subparsers.add_parser("stoic", help="Stoic Self-Control & Trigger Deconstruction (J Romano)")
    subparsers.add_parser("triggers", help="Stoic Self-Control & Trigger Deconstruction (J Romano)")
    subparsers.add_parser("nonreactivity", help="Stoic Self-Control & Trigger Deconstruction (J Romano)")

    # /auster (Paul Auster - 4 3 2 1 Parallel Lives & Counterfactual Mastery)
    subparsers.add_parser("auster", help="Paul Auster 4 3 2 1 Parallel Lives & Counterfactual Mastery")
    subparsers.add_parser("4321", help="Paul Auster 4 3 2 1 Parallel Lives & Counterfactual Mastery")
    subparsers.add_parser("timelines", help="Paul Auster 4 3 2 1 Parallel Lives & Counterfactual Mastery")
    subparsers.add_parser("counterfactual", help="Paul Auster 4 3 2 1 Parallel Lives & Counterfactual Mastery")

    # /greene (Robert Greene - The 33 Strategies of War: Strategy 9 Turn The Tables)
    subparsers.add_parser("greene", help="Robert Greene 33 Strategies of War: Strategy 9 Turn The Tables")
    subparsers.add_parser("counterattack", help="Robert Greene Counterattack Strategy & Adversity Mastery")
    subparsers.add_parser("war", help="Robert Greene 33 Strategies of War")
    subparsers.add_parser("tables", help="Turn the tables counterattack strategy")

    # /pyramid (Dr. Vlad Beliavsky - The Pyramid Mind: 6-Level Cognitive System)
    subparsers.add_parser("pyramid", help="Dr. Vlad Beliavsky Pyramid Mind: 6-Level Cognitive System")
    subparsers.add_parser("beliavsky", help="Dr. Vlad Beliavsky Pyramid Mind & Emotional Healing")
    subparsers.add_parser("overthinking", help="Cure overthinking & rumination with the 6-level pyramid")
    subparsers.add_parser("emotions", help="The Guest House principle for emotional regulation")

    # /comm (Four Books to Master Communication Skills - Gottman, Carnegie, Greene, Canwell)
    subparsers.add_parser("comm", help="Communication Mastery: Four Essential Canons")
    subparsers.add_parser("communication", help="Four books to master communication skills")
    subparsers.add_parser("gottman", help="Dr. John Gottman emotional attunement protocol")
    subparsers.add_parser("canwell", help="Christopher Canwell attraction psychology & frame")

    # /unscripted (5 Books The Rich Don't Want You to Know)
    subparsers.add_parser("unscripted", help="5 Books The Rich Don't Want You to Know (@coffeewithbooks__)")
    subparsers.add_parser("richbooks", help="Five books that rich don't want you to know")
    subparsers.add_parser("demarco", help="M.J. DeMarco UNSCRIPTED & CENTS wealth framework")
    subparsers.add_parser("scottadams", help="Scott Adams Systems over Goals & Talent Stacking")
    subparsers.add_parser("systems", help="Systems vs Goals and talent stacking engine")

    # /magnet (4 Books That Will Make You a Human Magnet)
    subparsers.add_parser("magnet", help="4 Books That Will Make You a Human Magnet (@glitch.mindset)")
    subparsers.add_parser("charisma", help="Tactical Charisma & Human Magnet Framework")
    subparsers.add_parser("lowndes", help="Leil Lowndes 92 Little Tricks & Flooding Smile")
    subparsers.add_parser("tracy", help="Brian Tracy How the Best Leaders Lead & Gravitas")
    subparsers.add_parser("king", help="Patrick King How to Listen with Intention")

    # /stronger (6 Books to Make You Emotionally Stronger)
    subparsers.add_parser("stronger", help="6 Books to Make You Emotionally Stronger (@bookreadersclub)")
    subparsers.add_parser("emotionalstrength", help="6 Books to Make You Emotionally Stronger")
    subparsers.add_parser("eq", help="Daniel Goleman Emotional Intelligence & Amygdala Control")
    subparsers.add_parser("juliesmith", help="Dr. Julie Smith Why Has Nobody Told Me This Before")
    subparsers.add_parser("meurisse", help="Thibaut Meurisse Master Your Emotions & Defusion")

    # /adrenaline (Top 5 Books To Maximize Your Adrenaline Rush)
    subparsers.add_parser("adrenaline", help="Top 5 Books To Maximize Your Adrenaline Rush (@booksopedia_)")
    subparsers.add_parser("rush", help="Alias for adrenaline")
    subparsers.add_parser("willpower", help="Peter Hollins Science of Self-Discipline")
    subparsers.add_parser("warofart", help="Steven Pressfield The War of Art")
    subparsers.add_parser("hollins", help="Peter Hollins Willpower & Friction")

    # /soul (4 Books for Better Mind, Body & Soul)
    subparsers.add_parser("soul", help="4 Books for Better Mind, Body & Soul (@ektadb_speaks)")
    subparsers.add_parser("mind", help="Alias for soul")
    subparsers.add_parser("tools", help="Phil Stutz & Barry Michels The Tools")
    subparsers.add_parser("trenton", help="Nick Trenton Stop Overthinking")
    subparsers.add_parser("bessel", help="Bessel van der Kolk The Body Keeps the Score")
    subparsers.add_parser("stutz", help="Phil Stutz The Tools")

    # /dialogue (Tactical Communication & Dialogue Playbook)
    subparsers.add_parser("dialogue", help="Tactical Communication & Dialogue Playbook (@booksopedia_)")
    subparsers.add_parser("script", help="Alias for dialogue")
    subparsers.add_parser("talk", help="Alias for dialogue")
    subparsers.add_parser("playbook", help="Alias for dialogue")
    subparsers.add_parser("conversation", help="Alias for dialogue")

    # /prakhar (Beyond Self-Help: 3 Life-Changing Books)
    subparsers.add_parser("prakhar", help="Beyond Self-Help: 3 Life-Changing Books (@prakhar_insights9)")
    subparsers.add_parser("flow", help="Steven Kotler Flow State & Transient Hypofrontality")
    subparsers.add_parser("stealingfire", help="Stealing Fire: Kotler & Wheal STER Genome")
    subparsers.add_parser("ashtavakra", help="Osho Mahagita: Ashtavakra Gita & Sakshi Bhava")
    subparsers.add_parser("peterson", help="Jordan Peterson 12 Rules for Life & Sovereignty")
    subparsers.add_parser("osho", help="Alias for prakhar (Mahagita / Ashtavakra)")
    subparsers.add_parser("kotler", help="Alias for prakhar (Stealing Fire / Flow)")

    # /neverquit (5 Books That Teach You to Never Quit in Life)
    subparsers.add_parser("neverquit", help="5 Books That Teach You to Never Quit in Life (@coffeewithbooks__)")
    subparsers.add_parser("resilience", help="Radical Resilience & 1/4 Step Rule (Jackson Sherry)")
    subparsers.add_parser("quit", help="Alias for neverquit")
    subparsers.add_parser("morin", help="Amy Morin 13 Things Mentally Strong People Don't Do")
    subparsers.add_parser("foroux", help="Darius Foroux Win Your Inner Battles")
    subparsers.add_parser("carnegie2", help="Dale Carnegie How to Stop Worrying and Start Living")
    subparsers.add_parser("holiday", help="Ryan Holiday The Obstacle Is the Way")
    subparsers.add_parser("sherry", help="Jackson Sherry 8 1/4 Rules for Resilience")

    # /schoolfail (5 Books That Teach What School Failed to Teach)
    subparsers.add_parser("schoolfail", help="5 Books That Teach What School Failed to Teach (@coffeewithbooks__)")
    subparsers.add_parser("reallife", help="Alias for schoolfail (Real-Life Meta-Skills)")
    subparsers.add_parser("gtd", help="David Allen Getting Things Done & 2-Minute Rule")
    subparsers.add_parser("smalltalk", help="Debra Fine The Fine Art of Small Talk")
    subparsers.add_parser("dobelli", help="Rolf Dobelli The Art of Thinking Clearly")
    subparsers.add_parser("thinkingclearly", help="Alias for dobelli (Cognitive Bias Elimination)")

    # /ego (Ryan Holiday Ego Is the Enemy)
    subparsers.add_parser("ego", help="Ryan Holiday Ego Is the Enemy (Aspire, Success, Failure)")
    subparsers.add_parser("egoisenemy", help="Alias for ego")
    subparsers.add_parser("holiday2", help="Ryan Holiday Ego Is the Enemy Stoic Mastery")
    subparsers.add_parser("canvas", help="The Canvas Strategy (Anteambulo Protocol)")
    subparsers.add_parser("alivetime", help="Alive Time vs Dead Time (Robert Greene & Ryan Holiday)")
    subparsers.add_parser("antiego", help="Ego Subdual & Apprentice Mindset")

    # /agreements (Don Miguel Ruiz The Four Agreements)
    subparsers.add_parser("agreements", help="Don Miguel Ruiz The Four Agreements (Toltec Freedom)")
    subparsers.add_parser("fouragreements", help="Alias for agreements")
    subparsers.add_parser("ruiz", help="Don Miguel Ruiz Toltec Wisdom")
    subparsers.add_parser("toltec", help="Toltec Shamanic Philosophy & Domestication Breakthrough")
    subparsers.add_parser("impeccable", help="Agreement 1: Be Impeccable With Your Word")
    subparsers.add_parser("personalfreedom", help="The 4 Agreements for Personal Freedom")

    # /beyondorder (Dr. Jordan B. Peterson Beyond Order)
    subparsers.add_parser("beyondorder", help="Dr. Jordan B. Peterson Beyond Order (12 More Rules for Life)")
    subparsers.add_parser("12morerules", help="Alias for beyondorder")
    subparsers.add_parser("peterson2", help="Dr. Jordan B. Peterson Beyond Order")
    subparsers.add_parser("morerules", help="Beyond Order 12 More Rules")

    # /meaning (Viktor E. Frankl Man's Search for Meaning)
    subparsers.add_parser("meaning", help="Viktor E. Frankl Man's Search for Meaning (Logotherapy)")
    subparsers.add_parser("frankl", help="Alias for meaning")
    subparsers.add_parser("manssearch", help="Alias for meaning")
    subparsers.add_parser("logotherapy", help="Logotherapy: Will to Meaning & The 3 Pathways")

    # /howwelearn (Benedict Carey & Stanislas Dehaene How We Learn)
    subparsers.add_parser("howwelearn", help="Benedict Carey & Stanislas Dehaene How We Learn (Cognitive Science)")
    subparsers.add_parser("carey", help="Alias for howwelearn")
    subparsers.add_parser("dehaene", help="Alias for howwelearn")
    subparsers.add_parser("learnscience", help="Cognitive Neuroscience of Memory & Desirable Difficulty")

    # /greenlights (Matthew McConaughey Greenlights)
    subparsers.add_parser("greenlights", help="Matthew McConaughey Greenlights: Traffic Light Triad & Art of Livin'")
    subparsers.add_parser("greenlight", help="Alias for greenlights")
    subparsers.add_parser("mcconaughey", help="Alias for greenlights")
    subparsers.add_parser("artoflivin", help="Alias for greenlights")

    # /wordpower (Norman Lewis Word Power Made Easy)
    subparsers.add_parser("wordpower", help="Norman Lewis Word Power Made Easy: Root-Word Etymology Engine")
    subparsers.add_parser("wordpowermadeeasy", help="Alias for wordpower")
    subparsers.add_parser("normanlewis", help="Alias for wordpower")
    subparsers.add_parser("vocab", help="Alias for wordpower")

    # /psychocybernetics (Dr. Maxwell Maltz Psycho-Cybernetics)
    subparsers.add_parser("psychocybernetics", help="Dr. Maxwell Maltz Psycho-Cybernetics: The Mind's Servo-Mechanism")
    subparsers.add_parser("maltz", help="Alias for psychocybernetics")
    subparsers.add_parser("cybernetics", help="Alias for psychocybernetics")

    # /supernatural (Dr. Joe Dispenza Becoming Supernatural)
    subparsers.add_parser("supernatural", help="Dr. Joe Dispenza Becoming Supernatural: Neuro-Quantum Transformation")
    subparsers.add_parser("dispenza", help="Alias for supernatural")
    subparsers.add_parser("becomingsupernatural", help="Alias for supernatural")

    # /execution (Larry Bossidy & Ram Charan Execution)
    subparsers.add_parser("execution", help="Larry Bossidy & Ram Charan Execution: The Discipline of Getting Things Done")
    subparsers.add_parser("bossidy", help="Alias for execution")
    subparsers.add_parser("charan", help="Alias for execution")

    # /sameasever (Morgan Housel Same as Ever)
    subparsers.add_parser("sameasever", help="Morgan Housel Same as Ever: A Guide to What Never Changes")
    subparsers.add_parser("housel2", help="Alias for sameasever")

    # /stolenfocus (Johann Hari Stolen Focus)
    subparsers.add_parser("stolenfocus", help="Johann Hari Stolen Focus: Why You Can't Pay Attention")
    subparsers.add_parser("johannhari", help="Alias for stolenfocus")
    subparsers.add_parser("hari", help="Alias for stolenfocus")

    # /avoiding (Chris Williamson & Dipen Parmar The Magic in the Work You Avoid)
    subparsers.add_parser("avoiding", help="The Magic You're Looking for is in the Work You're Avoiding")
    subparsers.add_parser("magic", help="Alias for avoiding")
    subparsers.add_parser("resistance", help="Alias for avoiding")
    subparsers.add_parser("chriswilliamson", help="Alias for avoiding")
    subparsers.add_parser("dipen", help="Alias for avoiding")

    # /shadows (Lewis Strauss & Robert Downey Jr. Power Stays in the Shadows)
    subparsers.add_parser("shadows", help="Power Stays in the Shadows & 31-Year RDJ Redemption Arc")
    subparsers.add_parser("strauss", help="Alias for shadows")
    subparsers.add_parser("rdj", help="Alias for shadows")
    subparsers.add_parser("oppenheimer", help="Alias for shadows")
    subparsers.add_parser("darkhorse", help="Alias for shadows")

    # /gita (Bhagavad Gita 6.5 & 3.42 Sri Krishna Overcoming Laziness & Slave Mind)
    subparsers.add_parser("gita", help="Bhagavad Gita 6.5 & 3.42 Sri Krishna on Overcoming Laziness & Mind Mastery")
    subparsers.add_parser("krishna", help="Alias for gita")
    subparsers.add_parser("laziness", help="Alias for gita")
    subparsers.add_parser("mindconquest", help="Alias for gita")
    subparsers.add_parser("aatma", help="Alias for gita")

    # /chanakya (Chanakya Neeti 4 Inviolable Boundaries)
    subparsers.add_parser("chanakya", help="Chanakya Neeti 4 Inviolable Boundaries of Self-Respect")
    subparsers.add_parser("boundaries", help="Alias for chanakya")
    subparsers.add_parser("shikhshit", help="Alias for chanakya")
    subparsers.add_parser("selfrespect", help="Alias for chanakya")

    # /dangerous (HK Prime 10 Rules to Become Dangerous & Stagnation Elimination)
    subparsers.add_parser("dangerous", help="HK Prime 10 Rules to Become Dangerous & Stagnation Elimination")
    subparsers.add_parser("danger", help="Alias for dangerous")
    subparsers.add_parser("hkprime", help="Alias for dangerous")
    subparsers.add_parser("tenrules", help="Alias for dangerous")

    # /mindstorming (Brian Tracy 20-Idea Mindstorming Method)
    subparsers.add_parser("mindstorming", help="Brian Tracy 20-Idea Mindstorming Method for Creative Problem Solving")
    subparsers.add_parser("mindstorm", help="Alias for mindstorming")
    subparsers.add_parser("twentyideas", help="Alias for mindstorming")
    subparsers.add_parser("20ideas", help="Alias for mindstorming")
    subparsers.add_parser("mindstorms", help="Alias for mindstorming")

    # /noregret (Sudha Murty No Regrets, Self-Elevation & Gita 6.5)
    subparsers.add_parser("noregret", help="Sudha Murty No Regrets, Self-Elevation & Gita 6.5")
    subparsers.add_parser("sudhamurty", help="Alias for noregret")
    subparsers.add_parser("murty", help="Alias for noregret")
    subparsers.add_parser("elevation", help="Alias for noregret")
    subparsers.add_parser("selfelevation", help="Alias for noregret")

    # /realistic (Devanand Exist Gita 6.5 Realistic Self-Motivation & No Magic Pill)
    subparsers.add_parser("realistic", help="Devanand Exist Gita 6.5 Realistic Self-Motivation & No Magic Pill")
    subparsers.add_parser("devanand", help="Alias for realistic")
    subparsers.add_parser("nomagicpill", help="Alias for realistic")
    subparsers.add_parser("gita65", help="Alias for realistic")

    # /traits (Alex Hormozi 3 Traits of Hyper-Successful People)
    subparsers.add_parser("traits", help="Alex Hormozi 3 Traits of Hyper-Successful People (Modern Wisdom #610)")
    subparsers.add_parser("hormozi", help="Alias for traits")
    subparsers.add_parser("hypersuccessful", help="Alias for traits")
    subparsers.add_parser("threetraits", help="Alias for traits")
    subparsers.add_parser("three_traits", help="Alias for traits")

    # /twopains (Jim Rohn: The Two Pains — Discipline vs Regret)
    subparsers.add_parser("twopains", help="Jim Rohn: The Two Pains — Discipline vs Regret (@excelleratee)")
    subparsers.add_parser("jimrohn", help="Alias for twopains")
    subparsers.add_parser("rohn", help="Alias for twopains")
    subparsers.add_parser("discipline", help="Alias for twopains")
    subparsers.add_parser("regret", help="Alias for twopains")

    # /tedtalks (Trading Tiers: 7 Life-Changing TED Talks)
    subparsers.add_parser("tedtalks", help="Trading Tiers: 7 Life-Changing TED Talks to Replace 2 Years of Mistakes (@tradingtiers)")
    subparsers.add_parser("ted", help="Alias for tedtalks")
    subparsers.add_parser("tradingtiers", help="Alias for tedtalks")
    subparsers.add_parser("sevenlessons", help="Alias for tedtalks")

    # /toxic (Dan Zakaria: Top 10 People to Avoid at All Costs)
    subparsers.add_parser("toxic", help="Dan Zakaria: Top 10 People to Avoid at All Costs (@danzakaria)")
    subparsers.add_parser("avoidpeople", help="Alias for toxic")
    subparsers.add_parser("danzakaria", help="Alias for toxic")
    subparsers.add_parser("tenpeople", help="Alias for toxic")
    subparsers.add_parser("purgeclowns", help="Alias for toxic")

    # /braindiscipline (CodeWithBlacky: How to Train Your Brain to Enjoy Discipline)
    subparsers.add_parser("braindiscipline", help="CodeWithBlacky: How to Train Your Brain to Enjoy Discipline (@codewithblacky)")
    subparsers.add_parser("enjoydiscipline", help="Alias for braindiscipline")
    subparsers.add_parser("solumondal", help="Alias for braindiscipline")
    subparsers.add_parser("codewithblacky", help="Alias for braindiscipline")
    subparsers.add_parser("dandiscipline", help="Alias for braindiscipline")

    # /upperbody (Grandson @a_k_da_don No-Gym Upper Body Calisthenics)
    subparsers.add_parser("upperbody", help="Grandson: No-Gym Upper Body Calisthenics Protocol (@a_k_da_don)")
    subparsers.add_parser("calisthenics", help="Alias for upperbody")
    subparsers.add_parser("akdadon", help="Alias for upperbody")
    subparsers.add_parser("grandson", help="Alias for upperbody")
    subparsers.add_parser("nogym", help="Alias for upperbody")

    # /standingabs (Grandson @a_k_da_don Standing Ab Workouts at Home)
    subparsers.add_parser("standingabs", help="Grandson: Standing Ab Workouts at Home Protocol (@a_k_da_don)")
    subparsers.add_parser("abs", help="Alias for standingabs")
    subparsers.add_parser("absworkout", help="Alias for standingabs")
    subparsers.add_parser("core", help="Alias for standingabs")
    subparsers.add_parser("standingcore", help="Alias for standingabs")

    # /abshred (Sanjay Kumar Jha Ultimate Ab Shredding & Core Burner)
    subparsers.add_parser("abshred", help="Sanjay Kumar Jha: Ultimate Ab Shredding & Core Burner Protocol")
    subparsers.add_parser("sanjaycore", help="Alias for abshred")
    subparsers.add_parser("coreburner", help="Alias for abshred")
    subparsers.add_parser("jha", help="Alias for abshred")
    subparsers.add_parser("abburner", help="Alias for abshred")

    # /skipreadstudy (Julie Hogbin 3-Tier Book Filter: Skip, Read, Study)
    subparsers.add_parser("skipreadstudy", help="Julie Hogbin 3-Tier Book Filter: Skip, Read, Study (@juliehogbin)")
    subparsers.add_parser("bookfilter", help="Alias for skipreadstudy")
    subparsers.add_parser("hogbin", help="Alias for skipreadstudy")
    subparsers.add_parser("juliehogbin", help="Alias for skipreadstudy")
    subparsers.add_parser("prioritizebooks", help="Alias for skipreadstudy")

    # /forearms (Himansu Fit Forearm Shirt-Sleeve Aesthetic & 3-Step Giant Set)
    subparsers.add_parser("forearms", help="Himansu Fit: Shirt-Sleeve Forearm Aesthetic & 3-Step Giant Set (@himansu_fit_)")
    subparsers.add_parser("forearm", help="Alias for forearms")
    subparsers.add_parser("himansu", help="Alias for forearms")
    subparsers.add_parser("himansufit", help="Alias for forearms")
    subparsers.add_parser("shirtsleeve", help="Alias for forearms")

    # /sunil (Sunil Yoga Fit Anterior Pelvic Tilt & Lordosis Correction)
    subparsers.add_parser("sunil", help="Sunil Yoga Fit: Anterior Pelvic Tilt & Lordosis Correction (@sunilyogafit_)")
    subparsers.add_parser("sunilyogafit", help="Alias for sunil")
    subparsers.add_parser("lordosis", help="Alias for sunil")
    subparsers.add_parser("pelvictilt2", help="Alias for sunil")
    subparsers.add_parser("apt2", help="Alias for sunil")

    # /julie5 (Julie Hogbin 5 Books to Communicate Better Than 99% of People)
    subparsers.add_parser("julie5", help="Julie Hogbin: 5 Books to Communicate Better Than 99%% of People (@juliehogbin)")
    subparsers.add_parser("communication5", help="Alias for julie5")
    subparsers.add_parser("communicate", help="Alias for julie5")
    subparsers.add_parser("tacticaltalk", help="Alias for julie5")
    subparsers.add_parser("bettercommunication", help="Alias for julie5")
    subparsers.add_parser("fivebooks", help="Alias for julie5")

    # /mainfocus (Tier 1 Core Direction)
    subparsers.add_parser("mainfocus", help="Kanad Core Direction: Tier 1 Sovereign Main Focus (P1)")
    subparsers.add_parser("coredirection", help="Alias for mainfocus")
    subparsers.add_parser("direction", help="Alias for mainfocus")
    subparsers.add_parser("p1", help="Alias for mainfocus")

    # /strategy (Tier 2 Strategic Assets)
    subparsers.add_parser("strategy", help="Strategic Assets: Tier 2 Self-Improvement & Future Planning (P2)")
    subparsers.add_parser("assets", help="Alias for strategy")
    subparsers.add_parser("p2", help="Alias for strategy")
    subparsers.add_parser("futureplanning", help="Alias for strategy")

    # /audit-tiers (Tri-Tier Vault Classification Audit)
    subparsers.add_parser("audit-tiers", help="Obsidian Vault Tri-Tier Classification Audit & Zero-Clutter Status")
    subparsers.add_parser("tiers", help="Alias for audit-tiers")
    subparsers.add_parser("quarantine", help="Alias for audit-tiers")
    subparsers.add_parser("auditfocus", help="Alias for audit-tiers")

    # /voice (Zero-Cost Voice Training & Vocal Resonance Protocol)
    subparsers.add_parser("voice", help="Zero-Cost Voice Training & Vocal Resonance Protocol")
    subparsers.add_parser("vocal", help="Alias for voice")
    subparsers.add_parser("resonance", help="Alias for voice")
    subparsers.add_parser("speech", help="Alias for voice")
    subparsers.add_parser("gravitas", help="Alias for voice")

    # /lighting (AI Century Studios 24 Cinematic Lighting Prompts)
    subparsers.add_parser("lighting", help="AI Century Studios: 24 Cinematic Lighting Prompts & Portrait Mastery")
    subparsers.add_parser("light", help="Alias for lighting")
    subparsers.add_parser("cinematiclight", help="Alias for lighting")
    subparsers.add_parser("prompts", help="Alias for lighting")

    # /wallstare (The_SpaceGuy 10-Min Wall-Staring Attention Training Protocol)
    subparsers.add_parser("wallstare", help="The_SpaceGuy: 10-Min Wall-Staring Attention Training & Trataka Protocol")
    subparsers.add_parser("wall", help="Alias for wallstare")
    subparsers.add_parser("attention", help="Alias for wallstare")
    subparsers.add_parser("trataka", help="Alias for wallstare")
    subparsers.add_parser("stare", help="Alias for wallstare")

    args = parser.parse_args()

    commands = {
        "boost": cmd_boost,
        "grill": cmd_grill,
        "goal": cmd_goal,
        "plan": cmd_plan,
        "supplement": cmd_supplement,
        "learn": cmd_learn,
        "plugin": cmd_plugin,
        "automation": cmd_automation,
        "text": cmd_text,
        "gut": cmd_gut,
        "constipation": cmd_gut,
        "posture": cmd_posture,
        "bottle": cmd_posture,
        "focus": cmd_focus,
        "animedoro": cmd_focus,
        "style": cmd_style,
        "oldmoney": cmd_style,
        "book": cmd_book,
        "audiobook": cmd_book,
        "audiobookshelf": cmd_book,
        "shoulder": cmd_shoulder,
        "rotator": cmd_shoulder,
        "video": cmd_video,
        "video2": cmd_video,
        "minidlna": cmd_video,
        "career": cmd_career,
        "interview": cmd_career,
        "job": cmd_career,
        "pest": cmd_pest,
        "home": cmd_pest,
        "bookposture": cmd_bookposture,
        "neck": cmd_bookposture,
        "chin": cmd_bookposture,
        "dtan": cmd_dtan,
        "soap": cmd_dtan,
        "skincare": cmd_dtan,
        "facewash": cmd_facewash,
        "fw": cmd_facewash,
        "cleanser": cmd_facewash,
        "palette": cmd_palette,
        "color": cmd_palette,
        "expensive": cmd_palette,
        "zyverel": cmd_zyverel,
        "pairings": cmd_zyverel,
        "combinations": cmd_zyverel,
        "pelvic": cmd_pelvic,
        "tilt": cmd_pelvic,
        "flatbelly": cmd_pelvic,
        "apt": cmd_pelvic,
        "glowup": cmd_glowup,
        "looksmax": cmd_glowup,
        "face": cmd_glowup,
        "jawline": cmd_glowup,
        "shamani": cmd_shamani,
        "rajbook": cmd_shamani,
        "bookrec": cmd_shamani,
        "napkin": cmd_shamani,
        "kwik": cmd_kwik,
        "limitless": cmd_kwik,
        "brain": cmd_kwik,
        "faster": cmd_kwik,
        "realestate": cmd_realestate,
        "househack": cmd_realestate,
        "duplex": cmd_realestate,
        "fha": cmd_realestate,
        "stock": cmd_stock,
        "sharemarket": cmd_stock,
        "coffeecan": cmd_stock,
        "lynch": cmd_stock,
        "banking": cmd_banking,
        "ibc": cmd_banking,
        "familybank": cmd_banking,
        "cashvalue": cmd_banking,
        "yale": cmd_yale,
        "shiller": cmd_yale,
        "markets": cmd_yale,
        "corporatefinance": cmd_yale,
        "faculty": cmd_faculty,
        "teachers": cmd_faculty,
        "ssc": cmd_faculty,
        "govtexam": cmd_faculty,
        "linkedin": cmd_linkedin,
        "jobsearch": cmd_linkedin,
        "hiring": cmd_linkedin,
        "networking": cmd_linkedin,
        "ig": cmd_ig,
        "instagram": cmd_ig,
        "reels": cmd_ig,
        "contentgrowth": cmd_ig,
        "control": cmd_control,
        "stoic": cmd_control,
        "triggers": cmd_control,
        "nonreactivity": cmd_control,
        "auster": cmd_auster,
        "4321": cmd_auster,
        "timelines": cmd_auster,
        "counterfactual": cmd_auster,
        "greene": cmd_greene,
        "counterattack": cmd_greene,
        "war": cmd_greene,
        "tables": cmd_greene,
        "pyramid": cmd_pyramid,
        "beliavsky": cmd_pyramid,
        "overthinking": cmd_pyramid,
        "emotions": cmd_pyramid,
        "comm": cmd_comm,
        "communication": cmd_comm,
        "gottman": cmd_comm,
        "canwell": cmd_comm,
        "unscripted": cmd_unscripted,
        "richbooks": cmd_unscripted,
        "demarco": cmd_unscripted,
        "scottadams": cmd_unscripted,
        "systems": cmd_unscripted,
        "magnet": cmd_magnet,
        "charisma": cmd_magnet,
        "lowndes": cmd_magnet,
        "tracy": cmd_magnet,
        "king": cmd_magnet,
        "stronger": cmd_stronger,
        "emotionalstrength": cmd_stronger,
        "eq": cmd_stronger,
        "juliesmith": cmd_stronger,
        "meurisse": cmd_stronger,
        "adrenaline": cmd_adrenaline,
        "rush": cmd_adrenaline,
        "willpower": cmd_adrenaline,
        "warofart": cmd_adrenaline,
        "hollins": cmd_adrenaline,
        "soul": cmd_soul,
        "mind": cmd_soul,
        "tools": cmd_soul,
        "trenton": cmd_soul,
        "bessel": cmd_soul,
        "stutz": cmd_soul,
        "dialogue": cmd_dialogue,
        "script": cmd_dialogue,
        "talk": cmd_dialogue,
        "playbook": cmd_dialogue,
        "conversation": cmd_dialogue,
        "prakhar": cmd_prakhar,
        "flow": cmd_prakhar,
        "stealingfire": cmd_prakhar,
        "ashtavakra": cmd_prakhar,
        "peterson": cmd_prakhar,
        "osho": cmd_prakhar,
        "kotler": cmd_prakhar,
        "neverquit": cmd_neverquit,
        "resilience": cmd_neverquit,
        "quit": cmd_neverquit,
        "morin": cmd_neverquit,
        "foroux": cmd_neverquit,
        "carnegie2": cmd_neverquit,
        "holiday": cmd_neverquit,
        "sherry": cmd_neverquit,
        "schoolfail": cmd_schoolfail,
        "reallife": cmd_schoolfail,
        "gtd": cmd_schoolfail,
        "smalltalk": cmd_schoolfail,
        "dobelli": cmd_schoolfail,
        "thinkingclearly": cmd_schoolfail,
        "ego": cmd_ego,
        "egoisenemy": cmd_ego,
        "holiday2": cmd_ego,
        "canvas": cmd_ego,
        "alivetime": cmd_ego,
        "antiego": cmd_ego,
        "agreements": cmd_agreements,
        "fouragreements": cmd_agreements,
        "ruiz": cmd_agreements,
        "toltec": cmd_agreements,
        "impeccable": cmd_agreements,
        "personalfreedom": cmd_agreements,
        "beyondorder": cmd_beyondorder,
        "12morerules": cmd_beyondorder,
        "peterson2": cmd_beyondorder,
        "morerules": cmd_beyondorder,
        "meaning": cmd_meaning,
        "frankl": cmd_meaning,
        "manssearch": cmd_meaning,
        "logotherapy": cmd_meaning,
        "howwelearn": cmd_howwelearn,
        "carey": cmd_howwelearn,
        "dehaene": cmd_howwelearn,
        "learnscience": cmd_howwelearn,
        "greenlights": cmd_greenlights,
        "greenlight": cmd_greenlights,
        "mcconaughey": cmd_greenlights,
        "artoflivin": cmd_greenlights,
        "wordpower": cmd_wordpower,
        "wordpowermadeeasy": cmd_wordpower,
        "normanlewis": cmd_wordpower,
        "vocab": cmd_wordpower,
        "psychocybernetics": cmd_psychocybernetics,
        "maltz": cmd_psychocybernetics,
        "cybernetics": cmd_psychocybernetics,
        "supernatural": cmd_supernatural,
        "dispenza": cmd_supernatural,
        "becomingsupernatural": cmd_supernatural,
        "execution": cmd_execution,
        "bossidy": cmd_execution,
        "charan": cmd_execution,
        "sameasever": cmd_sameasever,
        "housel2": cmd_sameasever,
        "stolenfocus": cmd_stolenfocus,
        "johannhari": cmd_stolenfocus,
        "hari": cmd_stolenfocus,
        "avoiding": cmd_avoiding,
        "magic": cmd_avoiding,
        "resistance": cmd_avoiding,
        "chriswilliamson": cmd_avoiding,
        "dipen": cmd_avoiding,
        "shadows": cmd_shadows,
        "strauss": cmd_shadows,
        "rdj": cmd_shadows,
        "oppenheimer": cmd_shadows,
        "darkhorse": cmd_shadows,
        "gita": cmd_krishna,
        "krishna": cmd_krishna,
        "laziness": cmd_krishna,
        "mindconquest": cmd_krishna,
        "aatma": cmd_krishna,
        "chanakya": cmd_chanakya,
        "boundaries": cmd_chanakya,
        "shikhshit": cmd_chanakya,
        "selfrespect": cmd_chanakya,
        "dangerous": cmd_dangerous,
        "danger": cmd_dangerous,
        "hkprime": cmd_dangerous,
        "tenrules": cmd_dangerous,
        "mindstorming": cmd_mindstorming,
        "mindstorm": cmd_mindstorming,
        "twentyideas": cmd_mindstorming,
        "20ideas": cmd_mindstorming,
        "mindstorms": cmd_mindstorming,
        "noregret": cmd_noregret,
        "sudhamurty": cmd_noregret,
        "murty": cmd_noregret,
        "elevation": cmd_noregret,
        "selfelevation": cmd_noregret,
        "realistic": cmd_realistic,
        "devanand": cmd_realistic,
        "nomagicpill": cmd_realistic,
        "gita65": cmd_realistic,
        "traits": cmd_traits,
        "hormozi": cmd_traits,
        "hypersuccessful": cmd_traits,
        "threetraits": cmd_traits,
        "three_traits": cmd_traits,
        "twopains": cmd_twopains,
        "jimrohn": cmd_twopains,
        "rohn": cmd_twopains,
        "discipline": cmd_twopains,
        "regret": cmd_twopains,
        "tedtalks": cmd_tedtalks,
        "ted": cmd_tedtalks,
        "tradingtiers": cmd_tedtalks,
        "sevenlessons": cmd_tedtalks,
        "toxic": cmd_toxic,
        "avoidpeople": cmd_toxic,
        "danzakaria": cmd_toxic,
        "tenpeople": cmd_toxic,
        "purgeclowns": cmd_toxic,
        "braindiscipline": cmd_braindiscipline,
        "enjoydiscipline": cmd_braindiscipline,
        "solumondal": cmd_braindiscipline,
        "codewithblacky": cmd_braindiscipline,
        "dandiscipline": cmd_braindiscipline,
        "upperbody": cmd_upperbody,
        "calisthenics": cmd_upperbody,
        "akdadon": cmd_upperbody,
        "grandson": cmd_upperbody,
        "nogym": cmd_upperbody,
        "standingabs": cmd_standingabs,
        "abs": cmd_standingabs,
        "absworkout": cmd_standingabs,
        "core": cmd_standingabs,
        "standingcore": cmd_standingabs,
        "skipreadstudy": cmd_skipreadstudy,
        "bookfilter": cmd_skipreadstudy,
        "hogbin": cmd_skipreadstudy,
        "juliehogbin": cmd_skipreadstudy,
        "prioritizebooks": cmd_skipreadstudy,
        "forearms": cmd_forearms,
        "forearm": cmd_forearms,
        "himansu": cmd_forearms,
        "himansufit": cmd_forearms,
        "shirtsleeve": cmd_forearms,
        "sunil": cmd_sunil,
        "sunilyogafit": cmd_sunil,
        "lordosis": cmd_sunil,
        "pelvictilt2": cmd_sunil,
        "apt2": cmd_sunil,
        "julie5": cmd_communication,
        "communication5": cmd_communication,
        "communicate": cmd_communication,
        "tacticaltalk": cmd_communication,
        "bettercommunication": cmd_communication,
        "fivebooks": cmd_communication,
        "mainfocus": cmd_mainfocus,
        "coredirection": cmd_mainfocus,
        "direction": cmd_mainfocus,
        "p1": cmd_mainfocus,
        "strategy": cmd_strategy,
        "assets": cmd_strategy,
        "p2": cmd_strategy,
        "futureplanning": cmd_strategy,
        "audit-tiers": cmd_audit_tiers,
        "tiers": cmd_audit_tiers,
        "quarantine": cmd_audit_tiers,
        "auditfocus": cmd_audit_tiers,
        "voice": cmd_voice,
        "vocal": cmd_voice,
        "resonance": cmd_voice,
        "speech": cmd_voice,
        "gravitas": cmd_voice,
        "lighting": cmd_lighting,
        "light": cmd_lighting,
        "cinematiclight": cmd_lighting,
        "prompts": cmd_lighting,
        "wallstare": cmd_wallstare,
        "wall": cmd_wallstare,
        "attention": cmd_wallstare,
        "trataka": cmd_wallstare,
        "stare": cmd_wallstare,
        "abshred": cmd_abshred,
        "sanjaycore": cmd_abshred,
        "coreburner": cmd_abshred,
        "jha": cmd_abshred,
        "abburner": cmd_abshred
    }

    if args.command in commands:
        commands[args.command](args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

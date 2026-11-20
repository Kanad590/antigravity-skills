#!/usr/bin/env python3
"""
Clock-Free Sequential Daily Routine Planner
Dynamic daily routine scheduler supporting Liluah and Arambagh locations,
integrating Jan Aushadhi supplements, 45-min bidi delays, wake-time anchoring, and study phases.
"""
import sys
import argparse
from datetime import datetime, timedelta

def format_offset(wake_dt, minutes_offset):
    target = wake_dt + timedelta(minutes=minutes_offset)
    return target.strftime("%I:%M %p").lstrip("0")

def get_routine(location="arambagh", wake_time="08:00"):
    is_liluah = location.lower() == "liluah"
    loc_title = "🏢 LILUAH OUTPOST (Survival Calisthenics & Deep Work)" if is_liluah else "🏠 ARAMBAGH HEADQUARTERS (Home Gym 30kg & Structured Study)"
    
    # Parse wake anchor
    try:
        parts = wake_time.strip().split(":")
        h = int(parts[0])
        m = int(parts[1]) if len(parts) > 1 else 0
        wake_dt = datetime(2026, 1, 1, h, m)
        wake_str = wake_dt.strftime("%I:%M %p").lstrip("0")
        t0 = wake_str
        t1 = format_offset(wake_dt, 90)   # T+1:30
        t2 = format_offset(wake_dt, 330)  # T+5:30
        t3 = format_offset(wake_dt, 480)  # T+8:00
        t4 = format_offset(wake_dt, 660)  # T+11:00
        t5 = format_offset(wake_dt, 840)  # T+14:00
        t6 = format_offset(wake_dt, 960)  # T+16:00
        timing_badge = f"⚓ WAKE ANCHOR: {wake_str} (Natural Flow Active)"
    except Exception:
        timing_badge = f"⚓ WAKE ANCHOR: {wake_time}"
        t0, t1, t2, t3, t4, t5, t6 = "T+0:00", "T+1:30", "T+5:30", "T+8:00", "T+11:00", "T+14:00", "T+16:00"

    workout_desc = (
        "• Floor Push-ups (4 sets)\n"
        "• Door Pulls / Inverted Rows (4 sets)\n"
        "• Bodyweight Squats & Walking Lunges (3 sets)\n"
        "• Heavy Water Jug Bicep Curls & Lateral Raises"
    ) if is_liluah else (
        "• Push Day / Pull Day (⚠️ Neutral Spine posture)\n"
        "• 30kg Dumbbell Bench & Shoulder Presses\n"
        "• Barbell/Dumbbell Deadlifts & Bulgarian Split Squats\n"
        "• Core Planks & Sub-occipital neck stretches"
    )

    flow = f"""
================================================================================
⏱️ DYNAMIC CLOCK-FREE SEQUENTIAL ROUTINE: {loc_title}
{timing_badge}
================================================================================

🌅 PHASE 1: MORNING KICKSTART & CELLULAR IGNITION (~{t0} - {t1})
--------------------------------------------------------------------------------
1. 💧 Hydration & Gut: 1 full glass of water + 💊 PMBI Code 2149 (Pre/Pro-biotic).
2. ☀️ Sunlight & Somatics: 10-15 mins balcony/terrace sunlight (no sunglasses).
   • Gentle sub-occipital neck rolling and shoulder rolls.
   • 📵 First 90 minutes STRICTLY ZERO social media / messaging.
3. 🍚 Meal 1 (Heavy Breakfast/Brunch): Rice, Dal, Vegetables.
4. 💊 Morning Supplements (with food):
   • 🐟 Code 1959 (Omega-3 Softgel)
   • ⚡ Code 230 (B-Complex + Zn) — Alternate days
   • 🍊 Code 1849 (Vitamin-C 500mg Chewable)
   • 🧬 Code 673 (Biotin 10mg)
   • 🥑 Code 588 (Vitamin-E 400mg) — 3x per week
5. ⏳ 45-MIN BIDI LOCK: ⚠️ Zero smoking immediately after food! Allow gastric blood flow.

--------------------------------------------------------------------------------
🧠 PHASE 2: DEEP WORK & MIDDAY RECHARGE (~{t1} - {t3})
--------------------------------------------------------------------------------
6. 📚 Deep Study Slot 1: Quantitative Aptitude or GI (50m Focus + 10m Diffuse).
7. 🧘 Midday Reset: 15 mins NSDR (Yoga Nidra) or eyes-closed breathing (~{t2}).
   • Flushes cortical adenosine and restores striatal dopamine.
8. 🥔 Meal 2 (Mid-afternoon Carb Fuel): Boiled potatoes / Muri / Banana + Water.
   • ⚠️ DO NOT skip lunch! Prevents late-afternoon hypoglycemic bidi cravings.
9. 📖 Deep Study Slot 2: English RC / Error Spotting or Mock Test.

--------------------------------------------------------------------------------
🏋️ PHASE 3: PHYSICAL CONDITIONING (OpenGym) (~{t3} - {t4})
--------------------------------------------------------------------------------
10. ⚡ Workout Session:
{workout_desc}
11. 🚿 Refresh & Cool Down: Post-workout shower + neck/lat stretching.
12. 📝 Deep Study Slot 3: Formula revision, static GK notes, or error log review.

--------------------------------------------------------------------------------
🌙 PHASE 4: NIGHT RECOVERY & CELLULAR REPAIR (~{t4} - {t6})
--------------------------------------------------------------------------------
13. 🍲 Meal 3 (Dinner): Balanced dinner (~{t4}).
14. 🥤 Anabolic Night Recovery Stack:
    • 🥛 1 scoop Nutrija Whey Protein (25-27g pure protein)
    • ⚡ 3-5g Creatine Monohydrate (Cognitive & muscular recovery)
    • 💊 PMBI Code 817 (Calcium + Vit D3 + Mg + Zinc)
15. ⏳ 45-Min Bidi Lock: Gastric protection window.
16. 📞 Hands-free phone call / family wind-down (~{t5}).
17. 😴 8 Hours Deep Slow-Wave Sleep: Dark room, cool environment, brain detox (~{t6}).
================================================================================
"""
    return flow

def main():
    parser = argparse.ArgumentParser(description="Clock-Free Sequential Routine Planner")
    parser.add_argument("--location", choices=["arambagh", "liluah"], default="arambagh", help="Current residence context")
    parser.add_argument("--wake", default="08:00", help="Approximate wake-up time (e.g. 07:30, 08:00, 09:00)")
    args = parser.parse_args()

    print(get_routine(location=args.location, wake_time=args.wake))

if __name__ == "__main__":
    main()

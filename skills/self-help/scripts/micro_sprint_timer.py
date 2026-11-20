#!/usr/bin/env python3
"""
Micro-Sprint Focus Booster & Physiological Sigh Protocol
Overcomes friction and task initiation paralysis using Huberman's somatic reset
and Oakley's 5-minute micro-sprint technique.
"""
import sys
import time
import argparse

def display_sigh_instructions():
    print("""
======================================================================
🫁 HUBERMAN PHYSIOLOGICAL SIGH (Instant Autonomic Reset)
======================================================================
1. 👃 Inhale deeply through your nose (expand lungs ~80%).
2. 👃 Immediately take a second sharp inhale through nose (top it off!).
3. 👄 Release a long, slow sigh out through your mouth (4-6 seconds).
4. 🔄 Repeat this sequence 2-3 times now.
----------------------------------------------------------------------
💡 Neuroscience: This rapidly evacuates excess CO2, halts sympathetic
   panic, and restores prefrontal cortex control over procrastination.
======================================================================
""")

def run_micro_sprint(minutes=5, simulate=False):
    display_sigh_instructions()
    print(f"🚀 LAUNCHING {minutes}-MINUTE GRADED MICRO-SPRINT")
    print("🎯 Task Rule: You do NOT have to finish the entire chapter.")
    print("   You only have to work on ONE single problem or paragraph for 5 minutes.")
    print("   Once 5 minutes pass, your brain's dopamine momentum takes over!")
    print("----------------------------------------------------------------------")
    
    if simulate:
        print(f"⏱️ [SIMULATED] Timer started for {minutes} minute(s)... Flow activated!")
        return

    seconds = minutes * 60
    try:
        for remaining in range(seconds, 0, -1):
            mins, secs = divmod(remaining, 60)
            timer_display = f"\r⏳ Focus Window: {mins:02d}:{secs:02d} remaining | 📵 Distractions Locked!"
            sys.stdout.write(timer_display)
            sys.stdout.flush()
            time.sleep(1)
        print("\n\n🎉 5-MINUTE MICRO-SPRINT COMPLETE!")
        print("🧠 Momentum Achieved! Your neural circuitry is now warmed up.")
        print("🔥 Keep going into a full 25-minute Pomodoro or take a 1-minute stretch!")
    except KeyboardInterrupt:
        print("\n\n⚠️ Sprint paused. Take a deep breath and jump right back in.")

def main():
    parser = argparse.ArgumentParser(description="Micro-Sprint Timer & Physiological Sigh Coach")
    parser.add_argument("--minutes", type=int, default=5, help="Sprint duration in minutes (default: 5)")
    parser.add_argument("--simulate", action="store_true", help="Simulate sprint without blocking sleep")
    args = parser.parse_args()

    run_micro_sprint(minutes=args.minutes, simulate=args.simulate)

if __name__ == "__main__":
    main()

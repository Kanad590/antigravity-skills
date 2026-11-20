#!/usr/bin/env python3
"""
Socratic Drill & Motive Accountability Interrogator
Conducts rigorous accountability grilling pulling directly from Kanad's core Motive
and challenges syllabus mastery across Quantitative Aptitude, Reasoning, English, and General Awareness.
"""
import sys
import random
import argparse

DRILL_QUESTIONS = [
    {
        "subject": "Quantitative Aptitude",
        "topic": "Time & Work (Alternate Days)",
        "question": "A can finish a work in 12 days, B in 15 days. If they work on alternate days starting with A, how many total days will the work take?",
        "answer": "13 1/4 days. (Work LCM = 60; A=5/day, B=4/day; 2-day cycle = 9 units; 6 cycles = 12 days = 54 units; Day 13 A does 5 units = 59; Day 14 B does 1/4 unit)."
    },
    {
        "subject": "Quantitative Aptitude",
        "topic": "Percentage & Successive Change",
        "question": "The price of petrol increases by 25%. By what percentage must a family reduce consumption to keep total expenditure unchanged?",
        "answer": "20%. (Formula: [r / (100 + r)] * 100 = 25/125 * 100 = 20%)."
    },
    {
        "subject": "Quantitative Aptitude",
        "topic": "Ratio & Mixture",
        "question": "A mixture contains milk and water in the ratio 7:3. If 5 liters of water is added to the mixture, the ratio becomes 7:5. What was the initial quantity of milk?",
        "answer": "17.5 liters. (Water increases by 2 units = 5 liters -> 1 unit = 2.5 liters. Milk = 7 units = 7 * 2.5 = 17.5 liters)."
    },
    {
        "subject": "Quantitative Aptitude",
        "topic": "Speed, Time & Distance (Trains)",
        "question": "A train running at 54 km/h crosses a platform of length 250 meters in 30 seconds. What is the length of the train?",
        "answer": "200 meters. (Speed = 54 * 5/18 = 15 m/s. Total distance in 30s = 15 * 30 = 450 m. Train length = 450 - 250 = 200 m)."
    },
    {
        "subject": "Logical Reasoning",
        "topic": "Syllogism (Only a Few)",
        "question": "Statements: Only a few Pens are Pencils. All Pencils are Erasers.\nConclusions: I. Some Pens are not Pencils. II. All Pens can never be Pencils. Are they valid?",
        "answer": "Both I and II are valid. 'Only a few A are B' strictly implies both 'Some A are B' AND 'Some A are not B'."
    },
    {
        "subject": "Logical Reasoning",
        "topic": "Coding-Decoding",
        "question": "In a certain code language, 'ROAD' is written as 'URDG'. How is 'SWAN' written in that code?",
        "answer": "'VZDQ'. (Each letter is shifted forward by +3: S+3=V, W+3=Z, A+3=D, N+3=Q)."
    },
    {
        "subject": "Logical Reasoning",
        "topic": "Blood Relations",
        "question": "Pointing to a man in a photograph, a woman says: 'His mother is the only daughter of my mother.' How is the woman related to the man?",
        "answer": "Mother. ('Only daughter of my mother' = the woman herself; therefore, she is his mother)."
    },
    {
        "subject": "English Language",
        "topic": "Grammar & Error Spotting",
        "question": "Identify the error: 'Neither the manager nor the employees was present at the annual general meeting.'",
        "answer": "Error in 'was'. When two subjects are connected by 'neither... nor', the verb agrees with the closer subject ('employees' is plural, so it must be 'were present')."
    },
    {
        "subject": "English Language",
        "topic": "Vocabulary & Usage",
        "question": "What is the meaning of 'Capricious' and what is its standard antonym?",
        "answer": "Meaning: Given to sudden and unaccountable changes of mood or behavior (fickle, unpredictable). Antonym: Steadfast, consistent, predictable."
    },
    {
        "subject": "General Awareness",
        "topic": "Banking / Monetary Policy",
        "question": "What happens to liquidity in the banking system when RBI increases the Cash Reserve Ratio (CRR)?",
        "answer": "Liquidity decreases. Commercial banks must lock up more cash with RBI, leaving less available credit for lending, cooling inflationary pressures."
    }
]

MOTIVE_REMINDERS = [
    "🔥 REMEMBER THE MOTIVE: What did they do to you? Look at that termination letter. Are you going to let their dismissal be the final chapter of your life?",
    "⚡ POWER & DIGNITY: Nobody is coming to hand you respect. Dignity isn't given; it is extracted through undeniable competence.",
    "🩸 YOUR REVENGE: The only true revenge is supreme, unquestionable success where those who doubted you can only watch from below.",
    "✉️ A LETTER TO YOURSELF (2023-05-23): 'Whatever you think is your boundary—it's not true. Just a little try, and you will fly. Will fly.'"
]

def conduct_grill(topic=None, auto_reveal=False):
    print("=" * 70)
    print("⚔️ ANTIGRAVITY SOCRATIC ACCOUNTABILITY GRILL")
    print("=" * 70)
    
    # Motive anchor
    motive = random.choice(MOTIVE_REMINDERS)
    print(f"\n{motive}\n")
    print("-" * 70)
    
    # Filter questions
    pool = DRILL_QUESTIONS
    if topic:
        pool = [q for q in DRILL_QUESTIONS if topic.lower() in q["subject"].lower() or topic.lower() in q["topic"].lower()]
        if not pool:
            pool = DRILL_QUESTIONS
            
    q = random.choice(pool)
    print(f"🎯 SUBJECT: {q['subject']} | TOPIC: {q['topic']}")
    print(f"❓ QUESTION:\n   {q['question']}\n")
    print("-" * 70)
    
    # For automated execution, flags, or non-interactive environments
    if auto_reveal or not sys.stdin.isatty():
        print(f"[AUTO-VERIFICATION / NON-INTERACTIVE MODE]")
        print(f"✅ SOLUTION:\n   {q['answer']}")
        print("=" * 70)
        return

    print("🛑 Stop! Do not scroll or guess. Close your eyes and solve it on paper.")
    print("💡 Type 'reveal' to verify your active recall, or 'exit':")
    try:
        user_input = input(">> ").strip().lower()
        if user_input in ["reveal", "ans", "answer", "y", "yes", ""]:
            print(f"\n✅ VERIFIED ANSWER:\n   {q['answer']}\n")
            print("Did you solve it cleanly without hesitation? If not, log it in your error journal immediately!")
        else:
            print("Session closed. Stay relentless.")
    except (EOFError, KeyboardInterrupt):
        print("\n\nSession terminated.")

def main():
    parser = argparse.ArgumentParser(description="Socratic Drill & Motive Accountability Interrogator")
    parser.add_argument("--topic", type=str, help="Filter drill by topic/subject (e.g. math, reasoning, english)")
    parser.add_argument("--auto", "--reveal", dest="auto", action="store_true", help="Auto-reveal answer without interactive prompt")
    args = parser.parse_args()

    conduct_grill(topic=args.topic, auto_reveal=args.auto)

if __name__ == "__main__":
    main()

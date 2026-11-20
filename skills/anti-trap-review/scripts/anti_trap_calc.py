#!/usr/bin/env python3
"""
Anti-Trap Review & Scoring Engine CLI
Calculates Net Score based on the 13-Factor Dual-Set model with Veto checking.
"""

import sys
import json
import argparse

FACTORS = [
    {
        "id": 1,
        "name": "সিলেবাস ও কনটেন্ট সম্পূর্ণতা",
        "key": "syllabus_completeness",
        "positive": 12,
        "norm_penalty": -5,
        "deceptive_penalty": -25,
        "veto_threshold": -25
    },
    {
        "id": 2,
        "name": "পড়াশোনার আসল গভীরতা (Exam Rigor)",
        "key": "exam_rigor",
        "positive": 12,
        "norm_penalty": -5,
        "deceptive_penalty": -22,
        "veto_threshold": None
    },
    {
        "id": 3,
        "name": "আর্থিক নিরাপত্তা (AutoPay স্বচ্ছতা)",
        "key": "financial_safety",
        "positive": 10,
        "norm_penalty": -5,
        "deceptive_penalty": -30,
        "veto_threshold": -30
    },
    {
        "id": 4,
        "name": "স্বাধীন ফোরাম জনমত (Quora/Reddit/MouthShut)",
        "key": "independent_forums",
        "positive": 10,
        "norm_penalty": -5,
        "deceptive_penalty": -20,
        "veto_threshold": None
    },
    {
        "id": 5,
        "name": "যাচাইকৃত ৫★ রিভিউ সততা",
        "key": "verified_5star",
        "positive": 10,
        "norm_penalty": -3,
        "deceptive_penalty": -15,
        "veto_threshold": None
    },
    {
        "id": 6,
        "name": "২-৩ স্টার গ্রাউন্ড রিয়ালিটি",
        "key": "ground_reality",
        "positive": 8,
        "norm_penalty": -3,
        "deceptive_penalty": -7,
        "veto_threshold": None
    },
    {
        "id": 7,
        "name": "সাম্প্রতিক ৩০-৯০ দিন ট্রেন্ড",
        "key": "recent_trend",
        "positive": 8,
        "norm_penalty": -3,
        "deceptive_penalty": -15,
        "veto_threshold": None
    },
    {
        "id": 8,
        "name": "ভাষাগত স্বচ্ছতা",
        "key": "language_clarity",
        "positive": 8,
        "norm_penalty": -3,
        "deceptive_penalty": -20,
        "veto_threshold": None
    },
    {
        "id": 9,
        "name": "বিজ্ঞাপনের সততা (Zero Deception)",
        "key": "ad_honesty",
        "positive": 6,
        "norm_penalty": -3,
        "deceptive_penalty": -15,
        "veto_threshold": None
    },
    {
        "id": 10,
        "name": "টেকনিক্যাল স্থায়িত্ব ও ডিভাইস এক্সেস",
        "key": "technical_stability",
        "positive": 3,
        "norm_penalty": -2,
        "deceptive_penalty": -10,
        "veto_threshold": None
    },
    {
        "id": 11,
        "name": "প্রাইভেসি ও স্প্যাম কল প্রতিরোধ",
        "key": "privacy_no_spam",
        "positive": 5,
        "norm_penalty": -3,
        "deceptive_penalty": -15,
        "veto_threshold": None
    },
    {
        "id": 12,
        "name": "ডেভেলপার সাপোর্ট ও কাস্টমার আচরণ",
        "key": "developer_support",
        "positive": 4,
        "norm_penalty": -2,
        "deceptive_penalty": -10,
        "veto_threshold": None
    },
    {
        "id": 13,
        "name": "ওয়েবসাইট রিভিউ ও টেস্টিমোনিয়াল সততা",
        "key": "website_reviews",
        "positive": 4,
        "norm_penalty": -2,
        "deceptive_penalty": -8,
        "veto_threshold": None
    }
]

def calculate_review(evaluations, product_name="Product"):
    """
    evaluations is a dict:
    {
       factor_id (1..13): {
           "status": "positive" | "norm" | "deceptive" | "neutral",
           "notes": "optional note"
       }
    }
    """
    total_positive = 0
    total_penalty = 0
    veto_triggered = []
    breakdown = []

    for f in FACTORS:
        fid = f["id"]
        ev = evaluations.get(fid, evaluations.get(str(fid), {"status": "neutral"}))
        status = ev.get("status", "neutral")
        notes = ev.get("notes", "")

        score = 0
        status_label = "Neutral (0)"
        if status == "positive":
            score = f["positive"]
            total_positive += score
            status_label = f"✅ Positive (+{score})"
        elif status == "norm":
            score = f["norm_penalty"]
            total_penalty += abs(score)
            status_label = f"🔵 Set-A Norm ({score})"
        elif status == "deceptive":
            score = f["deceptive_penalty"]
            total_penalty += abs(score)
            status_label = f"🔴 Set-B Deceptive ({score})"
            if f["veto_threshold"] and score <= f["veto_threshold"]:
                veto_triggered.append(f"{f['name']} ({score})")
        
        breakdown.append({
            "id": fid,
            "name": f["name"],
            "status": status_label,
            "score": score,
            "notes": notes
        })

    net_score = total_positive - total_penalty

    # Determine Verdict
    if veto_triggered:
        verdict = "🛑 HARD REJECT (VETO TRIGGERED)"
        verdict_color = "red"
        explanation = f"Veto Rule Triggered by fatal trap: {', '.join(veto_triggered)}"
    elif net_score >= 65:
        verdict = "🟢 FULL PASS (RECOMMENDED)"
        verdict_color = "green"
        explanation = "High quality, proven utility, and within acceptable industry norms."
    elif 35 <= net_score < 65:
        verdict = "🟡 CONDITIONAL USE (SANDBOX PROTOCOL REQUIRED)"
        verdict_color = "yellow"
        explanation = "Value exists but risk detected. Use secondary phone, virtual card with no auto-pay, and disposable email."
    else:
        verdict = "🛑 HARD REJECT (POOR SCORE)"
        verdict_color = "red"
        explanation = "Accumulated severe penalties and traps outweigh benefits. Blacklist/Uninstall recommended."

    return {
        "product_name": product_name,
        "total_positive": total_positive,
        "total_penalty": total_penalty,
        "net_score": net_score,
        "verdict": verdict,
        "verdict_color": verdict_color,
        "veto_triggered": veto_triggered,
        "explanation": explanation,
        "breakdown": breakdown
    }

def print_report(res):
    print("=" * 70)
    print(f"🛡️ ANTI-TRAP REVIEW REPORT: {res['product_name']}")
    print("=" * 70)
    print(f"Total Positive Points : +{res['total_positive']} / 100")
    print(f"Total Penalties       : -{res['total_penalty']}")
    print(f"NET SCORE             : {res['net_score']}")
    print(f"FINAL VERDICT         : {res['verdict']}")
    print(f"Explanation           : {res['explanation']}")
    print("-" * 70)
    print(f"{'#':<3} {'Factor':<42} {'Evaluation':<22} {'Score'}")
    print("-" * 70)
    for b in res["breakdown"]:
        print(f"{b['id']:<3} {b['name']:<42} {b['status']:<22} {b['score']:+d}")
    print("=" * 70)

def main():
    parser = argparse.ArgumentParser(description="Anti-Trap Forensic Review Calculator")
    parser.add_argument("--json", help="Path to input JSON evaluation file")
    parser.add_argument("--name", default="Sample App", help="Name of product being audited")
    parser.add_argument("--demo", action="store_true", help="Run a demo comparison")
    args = parser.parse_args()

    if args.demo:
        print("\n--- DEMO 1: SCAM APP (With AutoPay & Empty Syllabus) ---")
        scam_eval = {
            1: {"status": "deceptive"}, # Empty syllabus -25 (Veto)
            2: {"status": "deceptive"}, # Easy quiz -22
            3: {"status": "deceptive"}, # AutoPay trap -30 (Veto)
            4: {"status": "deceptive"}, # Quora/Reddit screams scam -20
            5: {"status": "deceptive"}, # Bot 5-star -15
            6: {"status": "deceptive"}, # -7
            7: {"status": "deceptive"}, # -15
            8: {"status": "deceptive"}, # -20
            9: {"status": "deceptive"}, # -15
            10: {"status": "deceptive"}, # -10
            11: {"status": "deceptive"}, # -15
            12: {"status": "deceptive"}, # -10
            13: {"status": "deceptive"}  # -8
        }
        res1 = calculate_review(scam_eval, "Shady Exam App")
        print_report(res1)

        print("\n--- DEMO 2: HONEST EDTECH (Industry Norms, Genuine Content) ---")
        honest_eval = {
            1: {"status": "positive"}, # +12
            2: {"status": "positive"}, # +12
            3: {"status": "norm"},     # -5 (Has AutoPay, but clear cancel)
            4: {"status": "positive"}, # +10
            5: {"status": "positive"}, # +10
            6: {"status": "positive"}, # +8
            7: {"status": "positive"}, # +8
            8: {"status": "positive"}, # +8
            9: {"status": "norm"},     # -3 (Slight 'India No.1' exaggeration)
            10: {"status": "positive"},# +3
            11: {"status": "norm"},    # -3 (1 follow-up call)
            12: {"status": "positive"},# +4
            13: {"status": "norm"}     # -2 (Selected testimonials)
        }
        res2 = calculate_review(honest_eval, "Verified Trusted App")
        print_report(res2)
        return

    if args.json:
        with open(args.json, "r", encoding="utf-8") as f:
            data = json.load(f)
        pname = data.get("product_name", args.name)
        evals = data.get("evaluations", {})
        res = calculate_review(evals, pname)
        print_report(res)
    else:
        print("Please provide --json <path> or use --demo to view example audits.")

if __name__ == "__main__":
    main()

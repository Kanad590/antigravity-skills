#!/usr/bin/env python3
"""
Anti-Trap Review & Scoring Engine CLI (v4.1 Calibrated & Robust Edition)
Calculates Net Score based on the 13-Factor Dual-Set model with Veto checking.
Strictly aligns mathematical implementation with references/scoring-model.md.
"""

import sys
import os
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
        "key": "linguistic_clarity",
        "positive": 8,
        "norm_penalty": -3,
        "deceptive_penalty": -20,
        "veto_threshold": None
    },
    {
        "id": 9,
        "name": "বিজ্ঞাপনের সততা",
        "key": "ad_honesty",
        "positive": 6,
        "norm_penalty": -3,
        "deceptive_penalty": -15,
        "veto_threshold": None
    },
    {
        "id": 10,
        "name": "টেকনিক্যাল স্থায়িত্ব ও ডিভাইস এক্সেস",
        "key": "tech_stability",
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
        "veto_threshold": -15
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
        "key": "website_testimonials",
        "positive": 4,
        "norm_penalty": -2,
        "deceptive_penalty": -8,
        "veto_threshold": None
    }
]

VALID_STATUSES = {"positive", "norm", "deceptive", "neutral", "uninspected"}

def calculate_review(evaluations, product_name="Target Offering"):
    """
    Evaluates offering against the 13-Factor Dual-Set model.
    Conforms strictly to references/scoring-model.md:
      - All Positive: +100
      - All Industry Norm: +56 (100 - 44)
      - All Deceptive: -112 (100 - 212)
    """
    total_penalty = 0
    veto_triggered = []
    breakdown = []
    inspected_count = 0

    for f in FACTORS:
        fid = f["id"]
        fkey = f["key"]
        
        # Look up by ID (int or str) or by factor key
        ev = evaluations.get(fid) or evaluations.get(str(fid)) or evaluations.get(fkey) or {}
        raw_status = str(ev.get("status", "neutral")).strip().lower()
        status = raw_status if raw_status in VALID_STATUSES else "neutral"
        notes = ev.get("notes", "")

        weight = f["positive"]
        score = weight
        penalty = 0
        status_label = "Neutral (0)"

        if status == "positive":
            inspected_count += 1
            status_label = f"✅ Positive (+{weight})"
            score = weight
        elif status == "norm":
            inspected_count += 1
            penalty = abs(f["norm_penalty"])
            score = weight - penalty
            total_penalty += penalty
            status_label = f"🔵 Set-A Norm (-{penalty})"
        elif status == "deceptive":
            inspected_count += 1
            penalty = abs(f["deceptive_penalty"])
            score = weight - penalty
            total_penalty += penalty
            status_label = f"🔴 Set-B Deceptive (-{penalty})"
            if f["veto_threshold"] is not None and (-penalty) <= f["veto_threshold"]:
                veto_triggered.append(f"{f['name']} (-{penalty})")
        else:
            status_label = "⚪ Uninspected (0)"

        breakdown.append({
            "id": fid,
            "key": fkey,
            "name": f["name"],
            "status": status_label,
            "score": score,
            "penalty": penalty,
            "notes": notes
        })

    # Mathematical Net Score (Aligned with scoring-model.md)
    net_score = 100 - total_penalty

    # Determine Verdict & Exit Code
    if inspected_count < 3:
        verdict = "⚪ INSUFFICIENT DATA (RESEARCH REQUIRED)"
        verdict_color = "gray"
        explanation = f"Only {inspected_count} of 13 factors inspected. Minimum 3 factors required to compute trustworthy verdict."
        exit_code = 2
    elif veto_triggered:
        verdict = "🛑 HARD REJECT (VETO TRIGGERED)"
        verdict_color = "red"
        explanation = f"Fatal trap detected: {', '.join(veto_triggered)}. Immediate kill rule enforced regardless of total score."
        exit_code = 1
    elif net_score >= 65:
        verdict = "🟢 FULL PASS (RECOMMENDED)"
        verdict_color = "green"
        explanation = "High quality, proven utility, and within acceptable industry norms."
        exit_code = 0
    elif 35 <= net_score < 65:
        verdict = "🟡 CONDITIONAL USE (SANDBOX PROTOCOL REQUIRED)"
        verdict_color = "yellow"
        explanation = "Moderate utility but clear risks detected. Sandbox protocol required: virtual card with no auto-pay, disposable email, secondary device."
        exit_code = 2
    else:
        verdict = "🛑 HARD REJECT (POOR SCORE)"
        verdict_color = "red"
        explanation = "Accumulated severe penalties and deceptive practices outweigh utility. Blacklist/Uninstall recommended."
        exit_code = 1

    return {
        "product_name": product_name,
        "inspected_count": inspected_count,
        "total_penalty": total_penalty,
        "net_score": net_score,
        "verdict": verdict,
        "verdict_color": verdict_color,
        "veto_triggered": veto_triggered,
        "explanation": explanation,
        "breakdown": breakdown,
        "exit_code": exit_code
    }

def print_report(res):
    print("=" * 76)
    print(f"🛡️  ANTI-TRAP REVIEW REPORT: {res['product_name']}")
    print("=" * 76)
    print(f"• Factors Inspected   : {res['inspected_count']} / 13")
    print(f"• Total Penalties     : -{res['total_penalty']}")
    print(f"• NET SCORE           : {res['net_score']} / 100")
    print(f"• FINAL VERDICT       : {res['verdict']}")
    print(f"• Explanation         : {res['explanation']}")
    print("-" * 76)
    print(f"{'#':<3} | {'Factor':<36} | {'Evaluation':<24} | {'Score'}")
    print("-" * 76)
    for b in res["breakdown"]:
        f_name = b["name"][:34]
        print(f"{b['id']:<3} | {f_name:<36} | {b['status']:<24} | {b['score']:>4}")
    print("=" * 76)

def main():
    parser = argparse.ArgumentParser(description="Anti-Trap Forensic Review & Scoring Engine CLI (v4.1)")
    parser.add_argument("--json", type=str, help="Path to input audit JSON file")
    parser.add_argument("--name", type=str, default="Target Offering", help="Name of product or offering")
    parser.add_argument("--demo", action="store_true", help="Run calibrated validation demos")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="Output format (default: text)")
    args = parser.parse_args()

    if args.demo:
        print("\n--- DEMO 1: SCAM EDTECH APP (Severe Traps & AutoPay Deception) ---")
        scam_eval = {
            1: {"status": "deceptive"}, # -25 (Veto)
            2: {"status": "deceptive"}, # -22
            3: {"status": "deceptive"}, # -30 (Veto)
            4: {"status": "deceptive"}, # -20
            5: {"status": "deceptive"}, # -15
            6: {"status": "deceptive"}, # -7
            7: {"status": "deceptive"}, # -15
            8: {"status": "deceptive"}, # -20
            9: {"status": "deceptive"}, # -15
            10: {"status": "deceptive"}, # -10
            11: {"status": "deceptive"}, # -15 (Veto)
            12: {"status": "deceptive"}, # -10
            13: {"status": "deceptive"}  # -8
        }
        res1 = calculate_review(scam_eval, "Predatory Test Prep App")
        print_report(res1)
        assert res1["net_score"] == -112, f"Expected -112, got {res1['net_score']}"
        assert len(res1["veto_triggered"]) >= 3, "Expected 3 fatal vetos"

        print("\n--- DEMO 2: HONEST EDTECH APP (Industry Norms + Proven Rigor) ---")
        honest_eval = {
            1: {"status": "positive"}, # +12
            2: {"status": "positive"}, # +12
            3: {"status": "norm"},     # -5 (Has AutoPay, but clear cancel)
            4: {"status": "positive"}, # +10
            5: {"status": "positive"}, # +10
            6: {"status": "positive"}, # +8
            7: {"status": "positive"}, # +8
            8: {"status": "positive"}, # +8
            9: {"status": "norm"},     # -3 (Slight exaggeration)
            10: {"status": "positive"},# +3
            11: {"status": "norm"},    # -3 (1 follow-up call)
            12: {"status": "positive"},# +4
            13: {"status": "norm"}     # -2 (Selected testimonials)
        }
        res2 = calculate_review(honest_eval, "Verified Trusted Prep")
        print_report(res2)
        assert res2["net_score"] == 87, f"Expected 87, got {res2['net_score']}"
        assert "FULL PASS" in res2["verdict"], "Expected Full Pass"

        print("\n--- DEMO 3: ALL INDUSTRY NORMS (Baseline Mass-Normal Test) ---")
        all_norm_eval = {i: {"status": "norm"} for i in range(1, 14)}
        res3 = calculate_review(all_norm_eval, "Average Industry Player")
        print_report(res3)
        assert res3["net_score"] == 56, f"Expected 56, got {res3['net_score']}"
        assert "CONDITIONAL USE" in res3["verdict"], "Expected Conditional Use for all-norm"

        print("\n--- DEMO 4: ZERO DATA (Insufficient Evidence Test) ---")
        res4 = calculate_review({}, "Unknown Brand")
        print_report(res4)
        assert "INSUFFICIENT DATA" in res4["verdict"], "Expected Insufficient Data"

        print("\n✅ ALL 4 CALIBRATION TESTS PASSED PERFECTLY!")
        sys.exit(0)

    if not args.json:
        print("Error: Missing required argument: --json <path> or --demo", file=sys.stderr)
        sys.exit(1)

    if not os.path.exists(args.json):
        print(f"Error: File not found: '{args.json}'", file=sys.stderr)
        sys.exit(1)

    try:
        with open(args.json, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON syntax in '{args.json}': {e}", file=sys.stderr)
        sys.exit(1)

    pname = data.get("product_name", args.name)
    evals = data.get("evaluations", {})
    res = calculate_review(evals, pname)

    if args.format == "json":
        print(json.dumps(res, indent=2, ensure_ascii=False))
    else:
        print_report(res)

    sys.exit(res["exit_code"])

if __name__ == "__main__":
    main()

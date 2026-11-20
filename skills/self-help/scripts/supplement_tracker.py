#!/usr/bin/env python3
"""
Jan Aushadhi (PMBJP) Supplement Tracker & Safety Auditor
Manages drug codes, scientific administration timing, alternate-day logic,
and provides strict safety interception against high-risk compounds (e.g. Code 1622).
"""
import sys
import argparse
from datetime import datetime

SUPPLEMENT_DB = {
    "2149": {
        "name": "Pre and Pro Biotic Capsules",
        "timing": "Morning Empty Stomach",
        "frequency": "Daily",
        "dose": "1 capsule with water",
        "price": "₹55.00 / 10's",
        "action": "Restores gut microbiome, improves digestion, prevents gas and nutrient malabsorption."
    },
    "1959": {
        "name": "Omega-3 Softgel Capsule (EPA 180 + DHA 120)",
        "timing": "With Meal 1 (Breakfast/Lunch)",
        "frequency": "Daily",
        "dose": "1 softgel",
        "price": "₹120.00 / 30's",
        "action": "Enhances neuronal membrane fluidity, combats Dry Eye, supports cognitive focus."
    },
    "230": {
        "name": "Vitamin B-Complex fort Zinc",
        "timing": "With Meal 1",
        "frequency": "Alternate Days (1 day on, 1 day off)",
        "dose": "1 capsule",
        "price": "₹9.90 / 10's",
        "action": "Cellular ATP energy synthesis. Alternate-day dosing prevents zinc accumulation."
    },
    "1849": {
        "name": "Vitamin-C Chewable Tablets 500mg",
        "timing": "With Meal 1",
        "frequency": "Daily",
        "dose": "1 chewable tablet",
        "price": "₹15.00 / 10's",
        "action": "Potent antioxidant; repairs oxidative damage caused by mental stress and pollution."
    },
    "588": {
        "name": "Vitamin E Softgel 400mg",
        "timing": "With Meal 1",
        "frequency": "3 Days a Week (Mon, Wed, Fri)",
        "dose": "1 softgel",
        "price": "₹22.00 / 10's",
        "action": "Lipid antioxidant, skin and eye protection. Fat-soluble, so cycled 3x/week."
    },
    "673": {
        "name": "Biotin Tablets 10mg",
        "timing": "With Meal 1",
        "frequency": "Daily",
        "dose": "1 tablet",
        "price": "₹34.00 / 10's",
        "action": "Supports hair follicle health and keratin synthesis."
    },
    "817": {
        "name": "Calcium Carbonate + Vit D3 + Mg + Zinc",
        "timing": "After Meal 3 (Dinner)",
        "frequency": "Daily",
        "dose": "1 tablet",
        "price": "₹14.30 / 10's",
        "action": "Bone density support; Magnesium soothes the central nervous system for deep sleep."
    }
}

STRICT_WARNINGS = {
    "1622": (
        "🚨 FATAL HEALTH HAZARD — DO NOT CONSUME!\n"
        "Drug Code 1622 contains Ferrous Ascorbate 100mg (~30mg Elemental Iron) + Folic Acid + Zinc.\n"
        "In non-anemic adult men, unexcretable elemental iron accumulates in the liver, pancreas, and heart,\n"
        "causing severe oxidative organ toxicity and hemochromatosis. NEVER TAKE CODE 1622!"
    )
}

def display_schedule():
    print("=" * 75)
    print("💊 JAN AUSHADHI (PMBJP) MASTER SUPPLEMENT PROTOCOL")
    print("=" * 75)
    
    sections = {
        "🌅 MORNING (EMPTY STOMACH)": ["2149"],
        "🍚 WITH MEAL 1 (MORNING/AFTERNOON)": ["1959", "230", "1849", "588", "673"],
        "🌙 AFTER MEAL 3 (NIGHT / DINNER)": ["817"]
    }
    
    for sec_title, codes in sections.items():
        print(f"\n{sec_title}:")
        print("-" * 75)
        for code in codes:
            item = SUPPLEMENT_DB[code]
            print(f"• [Code {code}] {item['name']}")
            print(f"  Dose: {item['dose']} | Frequency: {item['frequency']} | Price: {item['price']}")
            print(f"  Science: {item['action']}")
    print("\n" + "=" * 75)

def check_drug_code(code):
    clean_code = code.strip()
    if clean_code in STRICT_WARNINGS:
        print(f"\n❌ CRITICAL CONTRAINDICATION ALERT:\n{STRICT_WARNINGS[clean_code]}\n")
        return False
    elif clean_code in SUPPLEMENT_DB:
        item = SUPPLEMENT_DB[clean_code]
        print(f"\n✅ VERIFIED SAFE SUPPLEMENT [Code {clean_code}]:")
        print(f"   Name:      {item['name']}")
        print(f"   Timing:    {item['timing']}")
        print(f"   Dose:      {item['dose']} ({item['frequency']})")
        print(f"   Price:     {item['price']}")
        print(f"   Action:    {item['action']}\n")
        return True
    else:
        print(f"\n⚠️ Drug code '{clean_code}' is not in the curated Jan Aushadhi self-help stack.")
        return False

def main():
    parser = argparse.ArgumentParser(description="Jan Aushadhi Supplement Tracker & Safety Checker")
    parser.add_argument("--schedule", action="store_true", help="Print the full daily supplement schedule")
    parser.add_argument("--check", type=str, help="Check safety and dosing of a specific Jan Aushadhi drug code")
    args = parser.parse_args()

    if args.check:
        check_drug_code(args.check)
    else:
        display_schedule()

if __name__ == "__main__":
    main()

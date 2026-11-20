---
name: panchang-vedic
description: >-
  Use this skill whenever the user asks for daily Vedic Panchanga, Tithi, Nakshatra, Yoga, Karana,
  Rahu Kalam, Yamagandam, Gulika, Abhijit Muhurta, or major planetary transits (Gochar).
---

# Vedic Panchanga & Muhurta Skill

This skill calculates daily Panchanga elements and auspicious/inauspicious muhurtas using Swiss Ephemeris (`pyswisseph`) with standard Chitrapaksha / Lahiri Ayanamsha.

---

## 🚀 Quick Reference Commands

Helper CLI Script: `~/.gemini/config/plugins/panchang-vedic/skills/panchang-vedic/scripts/panchang_calc.py`

Task | Command
:--- | :---
**Today's Panchang & Muhurtas** | `~/.gemini/config/plugins/panchang-vedic/skills/panchang-vedic/scripts/panchang_calc.py`
**Panchang for Specific Date** | `~/.gemini/config/plugins/panchang-vedic/skills/panchang-vedic/scripts/panchang_calc.py --date "2026-11-15"`
**Machine JSON Output** | `~/.gemini/config/plugins/panchang-vedic/skills/panchang-vedic/scripts/panchang_calc.py --json`

---

## 💡 Capabilities

1. **5 Limbs of Panchanga:** Tithi, Vara, Nakshatra (with Pada), Yoga, and Karana.
2. **Key Muhurtas:** Rahu Kalam (Avoid for new beginnings), Yamagandam, Gulika, and Abhijit Muhurta (universal auspicious window).
3. **Gochar (Transit Summary):** Real-time sign locations for Jupiter, Saturn, Rahu, and Ketu.

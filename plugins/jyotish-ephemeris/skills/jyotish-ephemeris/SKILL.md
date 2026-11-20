---
name: jyotish-ephemeris
description: >-
  Use this skill whenever the user asks for Vedic astrology calculations, Nirayana / sidereal planetary positions,
  Lahiri Ayanamsha, Lagna (Ascendant), Nakshatra Pada, Navamsha (D-9), or planetary chart analysis matching Jagannatha Hora.
---

# Vedic Astrology (Jyotish) Ephemeris & Jagannatha Hora Automation Skill

This skill calculates high-precision Sidereal (Nirayana) planetary positions, Lahiri Ayanamsha (Chitrapaksha), Nakshatras, Padas, Navamsha (D-9), Lagna (Ascendant), and drives **Jagannatha Hora (Wine GUI)** autonomously to extract visual charts (Rasi D-1, Navamsha D-9, Vimshottari Dasa) and complete calculations.

---

## 🚀 Quick Reference Commands

### 1. Jagannatha Hora Autonomous GUI Runner (`jhora_runner.py`)
Generates `.jhd` chart files, loads into JHora, captures screenshots of charts and Dasas, and exports complete calculations via clipboard:

```bash
# General Chart Execution in Jagannatha Hora
~/.gemini/config/plugins/jyotish-ephemeris/skills/jyotish-ephemeris/scripts/jhora_runner.py \
  --date "1999-04-19" \
  --time "12:45pm" \
  --city "Kamarpukur" \
  --lat 22.90 \
  --lon 87.65 \
  --outdir ~/.gemini/antigravity/brain/charts
```

### 2. High-Precision Swiss Ephemeris Engine (`jyotish_calc.py`)
Terminal-based astronomical ephemeris matching JHora's Chitrapaksha Lahiri Ayanamsha:

Task | Command
:--- | :---
**Today's Planetary Positions** | `~/.gemini/config/plugins/jyotish-ephemeris/skills/jyotish-ephemeris/scripts/jyotish_calc.py`
**Chart for Specific Date & Time**| `~/.gemini/config/plugins/jyotish-ephemeris/skills/jyotish-ephemeris/scripts/jyotish_calc.py --date "1996-05-15" --time "06:30:00" --lat 22.5726 --lon 88.3639`
**Machine JSON Output** | `~/.gemini/config/plugins/jyotish-ephemeris/skills/jyotish-ephemeris/scripts/jyotish_calc.py --json`

---

## 🛠️ Jagannatha Hora (.jhd) Format Specifications

When authoring or modifying JHora `.jhd` birth files:
* **Line 1:** Month (1–12)
* **Line 2:** Day of month (1–31)
* **Line 3:** Year (YYYY)
* **Line 4:** Birth Time in `HH.MMSS` format (e.g. `3.300000` = 03:30:00 AM, `12.450000` = 12:45:00 PM). *Caution: Do NOT use fractional decimal hours; JHora treats .30 as 30 minutes.*
* **Line 5:** Timezone notation (e.g. `-5.300000` for 5 hours 30 mins East of GMT). *Negative indicates East.*
* **Line 6:** Longitude (e.g. `-88.010000` for 88° 01' East). *Negative indicates East.*
* **Line 7:** Latitude (e.g. `22.530000` for 22° 53' North). *Positive indicates North.*
* **Line 8:** Daylight Savings offset in hours (`0.000000`).
* **Lines 9 & 10:** Calculation Timezone (`-5.300000` or `-5.500000`).
* **Line 11:** `0`
* **Line 12:** `105`
* **Line 13:** City name (e.g. `Tarakeswar` or `Kamarpukur`)
* **Line 14:** Country name (`India`)

---

## 🛡️ Pop!_OS COSMIC Wayland & Wine Execution Guards

1. **Working Directory Mandate:** Always run `jhora.exe` from its directory:
   ```bash
   cd "/home/saman/.wine_jhora/drive_c/Program Files/Jagannatha Hora/bin"
   ```
   *Running from elsewhere fails to locate `swedll32.dll` and ephemeris tables.*
2. **Display Architecture:** Runs on persistent Xwayland instance on `DISPLAY=:1`.
3. **Modal & Permission Free-Pass:**
   * `/usr/bin/Xwayland` wrapper strips `-enable-ei-portal` to prevent "Allow remote control?" prompts from Wine cursor-warping calls.
   * `antigravity-freepass-sentinel.service` auto-confirms legacy Wayland portal prompts on DBus.
4. **Clipboard Extraction:** JHora copies calculations via `Ctrl+C` into the X11 clipboard under target `UTF8_STRING`. Use:
   ```bash
   xclip -selection clipboard -t UTF8_STRING -o
   ```

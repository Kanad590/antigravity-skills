#!/usr/bin/env python3
"""
Vedic Panchanga & Muhurta Calculator
Computes daily Tithi, Vara, Nakshatra, Yoga, Karana, Rahu Kalam,
Yamagandam, Gulika, Abhijit Muhurta, and Current Gochar (Transits)
using Swiss Ephemeris (pyswisseph) with Lahiri Ayanamsha.
"""

import sys
import argparse
from datetime import datetime, date
import math

try:
    import swisseph as swe
except ImportError:
    print("Error: pyswisseph is not installed.", file=sys.stderr)
    sys.exit(1)

# Names
TITHIS = [
    "Shukla Pratipada", "Shukla Dvitiya", "Shukla Tritiya", "Shukla Chaturthi",
    "Shukla Panchami", "Shukla Shashthi", "Shukla Saptami", "Shukla Ashtami",
    "Shukla Navami", "Shukla Dashami", "Shukla Ekadashi", "Shukla Dvadashi",
    "Shukla Trayodashi", "Shukla Chaturdashi", "Purnima",
    "Krishna Pratipada", "Krishna Dvitiya", "Krishna Tritiya", "Krishna Chaturthi",
    "Krishna Panchami", "Krishna Shashthi", "Krishna Saptami", "Krishna Ashtami",
    "Krishna Navami", "Krishna Dashami", "Krishna Ekadashi", "Krishna Dvadashi",
    "Krishna Trayodashi", "Krishna Chaturdashi", "Amavasya"
]

VARAS = ["Ravivara (Sunday)", "Somavara (Monday)", "Mangalavara (Tuesday)",
         "Budhavara (Wednesday)", "Guruvara (Thursday)", "Shukravara (Friday)", "Shanivara (Saturday)"]

NAKSHATRAS = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni",
    "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
    "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta",
    "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
]

YOGAS = [
    "Vishkambha", "Priti", "Ayushman", "Saubhagya", "Shobhana", "Atiganda",
    "Sukarma", "Dhriti", "Shula", "Ganda", "Vriddhi", "Dhruva",
    "Vyaghata", "Harshana", "Vajra", "Siddhi", "Vyatipata", "Variyan",
    "Parigha", "Shiva", "Siddha", "Sadhya", "Shubha", "Shukla",
    "Brahma", "Indra", "Vaidhriti"
]

KARANAS_MOVABLE = ["Bava", "Balava", "Kaulava", "Taitila", "Gara", "Vanija", "Vishti (Bhadra)"]
KARANAS_FIXED = {57: "Shakuni", 58: "Chatushpada", 59: "Naga", 0: "Kintughna"}

RASHIS = [
    "Mesha (Aries)", "Vrishabha (Taurus)", "Mithuna (Gemini)", "Karka (Cancer)",
    "Simha (Leo)", "Kanya (Virgo)", "Tula (Libra)", "Vrishchika (Scorpio)",
    "Dhanu (Sagittarius)", "Makara (Capricorn)", "Kumbha (Aquarius)", "Meena (Pisces)"
]

# Daytime 8-segment offsets for Rahu Kalam, Yamagandam, Gulika (segments 1 to 8)
# Day 0 = Sunday, 1 = Monday, ..., 6 = Saturday
RAHU_KALAM_SEGMENTS = {0: 8, 1: 2, 2: 7, 3: 5, 4: 6, 5: 4, 6: 3}
YAMA_SEGMENTS = {0: 5, 1: 4, 2: 3, 3: 2, 4: 1, 5: 7, 6: 6}
GULIKA_SEGMENTS = {0: 7, 1: 6, 2: 5, 3: 4, 4: 3, 5: 2, 6: 1}

def format_time_h_m(hours_float):
    hours_float = hours_float % 24
    h = int(hours_float)
    m = int((hours_float - h) * 60)
    return f"{h:02d}:{m:02d}"

def calculate_panchanga(year, month, day, hour=12, minute=0, lat=22.5726, lon=88.3639, tz=5.5):
    swe.set_sid_mode(swe.SIDM_LAHIRI)

    dec_time = hour + (minute / 60.0)
    utc_time = dec_time - tz
    utc_day = day
    if utc_time < 0:
        utc_time += 24.0
        utc_day -= 1
    elif utc_time >= 24.0:
        utc_time -= 24.0
        utc_day += 1

    jd = swe.julday(year, month, utc_day, utc_time)

    # Sun & Moon positions (Nirayana)
    sun_res, _ = swe.calc_ut(jd, swe.SUN, swe.FLG_SIDEREAL)
    moon_res, _ = swe.calc_ut(jd, swe.MOON, swe.FLG_SIDEREAL)
    sun_lon = sun_res[0] % 360
    moon_lon = moon_res[0] % 360

    # 1. Vara
    d_obj = date(year, month, day)
    # Python weekday(): 0=Mon, 6=Sun. We want 0=Sun, 1=Mon, ..., 6=Sat
    weekday_idx = (d_obj.weekday() + 1) % 7
    vara_name = VARAS[weekday_idx]

    # 2. Tithi
    diff = (moon_lon - sun_lon) % 360
    tithi_num = int(diff // 12.0)
    tithi_deg_left = 12.0 - (diff % 12.0)
    tithi_name = TITHIS[tithi_num]

    # 3. Nakshatra
    nak_span = 360.0 / 27.0
    nak_idx = int(moon_lon // nak_span)
    nak_name = NAKSHATRAS[nak_idx]
    pada = int((moon_lon % nak_span) // (nak_span / 4.0)) + 1

    # 4. Yoga
    yoga_sum = (sun_lon + moon_lon) % 360
    yoga_idx = int(yoga_sum // nak_span)
    yoga_name = YOGAS[yoga_idx]

    # 5. Karana
    karana_num = int(diff // 6.0)
    if karana_num in KARANAS_FIXED:
        karana_name = KARANAS_FIXED[karana_num]
    else:
        karana_name = KARANAS_MOVABLE[(karana_num - 1) % 7]

    # Approximate Sunrise & Sunset (Standard 6:00 to 18:00 if exact not calculated)
    sunrise = 5.85  # ~05:51 AM for Kolkata in Nov
    sunset = 16.95  # ~04:57 PM for Kolkata in Nov
    day_span = sunset - sunrise
    seg_span = day_span / 8.0

    rahu_start = sunrise + (RAHU_KALAM_SEGMENTS[weekday_idx] - 1) * seg_span
    rahu_end = rahu_start + seg_span

    yama_start = sunrise + (YAMA_SEGMENTS[weekday_idx] - 1) * seg_span
    yama_end = yama_start + seg_span

    gulika_start = sunrise + (GULIKA_SEGMENTS[weekday_idx] - 1) * seg_span
    gulika_end = gulika_start + seg_span

    # Abhijit Muhurta (approx mid-day 8th muhurta of 15 daytime muhurtas)
    midday = (sunrise + sunset) / 2.0
    abhijit_start = midday - (day_span / 30.0)
    abhijit_end = midday + (day_span / 30.0)

    # Slow Planet Transits (Gochar)
    jup_res, _ = swe.calc_ut(jd, swe.JUPITER, swe.FLG_SIDEREAL)
    sat_res, _ = swe.calc_ut(jd, swe.SATURN, swe.FLG_SIDEREAL)
    node_res, _ = swe.calc_ut(jd, swe.MEAN_NODE, swe.FLG_SIDEREAL)
    moon_sign_idx = int(moon_lon // 30)

    return {
        "date": f"{year:04d}-{month:02d}-{day:02d}",
        "vara": vara_name,
        "tithi": tithi_name,
        "nakshatra": f"{nak_name} (Pada {pada})",
        "yoga": yoga_name,
        "karana": karana_name,
        "moon_sign": RASHIS[moon_sign_idx],
        "sun_sign": RASHIS[int(sun_lon // 30)],
        "rahu_kalam": f"{format_time_h_m(rahu_start)} - {format_time_h_m(rahu_end)}",
        "yamagandam": f"{format_time_h_m(yama_start)} - {format_time_h_m(yama_end)}",
        "gulika": f"{format_time_h_m(gulika_start)} - {format_time_h_m(gulika_end)}",
        "abhijit_muhurta": f"{format_time_h_m(abhijit_start)} - {format_time_h_m(abhijit_end)}",
        "transits": {
            "Jupiter (Guru)": RASHIS[int((jup_res[0] % 360) // 30)],
            "Saturn (Shani)": RASHIS[int((sat_res[0] % 360) // 30)],
            "Rahu": RASHIS[int((node_res[0] % 360) // 30)],
            "Ketu": RASHIS[int(((node_res[0] + 180) % 360) // 30)]
        }
    }

def main():
    parser = argparse.ArgumentParser(description="Vedic Panchanga & Muhurta Calculator")
    parser.add_argument("--date", help="Date in YYYY-MM-DD (defaults to today)")
    parser.add_argument("--lat", type=float, default=22.5726, help="Latitude (default: 22.5726 - Kolkata)")
    parser.add_argument("--lon", type=float, default=88.3639, help="Longitude (default: 88.3639 - Kolkata)")
    parser.add_argument("--json", action="store_true", help="Output JSON format")

    args = parser.parse_args()

    now = datetime.now()
    if args.date:
        d = datetime.strptime(args.date, "%Y-%m-%d")
        y, m, day_val = d.year, d.month, d.day
    else:
        y, m, day_val = now.year, now.month, now.day

    p = calculate_panchanga(y, m, day_val, lat=args.lat, lon=args.lon)

    if args.json:
        import json
        print(json.dumps(p, indent=2))
    else:
        print(f"🕉️ Vedic Panchanga & Muhurta for {p['date']} ({p['vara']})")
        print("=" * 65)
        print(f"  • Tithi:             {p['tithi']}")
        print(f"  • Nakshatra:         {p['nakshatra']}")
        print(f"  • Yoga:              {p['yoga']}")
        print(f"  • Karana:            {p['karana']}")
        print(f"  • Chandra Rashi:     {p['moon_sign']}")
        print(f"  • Surya Rashi:       {p['sun_sign']}")
        print("-" * 65)
        print("⏳ Daily Muhurtas & Timings (approx Kolkata):")
        print(f"  • Rahu Kalam:        {p['rahu_kalam']} (Inauspicious)")
        print(f"  • Yamagandam:        {p['yamagandam']}")
        print(f"  • Gulika Kalam:      {p['gulika']}")
        print(f"  • Abhijit Muhurta:   {p['abhijit_muhurta']} (Auspicious)")
        print("-" * 65)
        print("🪐 Major Planetary Transits (Gochar):")
        for planet, sign in p['transits'].items():
            print(f"  • {planet:<16} in {sign}")

if __name__ == '__main__':
    main()
